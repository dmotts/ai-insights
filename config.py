import os

class Config:
    GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json')
    SHEET_NAME = os.getenv('SHEET_NAME', 'ReportData')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    PDFCO_API_KEY = os.getenv('PDFCO_API_KEY', 'your_pdfco_api_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg2://username:password@your-instance-ip/dbname')
    GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS', '')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
