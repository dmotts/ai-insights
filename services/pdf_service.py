import logging
import pdfkit  # For generating PDF from HTML

class PDFService:
    def __init__(self):
        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_pdf(self, html_content, output_path):
        """
        Generates a PDF from the provided HTML content and saves it to the output_path.
        """
        self.logger.debug(f'Generating PDF at {output_path}')
        try:
            # Generate PDF from HTML content and save to the specified output path
            pdfkit.from_string(html_content, output_path)
            self.logger.info(f'PDF generated and saved to: {output_path}')
            return output_path
        except Exception as e:
            self.logger.error(f'Error generating PDF: {e}', exc_info=True)
            return None