from openai import OpenAI
import logging

class OpenAIService:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def generate_report_content(self, client_name, report_data):
        prompt = (
            f"Generate a professional and detailed report for the client '{client_name}' with the following data: {report_data}. "
            "Include an introduction, a summary of the data, analysis, and a conclusion."
        )
        self.logger.debug('Generating report content with OpenAI GPT-4o-mini')
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            self.logger.info('Report content generated successfully')
            return response.choices[0].message['content'].strip()
        except Exception as e:
            self.logger.error(f'Error generating report content: {e}')
            return "Error generating report content"
