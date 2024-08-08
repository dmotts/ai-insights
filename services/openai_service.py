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

    def generate_report_content(self, industry: str, answers: List[str], include_sections: dict) -> str:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping report content generation.')
            return "OpenAI service is disabled."

        industry_trends = self.get_industry_trends(industry)
        benchmark_data = self.get_industry_benchmarks(industry)
        trend_analysis = self.perform_trend_analysis(industry)
        case_studies = self.get_case_studies(industry)

        prompt = f"""
        You are an AI consultant. Generate a concise and actionable AI Insights Report for a business owner in the {industry} industry. The report should provide detailed insights on how AI can improve their business based on the following responses:

        1. Specific operational processes to improve with AI: {answers[0]}
        2. Key challenges in improving customer experience: {answers[1]}
        3. Current data management and utilization challenges: {answers[2]}
        4. Areas of technology integration and inefficiency: {answers[3]}
        5. Long-term business goals and AI's role in achieving them: {answers[4]}
        6. Current AI maturity level: {answers[5]}

        The report should include:
        """
        if include_sections['introduction']:
            prompt += "- An **Introduction** summarizing the business context.\n"

        if include_sections['industry_trends']:
            prompt += f"- **Latest Trends** in the {industry} industry: {industry_trends}\n"

        if include_sections['ai_solutions']:
            prompt += "- **AI Solutions** for the identified issues.\n"

        if include_sections['analysis']:
            prompt += "- **Detailed Analysis and Recommendations** for implementation.\n"
            prompt += "- Industry benchmarks and case studies related to AI.\n"
            prompt += f"- **Benchmark Comparison**: {benchmark_data}\n"
            prompt += f"- **Trend Analysis**: {trend_analysis}\n"
            prompt += f"- **Case Studies**: {case_studies}\n"

        if include_sections['conclusion']:
            prompt += "- A **Conclusion** summarizing the key insights and action points.\n"

        prompt += """
        Provide a comparison with industry benchmarks where applicable, and suggest potential AI tools or platforms for improvement.
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

    def perform_trend_analysis(self, industry: str) -> str:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping trend analysis.')
            return "OpenAI service is disabled."

        prompt = f"Analyze historical data to identify trends and predict future developments in the {industry} industry."
        self.logger.debug(f'Performing trend analysis for {industry}')
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about trend analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            self.logger.info('Trend analysis performed successfully')
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f'Error performing trend analysis: {e}')
            return "Error performing trend analysis"

    def get_case_studies(self, industry: str) -> str:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping case studies generation.')
            return "OpenAI service is disabled."

        prompt = f"Provide case studies of successful AI implementation in the {industry} industry."
        self.logger.debug(f'Fetching case studies for {industry}')
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about industry-specific case studies."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            self.logger.info('Case studies fetched successfully')
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f'Error fetching case studies: {e}')
            return "Error fetching case studies"
