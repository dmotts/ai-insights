import logging
from typing import List
from services.utilities_service import UtilitiesService  
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, client=None, model=None):
        self.client = client
        self.model = model
        self.util = UtilitiesService()

    def generate_report_content(self, industry: str, answers: List[str], user_name: str) -> str:
        # Capitalize the user's name
        user_name = user_name.capitalize()

        if not self.client:
            logger.info('LLM API usage is disabled. Returning mock report content.')
            return self.generate_mock_report(industry, answers, user_name)

        try:
            prompt = self.build_prompt(industry, answers)
            logger.debug('Generating report content with LLM API')

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "You are a helpful assistant."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=1500)
            report_content = response.choices[0].message.content

            logger.info('Report content generated successfully')
            html_body_content = self.extract_html(report_content)
            logger.info('HTML content extracted from the response')
            styled_html_content = self.inject_styles(html_body_content, user_name)
            return styled_html_content
        except Exception as e:
            logger.error(f'Error generating report content: {e}', exc_info=True)
            return ""

    def inject_styles(self, html_content: str, user_name: str) -> str:
        """Injects CSS styles and user's name into the HTML content."""
        styles = """
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }

            a {
                color: inherit;
                text-decoration: none;
            }

            .container {
                width: 80%;
                margin: auto;
                background: #fff;
                padding: 40px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }

            header {
                background-color: #7a26b1;
                color: #fff;
                padding: 20px 0;
                text-align: center;
                border-radius: 10px 10px 0 0;
                position: relative;
            }

            header h1 {
                font-size: 2.5rem;
                margin: 0;
                padding: 0;
            }

            header h2 {
                font-size: 1.5rem;
                margin: 0;
                padding: 0;
                font-weight: 300;
            }

            section {
                margin: 20px 0;
            }

            h2 {
                color: #7a26b1;
                font-size: 1.8rem;
                margin-bottom: 10px;
            }

            p {
                font-size: 1.1rem;
                margin: 10px 0;
            }

            .cta {
                margin: 40px 0;
                padding: 20px;
                background-color: #f0effd;
                text-align: center;
                border: 2px solid #7a26b1;
                border-radius: 10px;
            }

            .cta a.cta-btn {
                color: #fff;
                background-color: #7a26b1;
                padding: 10px 20px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 5px;
                display: inline-block;
                transition: background-color 0.3s ease;
            }

            .cta a:hover {
                background-color: #45a049;
            }

            footer {
                text-align: center;
                margin-top: 20px;
                padding: 20px 0;
                background-color: #333;
                color: #fff;
                border-radius: 0 0 10px 10px;
            }

            footer p {
                margin: 0;
                font-size: 1rem;
            }
        </style>
        """
        return f"""
        <html><head>{styles}</head><body>
            <header>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a></p>
                <h1>{user_name}'s AI Insights Report</h1>
            </header>
            {html_content}
        </body></html>
        """

    def build_prompt(self, industry: str, answers: List[str]) -> str:
        return f"""
        You are an AI consultant preparing a comprehensive report for a business owner in the {industry} industry. The report must be detailed, insightful, and structured into the following sections:

        1. **Introduction**: Provide a brief overview of the business's context based on the industry.
        2. **Industry Trends**: Provide the latest AI trends in the {industry} industry.

        3. **Analysis and Recommendations**:
            - Current data management and utilization challenges: {answers[0]}
            - Areas of technology integration and inefficiency: {answers[1]}
            - Long-term business goals and AI's role in achieving them: {answers[2]}
            - Include a detailed analysis of how AI can address the specific challenges mentioned.
            - Offer actionable recommendations for AI implementation.
        5. **Conclusion**: Summarize the key insights and recommend next steps.

        Ensure the report is structured professionally, with clear headings and well-organized content. Also, include a call-to-action encouraging the business owner to engage with Daley Mottley AI Consulting for further AI consulting services.

        The report should be in the following format embedded in HTML code with the brackets filled in with the appropriate content:

        ## Format
        ```
        <body>
            <header>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a></p>
                <h1>AI Insights Report</h1>
            </header>

            <div class="container">
                <section>
                    <h2>Introduction</h2>
                    <p>{{ introduction }}</p>
                </section>

                <section>
                    <h2>Industry Trends</h2>
                    <p>{{ industry_trends }}</p>
                </section>
                <section>
                    <h2>Analysis & Recommendations</h2>
                    <p>{{ analysis }}</p>
                </section>

                <section>
                    <h2>Conclusion</h2>
                    <p>{{ conclusion }}</p>
                </section>

                <section class="cta">
                    <h2>Ready to Implement AI in Your Business?</h2>
                    <p>Contact <a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> for expert guidance on how AI can transform your business. Let us help you stay ahead of the competition with cutting-edge AI solutions.</p>
                    <a href="https://dmotts.github.io/portfolio/" class="cta-btn">Get Started</a>
                </section>
            </div>

            <footer>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> | All Rights Reserved &copy; { self.util.get_current_year() }</p>
            </footer>
        </body>
        ```
        """
        """

    def extract_html(self, content: str) -> str:
        """
        Extracts HTML content from the LLM response.
        Assumes the content is wrapped in a ```html block.
        """
        start = content.find("<body>")
        end = content.find("</body>") + len("</body>")
        if start == -1 or end == -1:
            logger.error("HTML content not found in the response")
            return content  # Fallback to returning the whole content
        return content[start:end]

    def generate_mock_report(self, industry: str, answers: List[str], user_name: str) -> str:
        """Generates a mock report for testing without using the LLM API."""
        mock_content = f"""
        <body>
            <header>
                <p>Daley Mottley AI Consulting</p>
                <h1>{user_name}'s AI Insights Report - Mock</h1>
            </header>

            <div class="container">
                <section>
                    <h2>Introduction</h2>
                    <p>This is a mock introduction for the {industry} industry.</p>
                </section>

                <section>
                    <h2>Industry Trends</h2>
                    <p>Mock trends for the {industry} industry.</p>
                </section>

                <section>
                    <h2>AI Solutions</h2>
                    <p>Mock solutions based on provided answers: {answers}.</p>
                </section>

                <section>
                    <h2>Analysis</h2>
                    <p>Mock analysis and recommendations.</p>
                </section>

                <section>
                    <h2>Conclusion</h2>
                    <p>Mock conclusion and next steps.</p>
                </section>

                <section class="cta">
                    <h2>Ready to Implement AI in Your Business?</h2>
                    <p>Contact <a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> for expert guidance on how AI can transform your business. Let us help you stay ahead of the competition with cutting-edge AI solutions.</p>
                    <a href="https://dmotts.github.io/portfolio/" class="cta-btn">Get Started</a>
                </section>
            </div>

            <footer>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> | All Rights Reserved &copy; { self.util.get_current_year() }</p>
            </footer>
        </body>
        """
        return self.inject_styles(mock_content, user_name)

