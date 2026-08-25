import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Resume ATS Score Checker' in rv.data

def test_analyze_endpoint_exists(client):
    """Test that the analyze endpoint exists"""
    rv = client.post('/analyze', data={
        'resume': (b'test resume content', 'test.txt'),
        'job_description': 'test job description'
    }, content_type='multipart/form-data')
    # We expect either a redirect or a successful response
    assert rv.status_code in [200, 302]