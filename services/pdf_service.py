import logging
import os
import pdfkit  # New dependency
from config import Config

class PDFService:
    def __init__(self, api_key=None):
        if not Config.ENABLE_PDF_SERVICE:
            logging.info('PDF service is disabled.')
            return

        self.logger = logging.getLogger(__name__)

    def generate_pdf(self, html_content, output_path=None):
        if not Config.ENABLE_PDF_SERVICE:
            logging.info('PDF service is disabled. Skipping PDF generation.')
            return None

        if output_path is None:
            # Set a default output path if none is provided
            output_path = '/tmp/ai-insights-report.pdf'

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

    def download_pdf(self, output_path):
        """
        Function preserved for backward compatibility in case future implementations need to download.
        In the current state, we simply reference the locally generated file.
        """
        self.logger.info(f'Checking for PDF at: {output_path}')
        if os.path.exists(output_path):
            self.logger.info(f'PDF available at: {output_path}')
            return output_path
        else:
            self.logger.error(f'PDF not found at {output_path}')
            return None