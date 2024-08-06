import os

class Config:
    GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json')
    SHEET_NAME = os.getenv('SHEET_NAME', 'ReportData')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    PDFCO_API_KEY = os.getenv('PDFCO_API_KEY', 'your_pdfco_api_key')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your_email@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_password')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true') == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false') == 'true'
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@example.com')
