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
As an AI consultant specializing in business and entrepreneurship, your task is to create a detailed industry-focused report for the user, showcasing the latest AI trends within the {industry} industry, and demonstrating the benefits of implementing AI in their business. The report should also provide specific examples of AI integrations that would be most beneficial based on the user’s current situation and goals.

### Business Overview:
- **Objectives**: The user's primary business objectives are to {answers[0]}.
- **Current Technology and Data**: The user’s business currently utilizes {answers[1]}.
- **Workforce and Training Needs**: The current skill level of the team is {answers[2]}, which will inform the type of AI training and integration strategies recommended.

### Industry AI Trends:
- **Current AI Trends in {industry}**: Provide an overview of the most relevant and emerging AI trends in the {industry} industry. Discuss how these trends are shaping the industry and influencing business practices.
- **Impact of AI on the Industry**: Explain how AI is currently impacting the {industry} industry, with specific examples of companies or sectors leading the way.

### Benefits of AI Implementation:
- **Strategic Benefits**: Discuss the key benefits of AI implementation for the user's business, aligned with their objectives (e.g., increased efficiency, cost savings, improved customer experience).
- **Case Studies and Examples**: Provide real-world examples or case studies of similar businesses that have successfully integrated AI and the positive outcomes they achieved.

### Tailored AI Integration Examples:
- **Technology Integration**: Recommend specific AI tools or platforms that align with the user’s current technology stack and business goals.
- **Workforce Training**: Suggest tailored training programs or resources to upskill the user's team, considering their current skill level.
- **Potential AI Applications**: List practical AI applications and integrations relevant to the user's business, such as predictive analytics, chatbots, or automation tools, with a brief description of how each could benefit their operations.

### Conclusion and Recommendations:
- **Summary of AI Opportunities**: Summarize the most promising AI opportunities for the user's business based on the industry trends and their specific situation.
- **Next Steps**: Provide actionable recommendations for moving forward with AI integration, including any immediate steps the user should take to begin the process.

- **Additional Resources** (Optional): Suggest further reading, tools, or contacts that could assist the user in their AI integration journey.




        Ensure the report is structured professionally, with clear headings and well-organized content. 

        The report should be in the following format embedded in HTML code with the brackets filled in with the appropriate content:

        ## Format
        ```
<body>
    <header>
        <div class="header-content">
            <p><a href="https://dmotts.github.io/portfolio/">Daley Mottley AI Consulting</a></p>
            <h1>AI Industry-Focused Report</h1>
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
            <h2>Business Overview</h2>
            <p><strong>Objectives:</strong> The user's primary business objectives are to {{ objectives }}.</p>
            <p><strong>Current Technology and Data:</strong> The user’s business currently utilizes {{ technology_and_data }}.</p>
            <p><strong>Workforce and Training Needs:</strong> The current skill level of the team is {{ workforce_training }}.</p>
        </section>

        <section>
            <h2>Industry AI Trends</h2>
            <p><strong>Current AI Trends in {{ industry }}:</strong> {{ industry_ai_trends }}</p>
            <p><strong>Impact of AI on the Industry:</strong> {{ ai_impact }}</p>
        </section>

        <section>
            <h2>Benefits of AI Implementation</h2>
            <p><strong>Strategic Benefits:</strong> {{ strategic_benefits }}</p>
            <p><strong>Case Studies and Examples:</strong> {{ case_studies }}</p>
        </section>

        <section>
            <h2>Tailored AI Integration Examples</h2>
            <p><strong>Technology Integration:</strong> {{ technology_integration }}</p>
            <p><strong>Workforce Training:</strong> {{ tailored_workforce_training }}</p>
            <p><strong>Potential AI Applications:</strong> {{ potential_ai_applications }}</p>
        </section>

        <section>
            <h2>Conclusion and Recommendations</h2>
            <p><strong>Summary of AI Opportunities:</strong> {{ ai_opportunities_summary }}</p>
            <p><strong>Next Steps:</strong> {{ next_steps }}</p>
            <p><strong>Additional Resources:</strong> {{ additional_resources }}</p>
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
