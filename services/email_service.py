import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from config import Config
import re
from datetime import datetime

class EmailService:

    def __init__(self):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled.')
            return

        self.email = Config.GMAIL_ADDRESS
        self.password = Config.GMAIL_APP_PASSWORD
        self.logger = logging.getLogger(__name__)

    def is_valid_email(self, email: str) -> bool:
        """Validates the email address using regex."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def send_email(self, recipient: str, subject: str, body: str, html_body: str = None):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled. Skipping email sending.')
            return

        if not self.is_valid_email(recipient):
            self.logger.warning(f'Invalid email address provided: {recipient}')
            return

        msg = MIMEMultipart('alternative')
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient, msg.as_string())
            server.quit()
            self.logger.info(f'Email sent successfully to {recipient}')
        except smtplib.SMTPException as e:
            self.logger.error(f'SMTP error sending email: {e}')
        except Exception as e:
            self.logger.error(f'Error sending email: {e}')

    def get_signature(self) -> str:
        """Returns the email signature."""
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
        """Injects CSS styles into the email content."""
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
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled. Skipping user report email sending.')
            return

        recipient = report_data['client_email']
        subject = f"Your AI Insights Report is Ready, {report_data['client_name']}"

        # Plaintext fallback
        body = f"""
        Hi {report_data['client_name']},

        Your AI Insights Report is ready! 

        You can download the PDF directly from the link below:
        {report_data['pdf_url']}

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
                <p><a href="{report_data['pdf_url']}" class="cta-button">Download your report</a></p>

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

        self.send_email(recipient, subject, body, html_body)
