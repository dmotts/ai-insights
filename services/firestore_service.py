import logging
import firebase_admin
from firebase_admin import credentials, firestore
from config import Config

class FirestoreService:
    def __init__(self):
        """
        Initializes the FirestoreService with Firestore client.
        """
        self.logger = logging.getLogger(__name__)

        # Initialize Firestore client
        cred = credentials.Certificate(Config.FIRESTORE_CREDENTIALS_JSON)
        firebase_admin.initialize_app(cred, {
            'projectId': Config.FIRESTORE_PROJECT_ID,
        })
        self.db = firestore.client()
        self.collection = self.db.collection('reports')

    def save_report_data(self, report_data: dict):
        """
        Saves report data to Firestore.
        """
        try:
            report_ref = self.collection.document(report_data['report_id'])
            report_ref.set(report_data)
            self.logger.info('Data written to Firestore successfully')
        except Exception as e:
            self.logger.error(f'Error saving report data to Firestore: {e}')

    def get_report_by_id(self, report_id: str):
        """
        Retrieves a report from Firestore by its ID.
        """
        try:
            report_ref = self.collection.document(report_id)
            report = report_ref.get()
            if report.exists:
                self.logger.info(f"Report retrieved successfully for ID {report_id}")
                return report.to_dict()
            else:
                self.logger.warning(f"No report found for ID {report_id}")
                return None
        except Exception as e:
            self.logger.error(f'Error retrieving report from Firestore: {e}')
            return None

    def delete_report(self, report_id: str):
        """
        Deletes a report from Firestore by its ID.
        """
        try:
            report_ref = self.collection.document(report_id)
            report_ref.delete()
            self.logger.info(f'Report with ID {report_id} deleted successfully')
        except Exception as e:
            self.logger.error(f'Error deleting report from Firestore: {e}')
