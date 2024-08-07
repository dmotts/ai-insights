import pytest
from app import app as flask_app
from sqlalchemy.orm import Session
from services.models import engine, Report

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_generate_report_endpoint(client, db, requests_mock):
    # Mock the OpenAI API response
    requests_mock.post('https://api.openai.com/v1/completions', json={
        'choices': [{'text': 'AI Insights Report Content'}]
    })
    # Mock the PDF.co API response
    requests_mock.post('https://api.pdf.co/v1/pdf/convert/from/html', json={
        'url': 'https://example.com/test.pdf'
    })

    response = client.post('/generate_report', json={
        'client_name': 'John Doe',
        'client_email': 'john.doe@example.com',
        'industry': 'Technology',
        'question1': 'Optimizing processes',
        'question2': 'Improving UX',
        'question3': 'Data analysis',
        'question4': 'Automation',
        'question5': 'AI in future growth'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'pdf_url' in data
    assert 'doc_url' in data

    report = db.query(Report).filter_by(client_email='john.doe@example.com').first()
    assert report is not None
