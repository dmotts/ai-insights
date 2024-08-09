from flask import Flask, request, jsonify, render_template, send_file
import os
import logging
import datetime
from services.sheets_service import SheetsService
from services.openai_service import OpenAIService
from services.pdf_service import PDFService
from services.email_service import EmailService
from services.integration_service import IntegrationService
from services.subscription_service import SubscriptionService
from config import Config
from sqlalchemy.orm import Session
from services.models import engine
from werkzeug.exceptions import HTTPException
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
sheets_service = SheetsService(app.config['GOOGLE_SHEETS_CREDENTIALS_JSON'], "AI Insights Report Email List")
openai_service = OpenAIService(app.config['OPENAI_API_KEY'], app.config['OPENAI_MODEL'])
pdf_service = PDFService(app.config['PDFCO_API_KEY'])
email_service = EmailService()
integration_service = IntegrationService()
subscription_service = SubscriptionService()

class ReportRequestSchema(Schema):
    client_name = fields.String(required=True)
    client_email = fields.Email(required=True)
    industry = fields.String(required=True)
    question1 = fields.String(required=True)
    question2 = fields.String(required=True)
    question3 = fields.String(required=True)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # Validate and deserialize input
        data = request.json
        schema = ReportRequestSchema()
        validated_data = schema.load(data)

        industry = validated_data.get('industry')
        answers = [
            validated_data.get('question1'),
            validated_data.get('question2'),
            validated_data.get('question3'),
        ]

        # Generate the report content using the enhanced OpenAI service
        report_content = openai_service.generate_report_content(industry, answers)

        # Render the content to HTML for the report
        html_content = render_template('report_template.html', report_content=report_content)

        # Generate PDF from the HTML content
        pdf_url = pdf_service.generate_pdf(html_content) if Config.ENABLE_PDF_SERVICE else "PDF service is disabled."

        # Create a Google Doc for the report
        report_id = generate_report_id()
        doc_url = sheets_service.create_google_doc(report_id, report_content) if Config.ENABLE_SHEETS_SERVICE else "Sheets service is disabled."

        # Save the report data to Google Sheets and database
        report_data = [
            report_id,
            validated_data['client_name'],
            validated_data['client_email'],
            industry,
            pdf_url,
            doc_url,
            datetime.datetime.now().isoformat()
        ]

        if Config.ENABLE_SHEETS_SERVICE:
            sheets_service.write_data(report_data)

        if Config.ENABLE_EMAIL_SERVICE:
            email_service.send_email(
                validated_data['client_email'],
                "Your AI Insights Report is Ready",
                f"Your report has been generated. Download it here: {pdf_url}\nView it online: {doc_url}"
            )

        # Add user to subscription list
        subscription_service.add_subscriber(validated_data['client_email'], industry)

        return jsonify({"status": "success", "report_id": report_id, "pdf_url": pdf_url, "doc_url": doc_url})
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({"status": "error", "message": "Validation error", "details": err.messages}), 400
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({"status": "error", "message": "An error occurred while generating the report."}), 500


@app.route('/download_report/<report_id>', methods=['GET'])
def download_report(report_id):
    # Logic to fetch and send the PDF file
    try:
        report = sheets_service.get_report_by_id(report_id)
        if report and report['pdf_url']:
            return send_file(report['pdf_url'], as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "Report not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred while downloading the report."}), 500

def generate_report_id():
    return str(int(datetime.datetime.now().timestamp()))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
