import logging
import requests
from config import Config

class PDFService:
    def __init__(self, api_key):
        if not Config.ENABLE_PDF_SERVICE:
            logging.info('PDF service is disabled.')
            return

        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def generate_pdf(self, html_content):
        if not Config.ENABLE_PDF_SERVICE:
            logging.info('PDF service is disabled. Skipping PDF generation.')
            return None

        self.logger.debug('Generating PDF with PDF.co')
        url = "https://api.pdf.co/v1/pdf/convert/from/html"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "html": html_content,  # The HTML content already includes styles
            "name": "report.pdf"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            if 'url' in result:
                self.logger.info('PDF generated successfully')
                return result['url']
            else:
                self.logger.error(f"Unexpected response format: {result}")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f'HTTP error generating PDF: {e}')
        except Exception as e:
            self.logger.error(f'Error generating PDF: {e}')
        return None
