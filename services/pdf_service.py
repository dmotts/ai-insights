import matplotlib.pyplot as plt
import io
import base64
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
            self.logger.info('PDF service is disabled. Skipping PDF generation.')
            return None

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
        except requests.exceptions.RequestException as e:
            self.logger.error(f'HTTP error generating PDF: {e}')
        except Exception as e:
            self.logger.error(f'Error generating PDF: {e}')
        return None

    def generate_graphs(self, analysis_data):
        if not Config.ENABLE_PDF_SERVICE:
            self.logger.info('PDF service is disabled. Skipping graph generation.')
            return None, None

        self.logger.debug('Generating graphs')
        try:
            # Example graph 1
            fig, ax = plt.subplots()
            ax.plot(analysis_data['x'], analysis_data['y'], marker='o')
            ax.set_title('AI Implementation Efficiency Over Time')
            ax.set_xlabel('Time (months)')
            ax.set_ylabel('Efficiency Improvement (%)')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph1 = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

            # Example graph 2
            fig, ax = plt.subplots()
            ax.bar(analysis_data['categories'], analysis_data['values'])
            ax.set_title('Operational Efficiency Scores by Department')
            ax.set_xlabel('Departments')
            ax.set_ylabel('Efficiency Score')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph2 = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

            self.logger.info('Graphs generated successfully')
            return f"data:image/png;base64,{graph1}", f"data:image/png;base64,{graph2}"
        except Exception as e:
            self.logger.error(f'Error generating graphs: {e}')
            return None, None
