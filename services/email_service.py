from protonmail import ProtonMail
import logging
from config import Config
import re
from datetime import datetime

class EmailService:

    def __init__(self):
        """
        Initializes the EmailService with ProtonMail credentials for sending emails.
        Sets up the ProtonMail API client.
        """
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled.')
            return

        self.email = Config.PROTONMAIL_ADDRESS
        self.password = Config.PROTONMAIL_PASSWORD
        self.logger = logging.getLogger(__name__)

        # Set up ProtonMail API client
        self.proton = ProtonMail()
        try:
            self.proton.login(self.email, self.password)
            self.logger.info("Successfully logged in to ProtonMail.")
        except Exception as e:
            self.logger.error(f"Failed to log in to ProtonMail: {e}")
            raise

        # Set up custom logging handler for email alerts
        self.setup_email_alerts()

    def setup_email_alerts(self):
        """
        Sets up a custom logging handler to send email alerts for errors.
        """
        try:
            handler = logging.StreamHandler()  # You can replace this with a file handler or other as needed
            handler.setLevel(logging.ERROR)
            handler.addFilter(self.EmailAlertFilter(self))

            # Add the handler to the logger
            self.logger.addHandler(handler)
            self.logger.info("Email alerts have been set up successfully.")
        except Exception as e:
            self.logger.error(f"Failed to set up email alerts: {e}")

    class EmailAlertFilter(logging.Filter):
        """
        A logging filter that sends an email when an ERROR level log is recorded.
        """
        def __init__(self, email_service):
            super().__init__()
            self.email_service = email_service

        def filter(self, record):
            if record.levelno >= logging.ERROR:
                try:
                    self.email_service.send_email(
                        recipient=Config.NOTIFICATION_EMAIL,
                        subject=f"Critical Error in Application: {record.levelname}",
                        body=record.getMessage()
                    )
                except Exception as e:
                    self.email_service.logger.error(f"Failed to send alert email: {e}")
            return True

    def is_valid_email(self, email: str) -> bool:
        """
        Validates the email address using a regex pattern.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def send_email(self, recipient: str, subject: str, body: str, html_body: str = None, attachments=None):
        """
        Sends an email to the specified recipient with both plain text and HTML options.
        """
        if not Config.ENABLE_EMAIL_SERVICE:
            self.logger.info('Email service is disabled. Skipping email sending.')
            return

        if not self.is_valid_email(recipient):
            self.logger.warning(f'Invalid email address provided: {recipient}')
            return

        try:
            # Create attachments if any
            attachment_objects = []
            if attachments:
                for attachment in attachments:
                    with open(attachment['file_path'], 'rb') as f:
                        content = f.read()
                    attachment_obj = self.proton.create_attachment(content=content, name=attachment['file_name'])
                    attachment_objects.append(attachment_obj)

            # Send message
            message = self.proton.create_message(
                recipients=[recipient],
                subject=subject,
                body=html_body if html_body else body,
                attachments=attachment_objects
            )
            sent_message = self.proton.send_message(message)
            self.logger.info(f'Email sent successfully to {recipient}')
        except Exception as e:
            self.logger.error(f'Error sending email: {e}')

    def get_signature(self) -> str:
        """
        Returns the email signature.
        """
        return """
        <table style="width: 100%; margin-top: 20px;">
            <tr>
                <td style="padding: 10px 0; font-family: Arial, sans-serif; font-size: 14px;">
                    <p style="margin: 0;">Best regards,</p>
                    <p style="margin: 5px 0;">Daley Mottley</p>
                    <p style="margin: 0;">
                        <a href="http://daleymottley.com" style="color: #7a26b1; text-decoration: underline;">
                            daleymottley.com
                        </a>
                    </p>
                </td>
            </tr>
        </table>
        """

    def inject_styles(self, html_content: str) -> str:
        """
        Injects CSS styles into the email content.
        """
        styles = """
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                background-color: #f4f4f4;
                padding: 0;
                margin: 0;
            }
            .email-container {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .header {
                background-color: #7a26b1;
                padding: 20px;
                text-align: center;
                color: #ffffff;
            }
            .header h1 {
                font-size: 24px;
                margin: 0;
                font-weight: normal;
            }
            .content {
                padding: 20px;
                text-align: left;
            }
            .content h2 {
                color: #7a26b1;
                font-size: 18px;
                margin-top: 0;
            }
            .content p {
                font-size: 16px;
                margin: 15px 0;
            }
            .cta-button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #7a26b1;
                color: #ffffff;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                font-size: 16px;
            }
            .footer {
                background-color: #333333;
                color: #ffffff;
                text-align: center;
                padding: 15px 10px;
                font-size: 14px;
            }
            .footer a,
            .footer a:hover,
            .footer a:active {
                color: inherit;
                text-decoration: none;
            }
        </style>
        """
        return f"<html><head>{styles}</head><body>{html_content}</body></html>"

    def send_report_email_to_user(self, report_data: dict):
        """
        Sends a report email to the user with a link to the PDF report.
        """
        if not Config.ENABLE_EMAIL_SERVICE:
            self.logger.info('Email service is disabled. Skipping user report email sending.')
            return

        recipient = report_data['client_email']
        subject = f"Your AI Insights Report is Ready, {report_data['client_name']}"

        # Get the PDF URL (from Google Drive if SheetsService is enabled, otherwise fallback to PDF.co)
        pdf_url = report_data.get('pdf_url', '#')

        # Plaintext fallback
        body = f"""
        Hi {report_data['client_name']},

        Your AI Insights Report is ready! 

        You can download the PDF directly from the link below:
        {pdf_url}

        I hope you find the insights valuable. If you have any questions or would like to discuss further how AI can benefit your business, feel free to reach out. I'm here to help.

        {self.get_signature()}
        """

        # HTML body with refined design
        html_body_content = f"""
        <div class="email-container">
            <div class="header">
                <h1>Your AI Insights Report is Ready!</h1>
            </div>
            <div class="content">
                <p>Hi {report_data['client_name']},</p>

                <p>Your <strong>AI Insights Report</strong> is ready and waiting for you.</p>

                <p>You can download the PDF directly from the link below:</p>
                <p><a href="{pdf_url}" class="cta-button">Download your report</a></p>

                <p>I hope you find the insights valuable. If you have any questions or would like to discuss further how AI can benefit your business, feel free to reach out. I'm here to help.</p>

                {self.get_signature()}
            </div>
            <div class="footer">
                <p>&copy; {datetime.now().year} <a href="http://daleymottley.com">Daley Mottley AI Consulting</a> | All Rights Reserved</p>
            </div>
        </div>
        """

        # Inject styles into the HTML content
        html_body = self.inject_styles(html_body_content)

        # Send the email
        self.send_email(recipient, subject, body, html_body)

    def send_notification_email_to_admin(self, report_data: dict):
        """
        Sends a notification email to the admin with links to the PDF report, database record, and Google Sheets entry.
        """
        if not Config.ENABLE_EMAIL_SERVICE:
            self.logger.info('Email service is disabled. Skipping admin notification email sending.')
            return

        recipient = Config.NOTIFICATION_EMAIL
        subject = f"New AI Insights Report Generated for {report_data['client_name']}"

        # Construct URLs
        pdf_url = report_data.get('pdf_url', '#')
        doc_url = report_data.get('doc_url', '#')
        db_record_url = f"https://yourapp.com/reports/{report_data['report_id']}"
        sheet_url = f"https://docs.google.com/spreadsheets/d/{report_data.get('sheet_id', '#')}/edit"

        # Plaintext fallback
        body = f"""
        A new AI Insights Report has been generated for {report_data['client_name']}.

        You can download the PDF directly from the link below:
        {pdf_url}

        View the report record in the database:
        {db_record_url}

        View the report entry in Google Sheets:
        {sheet_url}

        Report ID: {report_data['report_id']}
        """

        # HTML body with refined design
        html_body_content = f"""
        <div class="email-container">
            <div class="header">
                <h1>New AI Insights Report Generated!</h1>
            </div>
            <div class="content">
                <p>A new <strong>AI Insights Report</strong> has been generated for {report_data['client_name']}.</p>

                <p>You can download the PDF directly from the link below:</p>
                <p><a href="{pdf_url}" class="cta-button">Download the report</a></p>

                <p>View the report record in the database: <a href="{db_record_url}">Database Record</a></p>
                <p>View the report entry in Google Sheets: <a href="{sheet_url}">Google Sheet Entry</a></p>

                <p>Report ID: {report_data['report_id']}</p>

                {self.get_signature()}
            </div>
            <div class="footer">
                <p>&copy; {datetime.now().year} <a href="http://daleymottley.com">Daley Mottley AI Consulting</a> | All Rights Reserved</p>
            </div>
        </div>
        """

        # Inject styles into the HTML content
        html_body = self.inject_styles(html_body_content)

        # Send the email
        self.send_email(recipient, subject, body, html_body)

