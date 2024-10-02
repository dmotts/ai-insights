import logging
import os
import pdfkit  # For generating PDF from HTML
from shutil import copyfile

class PDFService:
    def __init__(self):
        # Initialize logger
        self.logger = logging.getLogger(__name__)

    def generate_pdf(self, html_content, output_path='ai-insights-report.pdf'):
        """
        Generates a PDF from the provided HTML content and saves it to the output_path.
        """
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

    def copy_pdf(self, source_path, destination_path):
        """
        Copies the PDF from the source path to the destination path.
        """
        self.logger.info(f'Copying PDF from {source_path} to {destination_path}')
        try:
            # Copy the PDF to the destination
            copyfile(source_path, destination_path)
            self.logger.info(f'PDF copied successfully to: {destination_path}')
            return destination_path
        except FileNotFoundError:
            self.logger.error(f'File not found: {source_path}')
            return None
        except Exception as e:
            self.logger.error(f'Error copying PDF: {e}')
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