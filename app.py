from flask import Flask, request, jsonify, render_template
import logging
import datetime
from services.sheets_service import SheetsService
from services.openai_service import OpenAIService
from services.pdf_service import PDFService
from services.email_service import EmailService
from config import Config
from sqlalchemy.orm import Session
from services.models import engine
from werkzeug.exceptions import HTTPException
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config.from_object(Config)

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize services
sheets_service = SheetsService(app.config['GOOGLE_SHEETS_CREDENTIALS_JSON'], app.config['SHEET_NAME'])
openai_service = OpenAIService(app.config['OPENAI_API_KEY'], app.config['OPENAI_MODEL'])
pdf_service = PDFService(app.config['PDFCO_API_KEY'])
email_service = EmailService()

class ReportRequestSchema(Schema):
    client_name = fields.String(required=True)
    client_email = fields.Email(required=True)
    industry = fields.String(required=True)
    question1 = fields.String(required=True)
    question2 = fields.String(required=True)
    question3 = fields.String(required=True)
    question4 = fields.String(required=True)
    question5 = fields.String(required=True)
    question6 = fields.String(required=True)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    logger.error(f"HTTP error occurred: {e}")
    return jsonify({"status": "error", "message": e.description}), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error occurred: {e}")
    return jsonify({"status": "error", "message": "An internal error occurred"}), 500

@app.route('/')
def index():
    return render_template('generate_report.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # Validate and deserialize input
        data = request.json
        schema = ReportRequestSchema()
        validated_data = schema.load(data)

        industry = validated_data.get('industry')
        answers = [
            validated_data.get('question1'),
            validated_data.get('question2'),
            validated_data.get('question3'),
            validated_data.get('question4'),
            validated_data.get('question5'),
            validated_data.get('question6')
        ]

        # Get customization options
        include_sections = {
            "introduction": data.get('includeIntroduction', True),
            "industry_trends": data.get('includeIndustryTrends', True),
            "ai_solutions": data.get('includeAISolutions', True),
            "analysis": data.get('includeAnalysis', True),
            "conclusion": data.get('includeConclusion', True)
        }

        # Generate report content
        report_content = openai_service.generate_report_content(industry, answers, include_sections)

        # Safely split the generated content into sections
        sections = report_content.split('\n\n')
        content_dict = {
            'introduction': sections[0] if len(sections) > 0 and include_sections['introduction'] else "Introduction section is unavailable.",
            'industry_trends': sections[1] if len(sections) > 1 and include_sections['industry_trends'] else "Industry trends section is unavailable.",
            'ai_solutions': sections[2] if len(sections) > 2 and include_sections['ai_solutions'] else "AI solutions section is unavailable.",
            'analysis': sections[3] if len(sections) > 3 and include_sections['analysis'] else "Analysis section is unavailable.",
            'conclusion': sections[4] if len(sections) > 4 and include_sections['conclusion'] else "Conclusion section is unavailable."
        }

        # Generate graphs with analysis data
        analysis_data = {
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 30, 25],
            'categories': ['HR', 'Finance', 'IT', 'Operations', 'Sales'],
            'values': [75, 85, 95, 80, 90]
        }
        graph1, graph2 = pdf_service.generate_graphs(analysis_data)
        content_dict['graph1'] = graph1
        content_dict['graph2'] = graph2

        html_content = render_template('report_template.html', **content_dict)

        # Generate PDF using PDF.co
        pdf_url = pdf_service.generate_pdf(html_content)

        if not pdf_url:
            return jsonify({"status": "error", "message": "Failed to generate PDF"}), 500

        # Create a Google Doc for the report
        report_id = generate_report_id()
        doc_url = sheets_service.create_google_doc(report_id, report_content)

        if not doc_url:
            return jsonify({"status": "error", "message": "Failed to create Google Doc"}), 500

        # Write report data to Google Sheets and Database
        report_data = [
            report_id,
            validated_data['client_name'],
            validated_data['client_email'],
            industry,
            pdf_url,
            doc_url,
            datetime.datetime.now().isoformat()
        ]

        with Session(engine) as db:
            sheets_service.write_data(db, report_data)

      #  email_service.send_email(
      #      validated_data['client_email'],
      #      "Your AI Insights Report is Ready",
       #     f"Your report has been generated. You can download it from the following links:\n\nPDF: {pdf_url}\nGoogle Doc: {doc_url}"
        #)

        # Schedule follow-up email (for demonstration, replace with actual scheduling)
        # email_service.send_follow_up_email(validated_data['client_email'], report_id)

        logger.info(f'Report generated with ID: {report_id}')
        return jsonify({"status": "success", "report_id": report_id, "pdf_url": pdf_url, "doc_url": doc_url})
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({"status": "error", "message": "Validation error", "details": err.messages}), 400
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({"status": "error", "message": "An error occurred while generating the report."}), 500

@app.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    try:
        all_reports = sheets_service.read_data()
        report = next((report for report in all_reports if report['Report ID'] == report_id), None)

        if report:
            logger.info(f'Report found: {report_id}')
            return jsonify(report)
        else:
            logger.warning(f'Report not found: {report_id}')
            return jsonify({"status": "error", "message": "Report not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving report: {e}")
        return jsonify({"status": "error", "message": "An error occurred while retrieving the report."}), 500

def generate_report_id():
    return str(int(datetime.datetime.now().timestamp()))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
