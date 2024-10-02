from flask import Flask, request, jsonify, render_template, send_from_directory
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
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Define the reports directory
reports_dir = os.path.join(app.root_path, 'reports')
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)
    logger.debug(f"Created reports directory at {reports_dir}")

# Initialize services based on configuration flags
email_service = None
if Config.ENABLE_EMAIL_SERVICE:
    try:
        email_service = EmailService()
        logger.info("EmailService is enabled.")
    except Exception as e:
        logger.error(f"Failed to initialize EmailService: {e}", exc_info=True)
else:
    logger.info("EmailService is disabled.")

sheets_service = None
if Config.ENABLE_SHEETS_SERVICE:
    google_sheets_credentials = app.config.get('GOOGLE_SHEETS_CREDENTIALS_JSON')
    sheet_name = app.config.get('SHEET_NAME')
    if google_sheets_credentials and sheet_name:
        try:
            sheets_service = SheetsService(google_sheets_credentials, sheet_name)
            logger.info("SheetsService is enabled.")
        except Exception as e:
            logger.error(f"Failed to initialize SheetsService: {e}", exc_info=True)
    else:
        logger.error("SheetsService cannot be initialized due to missing credentials or sheet name.")
else:
    logger.info("SheetsService is disabled.")

mongodb_service = None
if Config.ENABLE_DATABASE:
    try:
        mongodb_service = MongoDBService()
        logger.info("MongoDBService is enabled.")
    except Exception as e:
        logger.error(f"Failed to initialize MongoDBService: {e}", exc_info=True)
else:
    logger.info("MongoDBService is disabled.")

llm_service = None
if Config.ENABLE_LLM_SERVICE:
    try:
        llm_service = LLMService()
        logger.info("LLMService is enabled.")
    except Exception as e:
        logger.error(f"Failed to initialize LLMService: {e}", exc_info=True)
else:
    logger.info("LLMService is disabled.")

pdf_service = None
if Config.ENABLE_PDF_SERVICE:
    try:
        pdf_service = PDFService()
        logger.info("PDFService is enabled.")
    except Exception as e:
        logger.error(f"Failed to initialize PDFService: {e}", exc_info=True)
else:
    logger.info("PDFService is disabled.")

integration_service = None
if Config.ENABLE_INTEGRATION_SERVICE:
    try:
        integration_service = IntegrationService()
        logger.info("IntegrationService is enabled.")
    except Exception as e:
        logger.error(f"Failed to initialize IntegrationService: {e}", exc_info=True)
else:
    logger.info("IntegrationService is disabled.")

subscription_service = None
if Config.ENABLE_SUBSCRIPTION_SERVICE:
    try:
        subscription_service = SubscriptionService()
        logger.info("SubscriptionService is enabled.")
    except Exception as e:
        logger.error(f"Failed to initialize SubscriptionService: {e}", exc_info=True)
else:
    logger.info("SubscriptionService is disabled.")

utilities_service = UtilitiesService()
logger.info("UtilitiesService is initialized.")

# Initialize the ReportGenerator if LLM service is enabled
report_generator = None
if llm_service:
    try:
        report_generator = ReportGenerator(
            client=llm_service.client,
            model=llm_service.model,
            utilities_service=utilities_service
        )
        logger.info("ReportGenerator is initialized with LLM service.")
    except Exception as e:
        logger.error(f"Failed to initialize ReportGenerator: {e}", exc_info=True)
else:
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

        # Generate report content
        if Config.ENABLE_LLM_SERVICE and report_generator:
            logger.info("Generating report content using LLM service")
            html_content = report_generator.generate_report_content(industry, answers, user_name)
            logger.debug(f"Generated HTML content")
        else:
            html_content = "LLM service is disabled, and report generation cannot proceed."
            logger.warning("LLM service is disabled")

        # Generate PDF
        pdf_url = None
        report_id = utilities_service.generate_report_id()
        if Config.ENABLE_PDF_SERVICE and pdf_service:
            logger.info("Generating PDF from HTML content")
            file_name = f"report-{user_name}-{report_id}.pdf"
            output_path = os.path.join(reports_dir, file_name)
            pdf_generation_result = pdf_service.generate_pdf(html_content, output_path)
            if pdf_generation_result:
                logger.info(f"PDF generated successfully at: {output_path}")
                pdf_url = f"/reports/{file_name}"
            else:
                logger.error("PDF generation failed")
        else:
            logger.warning("PDF service is disabled")

        # Create a Google Doc for the report if SheetsService is enabled
        doc_url = None
        if Config.ENABLE_SHEETS_SERVICE and sheets_service:
            logger.info(f"Creating Google Doc for report ID: {report_id}")
            doc_url = sheets_service.create_google_doc(report_id, html_content)
            logger.debug(f"Google Doc created at URL: {doc_url}")
        else:
            logger.warning("Sheets service is disabled")

        # Prepare report data
        report_data = {
            'report_id': report_id,
            'client_name': validated_data['client_name'],
            'client_email': validated_data['client_email'],
            'industry': industry,
            'pdf_url': pdf_url,
            'doc_url': doc_url,
            'created_at': utilities_service.get_current_timestamp(),
        }

        # Save report data to MongoDB
        if Config.ENABLE_DATABASE and mongodb_service:
            try:
                mongodb_service.save_report_data(report_data)
                logger.info("Report data saved to MongoDB")
            except Exception as e:
                logger.error(f"Error saving report data to MongoDB: {e}", exc_info=True)

        # Save report data to Google Sheets
        if Config.ENABLE_SHEETS_SERVICE and sheets_service:
            try:
                sheets_service.write_data(data=report_data)
                logger.info("Report data written to Google Sheets")
            except Exception as e:
                logger.error(f"Error writing data to Google Sheets: {e}", exc_info=True)

        # Send report email to user
        if Config.ENABLE_EMAIL_SERVICE and email_service:
            try:
                logger.info("Sending report email to user")
                email_service.send_report_email_to_user(report_data)
                logger.info("Report email sent to user")
            except Exception as e:
                logger.error(f"Failed to send report email to user: {e}", exc_info=True)

        # Send notification email to admin
        if Config.ENABLE_EMAIL_SERVICE and email_service:
            try:
                logger.info("Sending notification email to admin")
                email_service.send_notification_email_to_admin(report_data)
                logger.info("Notification email sent to admin")
            except Exception as e:
                logger.error(f"Failed to send notification email to admin: {e}", exc_info=True)

        # Add the user to the subscription list if enabled
        if Config.ENABLE_SUBSCRIPTION_SERVICE and subscription_service:
            try:
                subscription_service.add_subscriber(validated_data['client_email'], industry)
                logger.info(f"Subscriber added: {validated_data['client_email']}")
            except Exception as e:
                logger.error(f"Failed to add subscriber: {e}", exc_info=True)

        logger.info(f'Report generated successfully with ID: {report_id}')
        return jsonify({
            "status": "success",
            "report_id": report_id,
            "pdf_url": pdf_url,
            "doc_url": doc_url
        })
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({
            "status": "error",
            "message": "Validation error",
            "details": err.messages
        }), 400
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An error occurred while generating the report."
        }), 500

@app.route('/reports/<filename>')
def serve_pdf(filename):
    logger.debug(f"Serving PDF file: {filename}")
    return send_from_directory(reports_dir, filename)

@app.route('/dashboard')
def dashboard():
    logger.info("Rendering the dashboard page")
    return render_template('dashboard/index.html')

# Main entry point to run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)