import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
from config import Config

class EmailService:
    def __init__(self):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled.')
            return

        self.email = os.getenv('GMAIL_ADDRESS', 'your_email@gmail.com')
        self.password = os.getenv('GMAIL_APP_PASSWORD', 'your_app_password')
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

    def send_follow_up_email(self, recipient: str, report_id: str):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled. Skipping follow-up email sending.')
            return

        subject = "Follow-up on Your AI Insights Report"
        body = f"""
        Dear {recipient},

        We hope you found the AI Insights Report (ID: {report_id}) helpful for your business. 
        We would love to hear your feedback on how the recommendations are being implemented.

        Please reply to this email or contact us for further assistance.

        Best regards,
        Your AI Consultant Team
        """

        self.send_email(recipient, subject, body)
        self.logger.info(f'Follow-up email sent to {recipient} for report ID: {report_id}')

    def schedule_follow_up(self, recipient: str, report_id: str):
        if not Config.ENABLE_EMAIL_SERVICE:
            logging.info('Email service is disabled. Skipping follow-up email scheduling.')
            return

        # For demonstration, we can simulate scheduling with a simple print statement.
        # In production, consider using a task scheduler like Celery or a cron job.
        print(f"Scheduling follow-up email for {recipient} about report ID: {report_id}")
