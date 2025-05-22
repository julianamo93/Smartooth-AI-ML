import pytest
from app.routes import init_routes
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    init_routes(app)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Smartooth AI" in response.data

def test_predict_route(client):
    test_data = {
        'age': 40,
        'history': 1,
        'severity': 3
    }
    response = client.post('/api/v1/predict', json=test_data)
    assert response.status_code == 200
    assert b'prediction' in response.data