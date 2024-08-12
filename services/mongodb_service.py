import logging
from pymongo import MongoClient
from config import Config

class MongoDBService:
    def __init__(self):
        """
        Initializes the MongoDBService with MongoDB client.
        """
        self.logger = logging.getLogger(__name__)

        # Initialize MongoDB client
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.MONGODB_DATABASE_NAME]
        self.collection_name = Config.MONGODB_COLLECTION_NAME
        self.collection = self.db[self.collection_name]

        # Ensure collection is created
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Ensures the collection exists in the database.
        """
        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name)
            self.logger.info(f'Collection {self.collection_name} created successfully')
        else:
            self.logger.info(f'Collection {self.collection_name} already exists')

    def save_report_data(self, report_data: dict):
        """
        Saves report data to MongoDB.
        """
        try:
            self.collection.insert_one(report_data)
            self.logger.info('Data written to MongoDB successfully')
        except Exception as e:
            self.logger.error(f'Error saving report data to MongoDB: {e}')

    def get_report_by_id(self, report_id: str):
        """
        Retrieves a report from MongoDB by its ID.
        """
        try:
            report = self.collection.find_one({"report_id": report_id})
            if report:
                self.logger.info(f"Report retrieved successfully for ID {report_id}")
                return report
            else:
                self.logger.warning(f"No report found for ID {report_id}")
                return None
        except Exception as e:
            self.logger.error(f'Error retrieving report from MongoDB: {e}')
            return None

    def delete_report(self, report_id: str):
        """
        Deletes a report from MongoDB by its ID.
        """
        try:
            result = self.collection.delete_one({"report_id": report_id})
            if result.deleted_count > 0:
                self.logger.info(f'Report with ID {report_id} deleted successfully')
            else:
                self.logger.warning(f'No report found to delete for ID {report_id}')
        except Exception as e:
            self.logger.error(f'Error deleting report from MongoDB: {e}')
