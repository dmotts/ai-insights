import logging
import os
import requests  # For downloading PDF from URL
import pdfkit  # For generating PDF from HTML
from config import Config

class PDFService:
    def __init__(self, api_key=None):
        # Initialize logger
        if not Config.ENABLE_PDF_SERVICE:
            logging.info('PDF service is disabled.')
            return

        self.logger = logging.getLogger(__name__)
        self.api_key = api_key  # Optional API key if needed for external services

    def generate_pdf(self, html_content, output_path='ai-insights-report.pdf'):
        if not Config.ENABLE_PDF_SERVICE:
            logging.info('PDF service is disabled. Skipping PDF generation.')
            return None

        self.logger.debug(f'Generating PDF locally with pdfkit at {output_path}')
        try:
            # Generate PDF from HTML content and save to the specified output path
            pdfkit.from_string(html_content, output_path)
            self.logger.info(f'PDF generated and saved to: {output_path}')
            return output_path
        except OSError as e:
            self.logger.error(f'Error generating PDF: {e}')
        except Exception as e:
            self.logger.error(f'Unexpected error generating PDF: {e}')
        return None

    def download_pdf(self, pdf_url, output_path):
        """
        Downloads a PDF from a URL and saves it to the specified output path.
        """
        self.logger.info(f'Downloading PDF from {pdf_url} to {output_path}')
        
        try:
            # Send a GET request to fetch the PDF from the given URL
            response = requests.get(pdf_url, stream=True)
            
            # Raise an exception if the response status code is not OK (200)
            response.raise_for_status()

            # Write the content of the PDF to the output_path
            with open(output_path, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # Filter out keep-alive chunks
                        pdf_file.write(chunk)
            
            self.logger.info(f'PDF downloaded and saved to: {output_path}')
            return output_path
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error downloading PDF from {pdf_url}: {e}')
            return None
        except Exception as e:
            self.logger.error(f'Unexpected error while downloading PDF: {e}')
            return None

    def check_pdf_exists(self, output_path):
        """
        Checks if a PDF exists at the given output path.
        """
        self.logger.info(f'Checking for PDF at: {output_path}')
        if os.path.exists(output_path):
            self.logger.info(f'PDF available at: {output_path}')
            return output_path
        else:
            self.logger.error(f'PDF not found at {output_path}')
            return None