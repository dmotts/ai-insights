import openai
import logging
from typing import List
from cachetools import cached, TTLCache
from config import Config

class OpenAIService:
    def __init__(self, api_key: str, model: str):
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled.')
            return

        openai.api_key = api_key
        self.client = openai
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache results for 5 minutes

    def generate_report_content(self, industry: str, answers: List[str]) -> str:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping report content generation.')
            return "OpenAI service is disabled."

        try:
            # Fetch required data
            industry_trends = self.get_industry_trends(industry)
            benchmark_data = self.get_industry_benchmarks(industry)

            # Construct the prompt
            prompt = self.build_prompt(industry, industry_trends, benchmark_data, answers)

            self.logger.debug('Generating report content with OpenAI')
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            report_content = response.choices[0].message.content
            self.logger.info('Report content generated successfully')
            return report_content
        except Exception as e:
            self.logger.error(f'Error generating report content: {e}')
            return f"Error generating report content: {str(e)}"

    def build_prompt(self, industry: str, industry_trends: str, benchmark_data: str, answers: List[str]) -> str:
        return f"""
        You are an AI consultant preparing a comprehensive report for a business owner in the {industry} industry. The report must be detailed, insightful, and structured into the following sections:

        1. **Introduction**: Provide a brief overview of the business's context based on the industry.
        2. **Industry Trends**: {industry_trends}
        3. **AI Solutions**: Offer AI-driven solutions for the following business needs:
            - Current data management and utilization challenges: {answers[0]}
            - Areas of technology integration and inefficiency: {answers[1]}
            - Long-term business goals and AI's role in achieving them: {answers[2]}
        4. **Analysis and Recommendations**:
            - Include a comparison with industry benchmarks: {benchmark_data}
            - Provide a detailed analysis of how AI can address the specific challenges mentioned.
            - Offer actionable recommendations for AI implementation.
        5. **Conclusion**: Summarize the key insights and recommend next steps.

        Ensure the report is structured professionally, with clear headings and well-organized content. Also, include a call-to-action encouraging the business owner to engage with Daley Mottley AI Consulting for further AI consulting services.
        """

    @cached(cache=lambda self: self.cache)
    def get_industry_trends(self, industry: str) -> str:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping industry trends generation.')
            return "OpenAI service is disabled."

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

    @cached(cache=lambda self: self.cache)
    def get_industry_benchmarks(self, industry: str) -> str:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping industry benchmarks generation.')
            return "OpenAI service is disabled."

        prompt = f"Provide industry benchmarks for the {industry} sector. Include key performance indicators and standard metrics used for comparison."
        self.logger.debug(f'Fetching industry benchmarks for {industry}')
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about industry benchmarks."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            self.logger.info('Industry benchmarks fetched successfully')
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f'Error fetching industry benchmarks: {e}')
            return "Error fetching industry benchmarks"
