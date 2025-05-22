from app.ml_models import DentalAIModel
import numpy as np

def test_model():
    try:
        # Inicializa o modelo melhorado
        model = DentalAIModel()
        
        # Dado de teste completo (com todos os features)
        test_data = {
            'age': 30,
            'history': 1,
            'severity': 2,
            'brushing_freq': 2,
            'flossing_freq': 1
        }
        
        # Faz a predição completa
        result = model.predict(test_data)
        print("Teste do modelo completo:")
        print(f"Predição: {result['prediction']}")
        print(f"Probabilidade: {result['probability']:.2f}")
        print(f"Recomendação: {result['recommendation']}")
        print(f"Pontos: {result['reward_points']}")
        
    except Exception as e:
        print(f"Erro no teste do modelo: {str(e)}")

if __name__ == "__main__":
    test_model()