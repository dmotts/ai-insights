import requests
import os
import logging

class PDFService:
    def __init__(self, api_key=None):
        self.logger = logging.getLogger(__name__)

    def generate_pdf(self, html_content, output_path='ai-insights-report.pdf'):
        try:
            # Generate PDF using pdfkit or another method and save to output_path
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