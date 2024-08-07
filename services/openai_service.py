import openai
import logging

class OpenAIService:
    def __init__(self, api_key, model):
        openai.api_key = api_key
        self.model = model
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def generate_report_content(self, answers):
        prompt = f"""
        Generate a comprehensive AI Insights Report for a business owner. The report should provide detailed insights on how AI can improve their business based on the following responses:
        1. {answers[0]}
        2. {answers[1]}
        3. {answers[2]}
        4. {answers[3]}
        5. {answers[4]}

        The report should include:
        - An introduction explaining the purpose of the report and the potential of AI in business optimization.
        - A summary of the business processes and challenges based on the provided answers.
        - An in-depth analysis of how AI can address these challenges and optimize processes.
        - A conclusion summarizing the key insights and recommendations for implementing AI solutions.
        """
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        return response.choices[0].message['content'].strip()
