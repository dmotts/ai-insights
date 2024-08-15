import logging
import requests
import os
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
            "name": "ai-insights-report.pdf"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            pdf_url = result.get('url')

            if pdf_url:
                self.logger.info(f'PDF generated successfully: {pdf_url}')
            else:
                self.logger.error(f"Unexpected response format: {result}")

            return pdf_url
        except requests.exceptions.RequestException as e:
            self.logger.error(f'HTTP error generating PDF: {e}')
        except Exception as e:
            self.logger.error(f'Error generating PDF: {e}')
        return None

    def download_pdf(self, pdf_url, output_path):
        if not pdf_url:
            self.logger.error('No URL provided for PDF download.')
            return None

        try:
            self.logger.debug(f'Downloading PDF from: {pdf_url}')
            response = requests.get(pdf_url)
            response.raise_for_status()
            with open(output_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            self.logger.info(f'PDF downloaded and saved to: {output_path}')
            return output_path
        except requests.exceptions.RequestException as e:
            self.logger.error(f'HTTP error downloading PDF: {e}')
            return None
        except Exception as e:
            self.logger.error(f'Error downloading PDF: {e}')
            return None
