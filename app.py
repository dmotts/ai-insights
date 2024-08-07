from flask import Flask, request, jsonify, render_template, url_for
from flask_mail import Mail, Message
import os
import logging
import datetime
from services.sheets_service import SheetsService
from services.openai_service import OpenAIService
from services.pdf_service import PDFService
from services.email_service import EmailService
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

logging.basicConfig(level=app.config['LOG_LEVEL'])
logger = logging.getLogger(__name__)

# Initialize services
sheets_service = SheetsService(app.config['GOOGLE_SHEETS_CREDENTIALS_JSON'], app.config['SHEET_NAME'])
openai_service = OpenAIService(app.config['OPENAI_API_KEY'], app.config['OPENAI_MODEL'])
pdf_service = PDFService(app.config['PDFCO_API_KEY'])
email_service = EmailService(app)

@app.route('/')
def index():
    return render_template('generate_report.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    answers = [
        data.get('question1'),
        data.get('question2'),
        data.get('question3'),
        data.get('question4'),
        data.get('question5')
    ]
    report_content = openai_service.generate_report_content(answers)
    html_content = render_template('report_template.html', **report_content)
    pdf_url = pdf_service.generate_pdf(html_content)

    if not pdf_url:
        return jsonify({"status": "error", "message": "Failed to generate PDF"}), 500

    report_data = [generate_report_id(), data['client_name'], report_content, pdf_url, datetime.datetime.now().isoformat()]
    sheets_service.write_data(report_data)

    email_service.send_email(
        data['client_email'],
        "Your AI Insights Report is Ready",
        f"Your report has been generated. You can download it from the following link: {pdf_url}"
    )

    logger.info(f'Report generated with ID: {report_data[0]}')
    return jsonify({"status": "success", "report_id": report_data[0], "pdf_url": pdf_url})

@app.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    all_reports = sheets_service.read_data()
    report = next((report for report in all_reports if report['Report ID'] == report_id), None)

    if report:
        logger.info(f'Report found: {report_id}')
        return jsonify(report)
    else:
        logger.warning(f'Report not found: {report_id}')
        return jsonify({"status": "error", "message": "Report not found"}), 404

def generate_report_id():
    return str(int(datetime.datetime.now().timestamp()))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
