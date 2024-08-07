import os

class Config:
    GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json')
    SHEET_NAME = os.getenv('SHEET_NAME', 'ReportData')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    PDFCO_API_KEY = os.getenv('PDFCO_API_KEY', 'your_pdfco_api_key')
    GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS', '')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
    
    # Use the DATABASE_URL from Render
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')
    
    # Feature flags to enable/disable services
    ENABLE_DATABASE = os.getenv('ENABLE_DATABASE', 'True') == 'True'
    ENABLE_EMAIL_SERVICE = os.getenv('ENABLE_EMAIL_SERVICE', 'True') == 'True'
    ENABLE_OPENAI_SERVICE = os.getenv('ENABLE_OPENAI_SERVICE', 'True') == 'True'
    ENABLE_PDF_SERVICE = os.getenv('ENABLE_PDF_SERVICE', 'True') == 'True'
    ENABLE_SHEETS_SERVICE = os.getenv('ENABLE_SHEETS_SERVICE', 'True') == 'True'
    ENABLE_INTEGRATION_SERVICE = os.getenv('ENABLE_INTEGRATION_SERVICE', 'True') == 'True'
    ENABLE_SUBSCRIPTION_SERVICE = os.getenv('ENABLE_SUBSCRIPTION_SERVICE', 'True') == 'True'