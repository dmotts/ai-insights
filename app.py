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

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize services
sheets_service = SheetsService(app.config['GOOGLE_SHEETS_CREDENTIALS_JSON'], "AI Insights Report Email List")
openai_service = OpenAIService(app.config['OPENAI_API_KEY'], app.config['OPENAI_MODEL'])
pdf_service = PDFService(app.config['PDFCO_API_KEY'])
email_service = EmailService()
integration_service = IntegrationService()
subscription_service = SubscriptionService()

# Schema for validating incoming report generation requests
class ReportRequestSchema(Schema):
    client_name = fields.String(required=True)
    client_email = fields.Email(required=True)
    industry = fields.String(required=True)
    question1 = fields.String(required=True)
    question2 = fields.String(required=True)
    question3 = fields.String(required=True)

# Error handler for HTTP exceptions
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    logger.error(f"HTTP error occurred: {e}")
    return jsonify({"status": "error", "message": e.description}), e.code

# General error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error occurred: {e}", exc_info=True)  # Log the full traceback for debugging
    return jsonify({"status": "error", "message": "An internal error occurred"}), 500

# Route to render the main report generation page
@app.route('/')
def index():
    logger.info("Rendering the main report generation page")
    return render_template('generate_report.html')

# Route to handle report generation requests
@app.route('/generate_report', methods=['POST'])
def generate_report():
    logger.info("Received a request to generate a report")
    try:
        # Validate and deserialize input data
        data = request.json
        logger.debug(f"Request data received: {data}")

        schema = ReportRequestSchema()
        validated_data = schema.load(data)
        logger.debug(f"Validated data: {validated_data}")

        industry = validated_data.get('industry')
        answers = [
            validated_data.get('question1'),
            validated_data.get('question2'),
            validated_data.get('question3'),
        ]

        # Generate the report content using OpenAI service
        logger.info("Generating report content using OpenAI service")
        report_content = openai_service.generate_report_content(industry, answers)
        logger.debug(f"Generated report content: {report_content}")

        # Render the report content to HTML
        html_content = render_template('report_template.html', 
                                        introduction=report_content.get('introduction'),
                                        industry_trends=report_content.get('industry_trends'),
                                        ai_solutions=report_content.get('ai_solutions'),
                                        analysis=report_content.get('analysis'),
                                        conclusion=report_content.get('conclusion'))
        logger.info("Report content rendered to HTML")

        # Generate a PDF from the HTML content
        if Config.ENABLE_PDF_SERVICE:
            logger.info("Generating PDF from HTML content")
            pdf_url = pdf_service.generate_pdf(html_content)
            logger.debug(f"PDF generated at URL: {pdf_url}")
        else:
            pdf_url = "PDF service is disabled."
            logger.warning("PDF service is disabled")

        # Create a Google Doc for the report
        report_id = generate_report_id()
        if Config.ENABLE_SHEETS_SERVICE:
            logger.info(f"Creating Google Doc for report ID: {report_id}")
            doc_url = sheets_service.create_google_doc(report_id, html_content)
            logger.debug(f"Google Doc created at URL: {doc_url}")
        else:
            doc_url = "Sheets service is disabled."
            logger.warning("Sheets service is disabled")

        # Save report data to Google Sheets and database
        report_data = {
            'report_id': report_id,
            'client_name': validated_data['client_name'],
            'client_email': validated_data['client_email'],
            'industry': industry,
            'pdf_url': pdf_url,
            'doc_url': doc_url,
            'created_at': datetime.datetime.now().isoformat()
        }

        if Config.ENABLE_SHEETS_SERVICE:
            logger.info("Saving report data to Google Sheets and database")
            sheets_service.write_data(data=report_data, db=db)        else:            logger.warning("Sheets service is disabled, skipping data saving")

        if Config.ENABLE_EMAIL_SERVICE:
            logger.info("Sending report via email")
            # Send an email to the user with links to the generated report
            email_service.send_email(
                validated_data['client_email'],
                "Your AI Insights Report is Ready",
                f"Your report has been generated. Download it here: {pdf_url}\nView it online: {doc_url}"
            )

        # Add the user to the subscription list
        subscription_service.add_subscriber(validated_data['client_email'], industry)
        logger.info(f"Subscriber added to the list: {validated_data['client_email']}")

        logger.info(f'Report generated successfully with ID: {report_id}')
        return jsonify({"status": "success", "report_id": report_id, "pdf_url": pdf_url, "doc_url": doc_url})
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({"status": "error", "message": "Validation error", "details": err.messages}), 400
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)  # Log the full traceback
        return jsonify({"status": "error", "message": "An error occurred while generating the report."}), 500

# Route to handle report download requests
@app.route('/download_report/<report_id>', methods=['GET'])
def download_report(report_id):
    logger.info(f"Received a request to download report with ID: {report_id}")
    try:
        # Fetch the report from the database or Google Sheets
        report = sheets_service.get_report_by_id(report_id)
        if report and 'pdf_url' in report:
            logger.info(f"Report found, sending file: {report['pdf_url']}")
            return send_file(report['pdf_url'], as_attachment=True)
        else:
            logger.warning(f"Report not found: {report_id}")
            return jsonify({"status": "error", "message": "Report not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving report: {e}", exc_info=True)  # Log the full traceback
        return jsonify({"status": "error", "message": "An error occurred while downloading the report."}), 500

# Function to generate a unique report ID based on timestamp
def generate_report_id():
    report_id = str(int(datetime.datetime.now().timestamp()))
    logger.debug(f"Generated report ID: {report_id}")
    return report_id

# Main entry point to run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
