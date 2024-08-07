import openai
import logging

class OpenAIService:
    def __init__(self, api_key, model):
        openai.api_key = api_key
        self.client = openai
        self.model = model
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def get_industry_trends(self, industry):
        prompt = f"Provide the latest AI trends and developments in the {industry} industry."
        self.logger.debug(f'Fetching industry trends for {industry}')
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about AI trends."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            self.logger.info('Industry trends fetched successfully')
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f'Error fetching industry trends: {e}')
            return "Error fetching industry trends"

    def generate_report_content(self, industry, answers):
        industry_trends = self.get_industry_trends(industry)
        prompt = f"""
        You are an AI consultant. Generate a concise and actionable AI Insights Report for a business owner in the {industry} industry. The report should provide detailed insights on how AI can improve their business based on the following responses:
    
        1. Key processes to optimize: {answers[0]}
        2. Challenges in improving customer experience: {answers[1]}
        3. Current data utilization: {answers[2]}
        4. Areas of operational inefficiency: {answers[3]}
        5. Long-term business goals and role of technology: {answers[4]}
    
        The report should include:
        - An **Introduction** summarizing the business context.
        - **Latest Trends** in the {industry} industry: {industry_trends}
        - **AI Solutions** for the identified issues.
        - **Detailed Analysis and Recommendations** for implementation.
        - Graphs and forecasts where applicable.
        - A **Conclusion** summarizing the key insights and action points.
        """
        self.logger.debug('Generating report content with OpenAI')
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            self.logger.info('Report content generated successfully')
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f'Error generating report content: {e}')
            return "Error generating report content"
    