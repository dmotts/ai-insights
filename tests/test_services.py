import pytest
from services.openai_service import OpenAIService
from services.pdf_service import PDFService

@pytest.fixture
def openai_service():
    return OpenAIService(api_key='test_key', model='gpt-3.5-turbo')

@pytest.fixture
def pdf_service():
    return PDFService(api_key='test_pdfco_key')

def test_generate_report_content(openai_service, requests_mock):
    industry = "Technology"
    answers = ["Optimizing processes", "Improving UX", "Data analysis", "Automation", "AI in future growth", "Initial Exploration"]
    
    # Mock the OpenAI API response
    requests_mock.post('https://api.openai.com/v1/completions', json={
        'choices': [{'text': 'AI Insights Report Content'}]
    })
    
    include_sections = {
        "introduction": True,
        "industry_trends": True,
        "ai_solutions": True,
        "analysis": True,
        "conclusion": True
    }
    
    content = openai_service.generate_report_content(industry, answers, include_sections)
    assert "AI Insights Report" in content

def test_generate_report_content_caching(openai_service, requests_mock):
    industry = "Technology"
    answers = ["Optimizing processes", "Improving UX", "Data analysis", "Automation", "AI in future growth", "Initial Exploration"]
    
    # Mock the OpenAI API response
    requests_mock.post('https://api.openai.com/v1/completions', json={
        'choices': [{'text': 'AI Insights Report Content'}]
    })
    
    include_sections = {
        "introduction": True,
        "industry_trends": True,
        "ai_solutions": True,
        "analysis": True,
        "conclusion": True
    }
    
    # First call to populate cache
    content_first = openai_service.generate_report_content(industry, answers, include_sections)
    # Second call should use cache
    content_cached = openai_service.generate_report_content(industry, answers, include_sections)
    
    assert content_first == content_cached

def test_generate_graphs(pdf_service):
    analysis_data = {
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 15, 30, 25],
        'categories': ['HR', 'Finance', 'IT', 'Operations', 'Sales'],
        'values': [75, 85, 95, 80, 90]
    }
    graph1, graph2 = pdf_service.generate_graphs(analysis_data)
    assert graph1 is not None
    assert graph2 is not None
