from flask import Flask, request, jsonify, render_template
import os
import logging
from services.sheets_service import SheetsService
from services.llm_service import LLMService
from services.pdf_service import PDFService
from services.email_service import EmailService
from services.integration_service import IntegrationService
from services.subscription_service import SubscriptionService
from services.report_generator import ReportGenerator
from services.utilities_service import UtilitiesService
from services.mongodb_service import MongoDBService
from config import Config
from werkzeug.exceptions import HTTPException
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config.from_object(Config)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize services based on configuration flags
try:
    email_service = EmailService() if Config.ENABLE_EMAIL_SERVICE else None
    if email_service:
        logger.info("EmailService is enabled.")
    else:
        logger.info("EmailService is disabled.")
except Exception as e:
    if "CAPTCHA" in str(e):
        logger.error("Failed to initialize EmailService: CAPTCHA is required and not implemented.")
    else:
        logger.error(f"Failed to initialize EmailService: {e}")
    email_service = None

# Check if Google Sheets credentials are provided before initializing the SheetsService
if Config.ENABLE_SHEETS_SERVICE:
    google_sheets_credentials = app.config.get('GOOGLE_SHEETS_CREDENTIALS_JSON')
    sheet_name = app.config.get('SHEET_NAME')
    if google_sheets_credentials and sheet_name:
        sheets_service = SheetsService(google_sheets_credentials, sheet_name)
        logger.info("SheetsService is enabled.")
    else:
        logger.error("SheetsService cannot be initialized due to missing credentials or sheet name.")
        sheets_service = None
else:
    sheets_service = None
    logger.info("SheetsService is disabled.")

mongodb_service = MongoDBService() if Config.ENABLE_DATABASE else None
if mongodb_service:
    logger.info("MongoDBService is enabled.")
else:
    logger.info("MongoDBService is disabled.")

llm_service = LLMService() if Config.ENABLE_LLM_SERVICE else None
if llm_service:
    logger.info("LLMService is enabled.")
else:
    logger.info("LLMService is disabled.")

pdf_service = PDFService(app.config['PDFCO_API_KEY']) if Config.ENABLE_PDF_SERVICE else None
if pdf_service:
    logger.info("PDFService is enabled.")
else:
    logger.info("PDFService is disabled.")

integration_service = IntegrationService() if Config.ENABLE_INTEGRATION_SERVICE else None
if integration_service:
    logger.info("IntegrationService is enabled.")
else:
    logger.info("IntegrationService is disabled.")

subscription_service = SubscriptionService() if Config.ENABLE_SUBSCRIPTION_SERVICE else None
if subscription_service:
    logger.info("SubscriptionService is enabled.")
else:
    logger.info("SubscriptionService is disabled.")

utilities_service = UtilitiesService('path_to/GeoLite2-City.mmdb')
logger.info("UtilitiesService is initialized.")

# Initialize the ReportGenerator if LLM service is enabled
if llm_service:
    report_generator = ReportGenerator(
        client=llm_service.client,
        model=llm_service.model,
        utilities_service=utilities_service
    )
    logger.info("ReportGenerator is initialized with LLM service.")
else:
    report_generator = None
    logger.info("ReportGenerator is not initialized because LLM service is disabled.")

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return utilities_service.handle_http_exception(e)

@app.errorhandler(Exception)
def handle_exception(e):
    return utilities_service.handle_general_exception(e)

@app.route('/')
def index():
    logger.info("Rendering the main report generation page")
    return render_template('generate_report.html')

# Define the ReportRequestSchema
class ReportRequestSchema(Schema):
    client_name = fields.Str(required=True)
    client_email = fields.Email(required=True)
    industry = fields.Str(required=True)
    question1 = fields.Str(required=True)
    question2 = fields.Str(required=True)
    question3 = fields.Str(required=True)

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

        user_name = validated_data.get('client_name')
        industry = validated_data.get('industry')
        answers = [
            validated_data.get('question1'),
            validated_data.get('question2'),
            validated_data.get('question3'),
        ]

        # Get user information from headers using UtilitiesService
        user_device_info = utilities_service.extract_user_info(request)

        # Delegate report generation to the ReportGenerator class
        if Config.ENABLE_LLM_SERVICE and report_generator:
            logger.info("Generating report content using LLM service")
            html_content = report_generator.generate_report_content(industry, answers, user_name)
            logger.debug(f"Generated HTML content: {html_content}")
        else:
            html_content = "LLM service is disabled, and report generation cannot proceed."
            logger.warning("LLM service is disabled")

        # Generate a PDF from the HTML content
        if Config.ENABLE_PDF_SERVICE and pdf_service:
            logger.info("Generating PDF from HTML content")
            pdf_url = pdf_service.generate_pdf(html_content)
            if pdf_url:
                logger.info(f"PDF generated successfully at: {pdf_url}")
                file_name = f"report-{user_name}-{utilities_service.generate_report_id()}.pdf"
                output_path = os.path.join("/tmp", file_name)
                pdf_service.download_pdf(pdf_url, output_path)

                if Config.ENABLE_SHEETS_SERVICE and sheets_service:
                    google_drive_pdf_url = sheets_service.save_pdf_to_drive(output_path, file_name)
                    logger.debug(f"PDF saved to Google Drive at URL: {google_drive_pdf_url}")
                else:
                    google_drive_pdf_url = pdf_url  # Use the PDF.co URL as a fallback
            else:
                logger.error("PDF generation failed")
                google_drive_pdf_url = None
        else:
            google_drive_pdf_url = None
            logger.warning("PDF service is disabled")

        # Create a Google Doc for the report if SheetsService is enabled
        report_id = utilities_service.generate_report_id()
        if Config.ENABLE_SHEETS_SERVICE and sheets_service:
            logger.info(f"Creating Google Doc for report ID: {report_id}")
            doc_url = sheets_service.create_google_doc(report_id, html_content)
            logger.debug(f"Google Doc created at URL: {doc_url}")
        else:
            doc_url = None
            logger.warning("Sheets service is disabled")

        # Prepare report data
        report_data = {
            'report_id': report_id,
            'client_name': validated_data['client_name'],
            'client_email': validated_data['client_email'],
            'industry': industry,
            'pdf_url': google_drive_pdf_url,
            'doc_url': doc_url,
            'created_at': utilities_service.get_current_timestamp(),
            **user_device_info
        }

        # Save report data to MongoDB
        if Config.ENABLE_DATABASE and mongodb_service:
            try:
                mongodb_service.save_report_data(report_data)
            except Exception as e:
                logger.error(f"Error saving report data to MongoDB: {e}")

        # Save report data to Google Sheets
        if Config.ENABLE_SHEETS_SERVICE and sheets_service:
            try:
                sheets_service.write_data(data=report_data)
            except Exception as e:
                logger.error(f"Error writing data to Google Sheets: {e}")

        # Send report email to user
        if Config.ENABLE_EMAIL_SERVICE and email_service:
            try:
                logger.info("Sending report email to user")
                email_service.send_report_email_to_user(report_data)
            except Exception as e:
                logger.error(f"Failed to send report email to user: {e}")

        # Send notification email to admin
        if Config.ENABLE_EMAIL_SERVICE and email_service:
            try:
                logger.info("Sending notification email to admin")
                email_service.send_notification_email_to_admin(report_data)
            except Exception as e:
                logger.error(f"Failed to send notification email to admin: {e}")

        # Add the user to the subscription list if enabled
        if Config.ENABLE_SUBSCRIPTION_SERVICE and subscription_service:
            try:
                subscription_service.add_subscriber(validated_data['client_email'], industry)
                logger.info(f"Subscriber added to the list: {validated_data['client_email']}")
            except Exception as e:
                logger.error(f"Failed to add subscriber: {e}")

        logger.info(f'Report generated successfully with ID: {report_id}')
        return jsonify({"status": "success", "report_id": report_id, "pdf_url": google_drive_pdf_url, "doc_url": doc_url})
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({"status": "error", "message": "Validation error", "details": err.messages}), 400
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "An error occurred while generating the report."}), 500

@app.route('/dashboard')
def dashboard():
    logger.info("Rendering the dashboard page")
    return render_template('dashboard/index.html')


# Main entry point to run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
