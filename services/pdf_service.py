import requests
import logging

class PDFService:
    def __init__(self, api_key):
        self.api_key = api_key
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def generate_pdf(self, html_content):
        self.logger.debug('Generating PDF with PDF.co')
        url = "https://api.pdf.co/v1/pdf/convert/from/html"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "html": html_content,
            "name": "report.pdf"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            self.logger.info('PDF generated successfully')
            return result['url']
        except Exception as e:
            self.logger.error(f'Error generating PDF: {e}')
            return None
