import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from .models import Report
import logging

class SheetsService:
    def __init__(self, credentials_json, sheet_name):
        """
        Initializes the SheetsService with Google Sheets credentials and sheet name.
        """
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/documents"
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, self.scope)
        self.client = gspread.authorize(self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.sheet = self._get_or_create_sheet(sheet_name)
        self.logger = logging.getLogger(__name__)

    def _get_or_create_sheet(self, sheet_name):
        """
        Gets or creates a Google Sheet with the specified name.
        """
        try:
            sheet = self.client.open(sheet_name).sheet1
            self.logger.info(f'Using existing sheet: {sheet_name}')
            return sheet
        except gspread.SpreadsheetNotFound:
            self.logger.info(f'Sheet "{sheet_name}" not found. Creating a new sheet.')
            try:
                sheet = self.client.create(sheet_name).sheet1
                self.logger.info(f'Created new sheet: {sheet_name}')
                return sheet
            except Exception as e:
                self.logger.error(f'Error creating Google Sheet: {e}')
                raise

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

    def write_data(self, db: Session, data):
        """
        Writes a new row of data to the Google Sheet and the database.
        """
        self.logger.debug('Writing data to Google Sheets and database')
        try:
            # Write to Google Sheets
            self.sheet.append_row(data)
            self.logger.info('Data written to Google Sheets successfully')
        except Exception as e:
            self.logger.error(f'Error writing to Google Sheets: {e}')

        try:
            # Write to database
            report = Report(
                client_name=data[1],
                client_email=data[2],
                industry=data[3],
                pdf_url=data[4],
                doc_url=data[5]
            )
            db.add(report)
            db.commit()
            self.logger.info('Data written to database successfully')
        except Exception as e:
            self.logger.error(f'Error writing data to database: {e}')

    def create_google_doc(self, report_id, content):
        """
        Creates a Google Doc with the report content.
        """
        self.logger.debug('Creating Google Doc for the report')
        try:
            # Create the document
            doc_title = f"AI Insights Report - {report_id}"
            body = {
                'title': doc_title
            }
            doc = self.docs_service.documents().create(body=body).execute()

            # Insert content into the document
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1
                        },
                        'text': content
                    }
                }
            ]
            self.docs_service.documents().batchUpdate(
                documentId=doc.get('documentId'), body={'requests': requests}).execute()

            # Share the document
            self.drive_service.permissions().create(
                fileId=doc.get('documentId'),
                body={'type': 'anyone', 'role': 'reader'}).execute()

            doc_url = f"https://docs.google.com/document/d/{doc.get('documentId')}/edit"
            self.logger.info(f'Document created successfully: {doc_url}')
            return doc_url
        except Exception as e:
            self.logger.error(f'Error creating Google Doc: {e}')
            return None
