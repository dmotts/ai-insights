import logging
from typing import List
from services.utilities_service import UtilitiesService
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)


class ReportGenerator:

    def __init__(self, client=None, model=None, utilities_service=None):
        self.client = client
        self.model = model
        self.util = utilities_service

    def generate_report_content(self, industry: str, answers: List[str],
                                user_name: str) -> str:
        # Capitalize the user's name
        user_name = user_name.capitalize()

        if not self.client:
            logger.info(
                'LLM API usage is disabled. Returning mock report content.')
            return self.generate_mock_report(industry, answers)

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
            html_body_content = self.extract_html(report_content)
            logger.info('HTML content extracted from the response')
            styled_html_content = self.inject_styles(html_body_content)
            return styled_html_content
        except Exception as e:
            logger.error(f'Error generating report content: {e}',
                         exc_info=True)
            return ""

    def inject_styles(self, html_content: str) -> str:
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
    padding: 40px;
    margin: auto;
    max-width: 900px; /* Reduced width for better readability */
    background: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

header {
    background-color: #7a26b1;
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

header p.subtitle {
    font-size: 1.1rem; 
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
    border-bottom: 1px solid #ddd;
    padding-bottom: 20px;
    margin-bottom: 20px;
}

.section h2 {
    color: #7a26b1;
    font-size: 1.8rem;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 2px solid #7a26b1;
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

.cta h2 {
    color: #7a26b1;    
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
            {html_content}
        </body></html>
        """

    def build_prompt(self, industry: str, answers: List[str],
                     user_name) -> str:
        return f"""
        ### Instruction:
As an AI consultant specializing in business and entrepreneurship, your task is to develop a strategic operational plan for integrating artificial intelligence into the user's business operations within the {industry} industry.

### Business Overview:
- **Objectives**: The primary objectives for AI integration are to {answer[0]}.
- **Current Technology and Data**: The business currently uses {answer[1]}, and AI will need to integrate with these existing systems and data.
- **Workforce and Training Needs**: The team’s skill level is currently at {answer[2]}, and they will require training to effectively use AI.

### Industry Trends:
- **Current Trends in {industry}**: Identify and analyze the latest trends in the {industry} industry that may impact or benefit from AI integration.
- **Opportunities**: Suggest ways in which AI can be used to capitalize on these trends, helping the business stay ahead of the competition.

### Requirements:
1. **Technology Integration**:
   - **Integration Steps**: Detail the steps for integrating AI technologies into existing business processes, considering the current technology stack.
   - **System Compatibility**: Evaluate the compatibility of AI tools with existing systems.
   - **Scalability**: Provide recommendations on how to scale AI solutions as the business grows.

2. **Workforce Training**:
   - **Training Plan**: Outline a comprehensive training plan based on the team’s current skill level and the specific needs identified.
   - **Skill Development**: Recommend areas for skill development to maximize the effectiveness of AI integration.
   - **Continuous Learning**: Suggest methods for ongoing training to keep the workforce up-to-date with AI advancements.

3. **Data Management**:
   - **Data Strategy**: Describe the strategies for managing and utilizing the data available to support AI implementation.
   - **Data Security**: Include considerations for data privacy and security, especially in relation to AI processing.
   - **Compliance**: Ensure that data management practices comply with relevant industry regulations.

4. **Risk and Challenges**:
   - **Risk Identification**: Identify potential risks and challenges that could arise during AI integration.
   - **Preventative Measures**: Propose preventative measures to mitigate these risks.
   - **Contingency Plans**: Develop contingency plans in case these challenges materialize.

### Output Structure:
- **Executive Summary**: Provide a brief overview of the operational plan.
- **Industry Trends**: Analysis of current trends in {industry} and AI-driven opportunities.
- **Technology Integration**: Detailed steps for integrating AI, system compatibility, and scalability.
- **Workforce Training**: Comprehensive training plan, skill development, and continuous learning strategies.
- **Data Management**: Data strategies, security considerations, and compliance measures.
- **Risk and Challenges**: Identification, preventative measures, and contingency plans.
- **Additional Recommendations**: Offer extra insights or suggest emerging technologies that might be relevant to the business.
- **Conclusion**: Summarize the expected impact of AI integration on business operations.


        Ensure the report is structured professionally, with clear headings and well-organized content. 

        The report should be in the following format embedded in HTML code with the brackets filled in with the appropriate content:

        ## Format
        ```
        <body>
    <header>
        <div class="header-content">
            <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a></p>
            <h1>AI Insights Report</h1>
            <p class="sub-title">Prepared for</p>
            <h3>{ user_name }</h3>
        </div>
    </header>

    <div class="container">
        <section>
            <h2>Introduction</h2>
            <p>{{ executive_summary }}</p>
        </section>

        <section>
            <h2>Industry Trends</h2>
            <p>{{ industry_trends }}</p>
        </section>

        <section>
            <h2>Technology Integration</h2>
            <p>{{ technology_integration }}</p>
        </section>

        <section>
            <h2>Workforce Training</h2>
            <p>{{ workforce_training }}</p>
        </section>

        <section>
            <h2>Data Management</h2>
            <p>{{ data_management }}</p>
        </section>

        <section>
            <h2>Risk & Challenges</h2>
            <p>{{ risk_And_challenges }}</p>
        </section>

        <section>
            <h2>Additional Recommendations</h2>
            <p>{{ additional_recommendations }}</p>
        </section>
        
        <section>
            <h2>Conclusion</h2>
            <p>{{ conclusion }}</p>
        </section>

        <section class="cta">
            <h2>Ready to Implement AI in Your Business?</h2>
            <p>Contact <a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> for expert guidance on how AI can transform your business. Let us help you stay ahead of the competition with cutting-edge AI solutions.</p>
            <a href="https://dmotts.github.io/portfolio/" class="cta-btn">Learn More</a>
        </section>
    </div>

    <footer>
        <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> | All Rights Reserved &copy; { self.util.get_current_year() }</p>
    </footer>
</body>
        ```       
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

    def generate_mock_report(self, industry: str, answers: List[str]) -> str:
        """Generates a mock report for testing without using the LLM API."""
        mock_content = f"""
        <body>
            <header>
                <p>Daley Mottley AI Consulting</p>
                <h1>AI Insights Report - Mock</h1>
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
                    <a href="https://dmotts.github.io/portfolio/" class="cta-btn">Learn More</a>
                </section>
            </div>

            <footer>
                <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a> | All Rights Reserved &copy; { self.util.get_current_year() }</p>
            </footer>
        </body>
        """
        return self.inject_styles(mock_content)
