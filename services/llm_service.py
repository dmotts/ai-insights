import logging
from cachetools import cached, TTLCache
from config import Config
from services.report_generator import ReportGenerator  # Import the ReportGenerator

class LLMService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if Config.USE_OPENAI_API:
            self.openai_api_key = Config.OPENAI_API_KEY
            self.model = Config.LLM_MODEL
            self.client = OpenAI(api_key=self.openai_api_key)
        else:
            logging.info('LLM service is disabled.')
            self.client = None
            self.model = None

        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache results for 5 minutes
        self.report_generator = ReportGenerator(self.client, self.model)  # Instantiate ReportGenerator

    def generate_report_content(self, industry: str, answers: List[str], user_name: str) -> str:
        """Delegate report generation to the ReportGenerator."""
        return self.report_generator.generate_report_content(industry, answers, user_name)
