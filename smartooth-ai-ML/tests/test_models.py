import pytest
from app.ml_models import DentalAIModel
from faker import Faker

fake = Faker()

@pytest.fixture
def ai_model():
    return DentalAIModel()

def test_model_prediction(ai_model):
    test_data = {
        'age': 35,
        'history': 1,
        'severity': 2,
        'brushing_freq': 2,
        'flossing_freq': 1
    }
    result = ai_model.predict(test_data)
    assert 'prediction' in result
    assert 'probability' in result
    assert isinstance(result['prediction'], int)
    assert 0 <= result['probability'] <= 1

def test_reward_calculation(ai_model):
    test_data = {
        'age': 30,
        'history': 0,
        'severity': 1,
        'brushing_freq': 3,  # 3x ao dia = 30 pontos
        'flossing_freq': 1,  # 1x ao dia = 20 pontos
        'regular_checkups': True  # +50 pontos
    }
    assert ai_model.calculate_reward_points(test_data) == 100