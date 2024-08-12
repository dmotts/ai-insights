from sqlalchemy.orm import Session
from .models import Report
import logging

class DatabaseService:
    def __init__(self, session: Session):
        """
        Initializes the DatabaseService with an SQLAlchemy session.
        """
        self.session = session
        self.logger = logging.getLogger(__name__)

    def save_report_data(self, report_data: dict):
        """
        Saves report data to the database.
        """
        try:
            report = Report(
                report_id=report_data['report_id'],  # Ensure report_id is saved
                client_name=report_data['client_name'],
                client_email=report_data['client_email'],
                industry=report_data['industry'],
                pdf_url=report_data['pdf_url'],
                doc_url=report_data['doc_url'],
                created_at=report_data['created_at']
            )
            self.session.add(report)
            self.session.commit()
            self.logger.info(f"Data written to the database successfully for report ID {report_data['report_id']}")
        except Exception as e:
            self.logger.error(f'Error saving report data to the database: {e}')
            self.session.rollback()  # Rollback in case of an error to avoid a partial commit

    def get_report_by_id(self, report_id: str):
        """
        Retrieves a report from the database by its ID.
        """
        try:
            report = self.session.query(Report).filter_by(report_id=report_id).first()
            if report:
                self.logger.info(f"Report retrieved successfully for ID {report_id}")
            else:
                self.logger.warning(f"No report found for ID {report_id}")
            return report
        except Exception as e:
            self.logger.error(f'Error retrieving report from the database: {e}')
            return None

    def delete_report(self, report_id: str):
        """
        Deletes a report from the database by its ID.
        """
        try:
            report = self.session.query(Report).filter_by(report_id=report_id).first()
            if report:
                self.session.delete(report)
                self.session.commit()
                self.logger.info(f'Report with ID {report_id} deleted successfully')
            else:
                self.logger.warning(f'No report found to delete for ID {report_id}')
        except Exception as e:
            self.logger.error(f'Error deleting report from the database: {e}')
            self.session.rollback()  # Rollback in case of an error
