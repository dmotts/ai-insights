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
        user_name = user_name.capitalize()

        # Generate content based on the flag (real or mock)
        if not self.client:
            logger.info('LLM API usage is disabled. Returning mock report content.')
            content_sections = self.generate_mock_content(industry, answers)
        else:
            try:
                prompt = self.build_prompt(industry, answers, user_name)
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
                content_sections = self.extract_content_sections(report_content)
            except Exception as e:
                logger.error(f'Error generating report content: {e}', exc_info=True)
                return ""

        # Inject the content into the HTML template
        return self.generate_final_report(content_sections, user_name)

    def build_prompt(self, industry: str, answers: List[str], user_name: str) -> str:
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
                <div class="header-content">
                    <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a></p>
                    <h1>AI Insights Report</h1>
                    <h2>Prepared for</h2>
                    <h3>{user_name}</h3>
                </div>
            </header>

            <div class="container">
                <section>
                    <h2><i class="fas fa-lightbulb"></i> Introduction</h2>
                    <p>{{ introduction }}</p>
                </section>

                <section>
                    <h2><i class="fas fa-chart-line"></i> Industry Trends</h2>
                    <p>{{ industry_trends }}</p>
                </section>

                <section>
                    <h2><i class="fas fa-cogs"></i> Analysis & Recommendations</h2>
                    <p>{{ analysis }}</p>
                </section>

                <section>
                    <h2><i class="fas fa-flag-checkered"></i> Conclusion</h2>
                    <p>{{ conclusion }}</p>
                </section>

                <section class="cta">
                    <h2>Ready to Implement AI in Your Business?</h2>
                    <p>Contact <a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> for expert guidance on how AI can transform your business. Let us help you stay ahead of the competition with cutting-edge AI solutions.</p>
                    <a href="https://dmotts.github.io/portfolio/" class="cta-btn">Learn More</a>
                </section>
            </div>

            <footer>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> | All Rights Reserved &copy; {self.util.get_current_year()}</p>
            </footer>
        </body>
        ```       
        """

    def extract_content_sections(self, content: str) -> dict:
        """
        Extracts content sections from the LLM response.
        Assumes the content is structured with placeholders for sections like {{ introduction }}.
        """
        sections = {
            'introduction': self.extract_between(content, '{{ introduction }}', '{{ industry_trends }}'),
            'industry_trends': self.extract_between(content, '{{ industry_trends }}', '{{ analysis }}'),
            'analysis': self.extract_between(content, '{{ analysis }}', '{{ conclusion }}'),
            'conclusion': self.extract_between(content, '{{ conclusion }}', '</body>')
        }
        return sections

    def extract_between(self, content: str, start_marker: str, end_marker: str) -> str:
        start = content.find(start_marker)
        end = content.find(end_marker)
        if start == -1 or end == -1:
            return ""
        return content[start + len(start_marker):end].strip()

    def generate_mock_content(self, industry: str, answers: List[str]) -> dict:
        """Generates mock content sections."""
        return {
            'introduction': f"This is a mock introduction for the {industry} industry.",
            'industry_trends': f"Mock trends for the {industry} industry.",
            'analysis': f"Mock solutions based on provided answers: {answers}.",
            'conclusion': "Mock conclusion and next steps."
        }

    def generate_final_report(self, content_sections: dict, user_name: str) -> str:
        """Generates the final HTML report by injecting content into the template."""
        styles = self.get_styles()
        html_template = f"""
        <html><head>{styles}</head><body>
            <header>
                <div class="header-content">
                    <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a></p>
                    <h1>AI Insights Report</h1>
                    <h2>Prepared for</h2>
                    <h3>{user_name}</h3>
                </div>
            </header>

            <div class="container">
                <section>
                    <h2><i class="fas fa-lightbulb"></i> Introduction</h2>
                    <p>{content_sections['introduction']}</p>
                </section>

                <section>
                    <h2><i class="fas fa-chart-line"></i> Industry Trends</h2>
                    <p>{content_sections['industry_trends']}</p>
                </section>

                <section>
                    <h2><i class="fas fa-cogs"></i> Analysis & Recommendations</h2>
                    <p>{content_sections['analysis']}</p>
                </section>

                <section>
                    <h2><i class="fas fa-flag-checkered"></i> Conclusion</h2>
                    <p>{content_sections['conclusion']}</p>
                </section>

                <section class="cta">
                    <h2>Ready to Implement AI in Your Business?</h2>
                    <p>Contact <a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> for expert guidance on how AI can transform your business. Let us help you stay ahead of the competition with cutting-edge AI solutions.</p>
                    <a href="https://dmotts.github.io/portfolio/" class="cta-btn">Learn More</a>
                </section>
            </div>

            <footer>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> | All Rights Reserved &copy; {self.util.get_current_year()}</p>
            </footer>
        </body></html>
        """
        return html_template

    def get_styles(self) -> str:
        """Returns the CSS styles."""
        return """
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
                color: #7a26b1;
                text-decoration: none;
            }
            a:hover {
                color: #4a9ddf;
            }
            .container {
                padding: 40px;
                margin: auto;
                max-width: 900px;
                background: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }
            header {
                background: linear-gradient(135deg, #7a26b1, #9e46d0);
                color: #fff;
                padding: 40px 0;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .header-content {
                width: 85%;
                margin: 0 auto;
            }
            header p {
                font-size: 1.2rem;
                margin: 0;
                padding-bottom: 10px;
            }
            header h1 {
                font-size: 2.5rem;
                margin: 0;
                padding-bottom: 10px;
                color: #fff;
            }
            header h2 {
                font-size: 1.5rem;
                margin: 0;
                padding-bottom: 5px;
                font-weight: normal;
                color: #ddd;
            }
            header h3 {
                font-size: 1.2rem;
                margin: 0;
                font-weight: normal;
                color: #fff;
                font-style: italic;
            }
            .section {
                border-bottom: 1px solid #e2e2e2;
                padding-bottom: 20px;
                margin-bottom: 20px;
            }
            h2 {
                color: #7a26b1;
                font-size: 1.8rem;
                margin-bottom: 10px;
                padding-bottom: 5px;
                border-bottom: 2px solid #7a26b1;
                display: flex;
                align-items: center;
            }
            h2 i {
                margin-right: 10px;
            }
            .section p {
                font-size: 1.1rem;
                margin: 10px 0;
                text-align: justify;
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
                background: linear-gradient(135deg, #7a26b1, #9e46d0);
                color: #fff;
                border-radius: 0 0 10px 10px;
            }
            footer p {
                margin: 0;
                font-size: 1rem;
            }
        </style>
        """
