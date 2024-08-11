import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from sqlalchemy.orm import Session
from .models import Report
import os
import logging
from config import Config

class SheetsService:

    def __init__(self, credentials_json, sheet_name):
        if not Config.ENABLE_SHEETS_SERVICE:
            logging.info('Sheets service is disabled.')
            return

        self.logger = logging.getLogger(__name__)

        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/documents"
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_json, self.scope)
        self.client = gspread.authorize(self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.sheet = self._get_or_create_sheet(sheet_name)
        self.folder_id = self._get_or_create_folder(Config.GOOGLE_DRIVE_FOLDER_NAME)

    def _get_or_create_sheet(self, sheet_name):
        try:
            sheet = self.client.open(sheet_name).sheet1
            self.logger.info(f'Using existing sheet: {sheet_name}')
            return sheet
        except gspread.SpreadsheetNotFound:
            self.logger.info(
                f'Sheet "{sheet_name}" not found. Creating a new sheet.')
            try:
                sheet = self.client.create(sheet_name).sheet1
                self.logger.info(f'Created new sheet: {sheet_name}')
                return sheet
            except Exception as e:
                self.logger.error(f'Error creating Google Sheet: {e}')
                raise

    def _get_or_create_folder(self, folder_name):
        try:
            response = self.drive_service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                spaces='drive'
            ).execute()

            if len(response.get('files', [])) > 0:
                self.logger.info(f'Using existing folder: {folder_name}')
                return response['files'][0]['id']

            # Folder doesn't exist, create it
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive_service.files().create(body=file_metadata, fields='id').execute()
            self.logger.info(f'Created new folder: {folder_name}')
            return folder.get('id')

        except HttpError as error:
            self.logger.error(f'An error occurred while accessing Google Drive: {error}')
            raise

    def save_pdf_to_drive(self, file_path, file_name):
        try:
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id],
                'mimeType': 'application/pdf'
            }
            media = MediaFileUpload(file_path, mimetype='application/pdf')
            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            file_id = file.get('id')
            pdf_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

            # Share the PDF
            self.drive_service.permissions().create(
                fileId=file_id,
                body={
                    'type': 'anyone',
                    'role': 'reader'
                }
            ).execute()

            self.logger.info(f'PDF saved to Google Drive: {pdf_url}')
            return pdf_url
        except Exception as e:
            self.logger.error(f'Error saving PDF to Google Drive: {e}')
            return None

    def create_google_doc(self, report_id, content):
        if not Config.ENABLE_SHEETS_SERVICE:
            logging.info(
                'Sheets service is disabled. Skipping Google Doc creation.')
            return None

        self.logger.debug('Creating Google Doc for the report')
        try:
            # Create the document
            doc_title = f"AI Insights Report - {report_id}"
            body = {'title': doc_title}
            doc = self.docs_service.documents().create(body=body).execute()

            # Insert content into the document
            requests = [{
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': content
                }
            }]
            self.docs_service.documents().batchUpdate(
                documentId=doc.get('documentId'), body={
                    'requests': requests
                }).execute()

            # Share the document
            self.drive_service.permissions().create(
                fileId=doc.get('documentId'),
                body={
                    'type': 'anyone',
                    'role': 'reader'
                }
            ).execute()

            doc_url = f"https://docs.google.com/document/d/{doc.get('documentId')}/edit"
            self.logger.info(f'Document created successfully: {doc_url}')
            return doc_url
        except Exception as e:
            self.logger.error(f'Error creating Google Doc: {e}')
            return None

    def write_data(self, db: Session, data):
        try:
            # Write to Google Sheets
            self.sheet.append_row(list(data.values()))
            self.logger.info('Data written to Google Sheets successfully')

            if Config.ENABLE_DATABASE:
                # Write to database
                report = Report(
                    client_name=data['client_name'],
                    client_email=data['client_email'],
                    industry=data['industry'],
                    pdf_url=data['pdf_url'],
                    doc_url=data['doc_url']
                )
                db.add(report)
                db.commit()
                self.logger.info('Data written to database successfully')

        except Exception as e:
            self.logger.error(f'Error writing data: {e}')
