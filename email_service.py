from flask_mail import Mail, Message
import logging

class EmailService:
    def __init__(self, app):
        self.mail = Mail(app)
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def send_email(self, recipient, subject, body):
        self.logger.debug('Sending email')
        try:
            msg = Message(subject, recipients=[recipient])
            msg.body = body
            self.mail.send(msg)
            self.logger.info('Email sent successfully')
        except Exception as e:
            self.logger.error(f'Error sending email: {e}')
