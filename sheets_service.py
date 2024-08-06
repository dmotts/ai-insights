import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

class SheetsService:
    def __init__(self, credentials_json, sheet_name):
        """
        Initializes the SheetsService with Google Sheets credentials and sheet name.
        """
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheet_name).sheet1
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def read_data(self):
        """
        Reads all records from the Google Sheet.
        """
        self.logger.debug('Reading data from Google Sheets')
        try:
            data = self.sheet.get_all_records()
            self.logger.info('Data read successfully')
            return data
        except Exception as e:
            self.logger.error(f'Error reading data: {e}')
            return []

    def write_data(self, data):
        """
        Writes a new row of data to the Google Sheet.
        """
        self.logger.debug('Writing data to Google Sheets')
        try:
            self.sheet.append_row(data)
            self.logger.info('Data written successfully')
        except Exception as e:
            self.logger.error(f'Error writing data: {e}')
