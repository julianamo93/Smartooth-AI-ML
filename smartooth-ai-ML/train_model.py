import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class DentalAIModel:
    def __init__(self):
        self.model = None
        self.model_path = "smartooth-ai-ML/app/model/dental_model.joblib"
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def train(self, X, y):
        self.model = RandomForestClassifier()
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)
        print(f"Modelo salvo em: {self.model_path}")

def main():
    print("Treinando modelo...")
    
    # Exemplo de dados simples (substitua pelos seus reais, se tiver)
    data = {
        'age': [25, 30, 35, 40, 45, 50],
        'brushing_freq': [2, 3, 1, 2, 2, 3],
        'flossing_freq': [1, 1, 0, 1, 0, 1],
        'treatment_needed': [1, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    
    X = df[['age', 'brushing_freq', 'flossing_freq']]
    y = df['treatment_needed']

    model = DentalAIModel()
    model.train(X, y)

if __name__ == "__main__":
    main()
