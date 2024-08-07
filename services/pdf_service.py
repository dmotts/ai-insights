import requests
import logging
import matplotlib.pyplot as plt
import io
import base64

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

    def generate_graphs(self):
        self.logger.debug('Generating graphs')
        try:
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph1 = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

            fig, ax = plt.subplots()
            ax.bar([1, 2, 3, 4], [1, 4, 2, 3])
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
