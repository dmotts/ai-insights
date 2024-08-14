import os
import json
import logging
from distutils.util import strtobool

class Config:
    # Google Sheets Configuration (Check environment variables first, then fall back to file)
    GOOGLE_SHEETS_CREDENTIALS = None

    def load_google_sheets_credentials():
        if os.getenv('GOOGLE_SHEETS_TYPE'):
            return {
                "type": os.getenv('GOOGLE_SHEETS_TYPE', 'service_account'),
                "project_id": os.getenv('GOOGLE_SHEETS_PROJECT_ID', ''),
                "private_key_id": os.getenv('GOOGLE_SHEETS_PRIVATE_KEY_ID', ''),
                "private_key": os.getenv('GOOGLE_SHEETS_PRIVATE_KEY', '').replace('\\n', '\n'),
                "client_email": os.getenv('GOOGLE_SHEETS_CLIENT_EMAIL', ''),
                "client_id": os.getenv('GOOGLE_SHEETS_CLIENT_ID', ''),
                "auth_uri": os.getenv('GOOGLE_SHEETS_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                "token_uri": os.getenv('GOOGLE_SHEETS_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                "auth_provider_x509_cert_url": os.getenv('GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL', 'https://www.googleapis.com/oauth2/v1/certs'),
                "client_x509_cert_url": os.getenv('GOOGLE_SHEETS_CLIENT_X509_CERT_URL', ''),
            }
        else:
            try:
                with open('credentials.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                logging.warning("credentials.json not found and no environment variables set for Google Sheets credentials.")
            except json.JSONDecodeError:
                logging.error("Invalid JSON format in credentials.json.")
            return None

    GOOGLE_SHEETS_CREDENTIALS = load_google_sheets_credentials()

    if not GOOGLE_SHEETS_CREDENTIALS:
        raise ValueError("Google Sheets credentials are not set. Please configure them via environment variables or credentials.json.")

    SHEET_NAME = os.getenv('SHEET_NAME', 'ReportData')
    GOOGLE_DRIVE_FOLDER_NAME = os.getenv('GOOGLE_DRIVE_FOLDER_NAME', 'AI_Reports')

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    logging.basicConfig(level=LOG_LEVEL)

    # LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LLM_MODEL = os.getenv('LLM_MODEL')
    USE_OPENAI_API = strtobool(os.getenv('USE_OPENAI_API', 'True'))

    # PDF.co Configuration
    PDFCO_API_KEY = os.getenv('PDFCO_API_KEY')

    # ProtonMail Configuration
    PROTONMAIL_ADDRESS = os.getenv('PROTONMAIL_ADDRESS', '')
    PROTONMAIL_PASSWORD = os.getenv('PROTONMAIL_PASSWORD', '')

    # Notification Email
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')

    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI')
    MONGODB_DATABASE_NAME = os.getenv('MONGODB_DATABASE_NAME', 'ai')
    MONGODB_COLLECTION_NAME = os.getenv('MONGODB_COLLECTION_NAME', 'reports')

    # Feature Flags to enable/disable services
    ENABLE_DATABASE = strtobool(os.getenv('ENABLE_DATABASE', 'True'))
    ENABLE_EMAIL_SERVICE = strtobool(os.getenv('ENABLE_EMAIL_SERVICE', 'True'))
    ENABLE_LLM_SERVICE = strtobool(os.getenv('ENABLE_LLM_SERVICE', 'True'))
    ENABLE_PDF_SERVICE = strtobool(os.getenv('ENABLE_PDF_SERVICE', 'True'))
    ENABLE_SHEETS_SERVICE = strtobool(os.getenv('ENABLE_SHEETS_SERVICE', 'True'))
    ENABLE_INTEGRATION_SERVICE = strtobool(os.getenv('ENABLE_INTEGRATION_SERVICE', 'True'))
    ENABLE_SUBSCRIPTION_SERVICE = strtobool(os.getenv('ENABLE_SUBSCRIPTION_SERVICE', 'True'))

    @classmethod
    def validate_config(cls):
        """Raise errors if critical configurations are missing."""
        if cls.ENABLE_LLM_SERVICE and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in the environment.")
        if cls.ENABLE_PDF_SERVICE and not cls.PDFCO_API_KEY:
            raise ValueError("PDFCO_API_KEY must be set in the environment.")
        if cls.ENABLE_EMAIL_SERVICE and (not cls.PROTONMAIL_ADDRESS or not cls.PROTONMAIL_PASSWORD):
            raise ValueError("PROTONMAIL_ADDRESS and PROTONMAIL_PASSWORD must be set in the environment.")
        if cls.ENABLE_DATABASE and not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI must be set in the environment.")

        # Validate Google Sheets credentials
        if cls.ENABLE_SHEETS_SERVICE:
            required_fields = ['project_id', 'private_key_id', 'private_key', 'client_email', 'client_id']
            for field in required_fields:
                if not cls.GOOGLE_SHEETS_CREDENTIALS or not cls.GOOGLE_SHEETS_CREDENTIALS.get(field):
                    raise ValueError(f"Google Sheets {field} must be set in the environment or credentials.json.")

# Validate configuration on startup
Config.validate_config()