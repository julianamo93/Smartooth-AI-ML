import joblib
import numpy as np
import pandas as pd
import os
from typing import Dict, List, Tuple
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from config import Config

class DentalAIModel:
    def __init__(self):
        self.model = None
        self.model_path = "smartooth-ai-ML/app/model/dental_model.joblib"
        # self.load_model()  # deixe comentado por enquanto

    def load_model(self):
        try:
            self.model = joblib.load(self.model_path)
            print("Modelo carregado com sucesso.")
        except Exception as e:
            raise RuntimeError(f"Falha ao carregar modelo: {str(e)}")
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Valida a estrutura dos dados de treinamento"""
        required_columns = {'age', 'history', 'severity', 'brushing_freq', 'flossing_freq', 'treatment_needed'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Colunas obrigatórias faltando: {missing}")
        return True
    
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Pré-processa os dados para treinamento"""
        try:
            self.validate_data(df)
            
            # Converter dados categóricos se necessário
            df['history'] = df['history'].astype(int)
            df['treatment_needed'] = df['treatment_needed'].astype(int)
            
            # Selecionar features e target
            X = df[['age', 'history', 'severity', 'brushing_freq', 'flossing_freq']]
            y = df['treatment_needed']
            
            return X, y
            
        except Exception as e:
            raise ValueError(f"Erro no pré-processamento: {str(e)}")
    
    def train_model(self) -> None:
        """Treina e avalia um novo modelo, salvando-o para uso futuro"""
        try:
            # Carregar e preparar dados
            df = pd.read_csv(self.data_path)
            X, y = self.preprocess_data(df)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=0.2, 
                random_state=42,
                stratify=y
            )
            
            # Configurar e treinar modelo
            self.model = GradientBoostingClassifier(
                n_estimators=self.config.MODEL_N_ESTIMATORS,
                learning_rate=self.config.MODEL_LEARNING_RATE,
                max_depth=self.config.MODEL_MAX_DEPTH,
                random_state=42,
                min_samples_split=10,
                min_samples_leaf=5
            )
            
            self.model.fit(X_train, y_train)
            
            # Avaliação detalhada
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print("\n" + "="*50)
            print(f"Acurácia do modelo: {accuracy:.2f}")
            print("Relatório de Classificação:")
            print(classification_report(y_test, y_pred))
            print("="*50 + "\n")
            
            # Salvar modelo
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            print(f"Modelo salvo em: {self.model_path}")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de dados não encontrado em: {self.data_path}")
        except Exception as e:
            raise RuntimeError(f"Erro durante o treinamento: {str(e)}")
    
    def validate_input(self, input_data: Dict) -> bool:
        """Valida os dados de entrada para predição"""
        required = {'age', 'history', 'severity'}
        if not all(field in input_data for field in required):
            missing = required - set(input_data.keys())
            raise ValueError(f"Campos obrigatórios faltando: {missing}")
        
        if not isinstance(input_data['age'], (int, float)) or input_data['age'] <= 0:
            raise ValueError("Idade deve ser um número positivo")
        
        return True
    
    def predict(self, input_data: Dict) -> Dict:
        """
        Faz previsão com dados de entrada
        
        Args:
            input_data: Dicionário contendo:
                - age: Idade do paciente (int)
                - history: Histórico de problemas (0 ou 1)
                - severity: Severidade atual (1-3)
                - brushing_freq: Frequência de escovação (opcional)
                - flossing_freq: Frequência de uso de fio dental (opcional)
        
        Returns:
            Dicionário com:
                - prediction: 0 ou 1
                - probability: Probabilidade da previsão
                - recommendation: Recomendação textual
                - reward_points: Pontos de recompensa calculados
        """
        try:
            self.validate_input(input_data)
            
            # Preparar features com valores padrão se necessário
            features = np.array([
                input_data['age'],
                input_data['history'],
                input_data['severity'],
                input_data.get('brushing_freq', self.config.DEFAULT_BRUSHING_FREQ),
                input_data.get('flossing_freq', self.config.DEFAULT_FLOSSING_FREQ)
            ]).reshape(1, -1)
            
            # Fazer previsão
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'recommendation': self.generate_recommendation(prediction, probability),
                'reward_points': self.calculate_reward_points(input_data),
                'model_version': self.config.MODEL_VERSION
            }
            
        except Exception as e:
            raise ValueError(f"Erro na predição: {str(e)}")
    
    def generate_recommendation(self, prediction: int, probability: float) -> str:
        """Gera recomendações personalizadas baseadas na previsão"""
        if prediction == 1 and probability > self.config.HIGH_RISK_THRESHOLD:
            return ("🔴 Risco alto! Recomendamos consulta urgente com um especialista "
                   "dentro de 1 semana.")
        elif prediction == 1:
            return ("🟡 Risco moderado. Sugerimos agendar uma avaliação preventiva "
                   "dentro de 1 mês.")
        else:
            return ("🟢 Risco baixo. Continue com os bons hábitos de higiene bucal "
                   "e visite seu dentista regularmente.")
    
    def calculate_reward_points(self, input_data: Dict) -> int:
        """Calcula pontos de recompensa baseados em hábitos saudáveis"""
        points = 0
        points += input_data.get('brushing_freq', 0) * self.config.REWARD_BRUSHING_POINTS
        points += input_data.get('flossing_freq', 0) * self.config.REWARD_FLOSSING_POINTS
        
        if input_data.get('regular_checkups', False):
            points += self.config.REWARD_CHECKUP_POINTS
        
        # Bônus para hábitos consistentes
        if (input_data.get('brushing_freq', 0) >= 2 and 
            input_data.get('flossing_freq', 0) >= 1):
            points += self.config.REWARD_CONSISTENCY_BONUS
            
        return points
    
    def get_personalized_tips(self, patient_data: Dict) -> List[str]:
        """
        Retorna dicas personalizadas baseadas nos hábitos do paciente
        
        Args:
            patient_data: Dicionário contendo hábitos do paciente
        
        Returns:
            Lista com até 3 dicas personalizadas
        """
        tips = []
        
        # Dicas baseadas em escovação
        brushing = patient_data.get('brushing_freq', 0)
        if brushing < 1:
            tips.append("⚠️ Escove seus dentes pelo menos 1x ao dia para manter a saúde bucal básica.")
        elif brushing < 2:
            tips.append("✨ Melhore sua rotina escovando os dentes 2x ao dia (manhã e noite).")
        
        # Dicas baseadas em fio dental
        if patient_data.get('flossing_freq', 0) < 1:
            tips.append("🧵 Use fio dental diariamente para prevenir problemas gengivais.")
        
        # Dicas baseadas em check-ups
        if not patient_data.get('regular_checkups', False):
            tips.append("🦷 Agende consultas odontológicas a cada 6 meses para prevenção.")
        
        # Feedback positivo se todos bons hábitos
        if not tips:
            tips.append("🏆 Excelentes hábitos! Continue assim para manter um sorriso saudável.")
        
        return tips[:3]  # Limita a 3 dicas