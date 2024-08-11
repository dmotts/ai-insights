import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from config import Config

class EmailService:
    def __init__(self):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled.')
            return

        self.email = Config.GMAIL_ADDRESS
        self.password = Config.GMAIL_APP_PASSWORD
        self.logger = logging.getLogger(__name__)

    def send_email(self, recipient: str, subject: str, body: str):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled. Skipping email sending.')
            return

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

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

    def send_notification_email(self, report_data: dict, user_device_info: dict, spreadsheet_url: str):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled. Skipping notification email sending.')
            return

        recipient = Config.NOTIFICATION_EMAIL
        subject = f"New Report Generated - {report_data['client_name']} ({report_data['created_at']})"

        body = f"""
        A new report has been generated.

        Report ID: {report_data['report_id']}
        Client Name: {report_data['client_name']}
        Client Email: {report_data['client_email']}
        Industry: {report_data['industry']}

        Date/Time: {report_data['created_at']}
        Location: {user_device_info.get('location', 'Unknown')}
        Device: {user_device_info.get('device', 'Unknown')}
        IP Address: {user_device_info.get('ip_address', 'Unknown')}
        Language: {user_device_info.get('language', 'Unknown')}
        Referrer: {user_device_info.get('referrer', 'Unknown')}

        Spreadsheet Link: {spreadsheet_url}
        PDF Link: {report_data['pdf_url']}

        Best regards,
        AI Consulting Team
        """

        self.send_email(recipient, subject, body)
        self.logger.info(f'Notification email sent to {recipient} for report ID: {report_data["report_id"]}')
