import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações gerais
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/production_model.pkl')
    MODEL_VERSION = os.getenv('MODEL_VERSION', '1.2.0')
    
    # Configurações do modelo de IA
    MODEL_N_ESTIMATORS = int(os.getenv('MODEL_N_ESTIMATORS', 200))
    MODEL_LEARNING_RATE = float(os.getenv('MODEL_LEARNING_RATE', 0.1))
    MODEL_MAX_DEPTH = int(os.getenv('MODEL_MAX_DEPTH', 3))
    MODEL_THRESHOLD = float(os.getenv('MODEL_THRESHOLD', 0.7))
    HIGH_RISK_THRESHOLD = float(os.getenv('HIGH_RISK_THRESHOLD', 0.75))
    
    # Valores padrão para predição
    DEFAULT_BRUSHING_FREQ = int(os.getenv('DEFAULT_BRUSHING_FREQ', 1))  # 1x ao dia
    DEFAULT_FLOSSING_FREQ = int(os.getenv('DEFAULT_FLOSSING_FREQ', 0))  # Nunca
    
    # Configurações de IoT
    MAX_IOT_DEVICES = int(os.getenv('MAX_IOT_DEVICES', 100))
    IOT_SYNC_INTERVAL = int(os.getenv('IOT_SYNC_INTERVAL', 60))  # segundos
    
    # Configurações de recompensas
    REWARD_BRUSHING_POINTS = int(os.getenv('REWARD_BRUSHING_POINTS', 10))
    REWARD_FLOSSING_POINTS = int(os.getenv('REWARD_FLOSSING_POINTS', 20))
    REWARD_CHECKUP_POINTS = int(os.getenv('REWARD_CHECKUP_POINTS', 50))
    REWARD_CONSISTENCY_BONUS = int(os.getenv('REWARD_CONSISTENCY_BONUS', 30))

class DevelopmentConfig(Config):
    DEBUG = True
    MODEL_PATH = 'models/development_model.pkl'  # Modelo separado para desenvolvimento

class ProductionConfig(Config):
    DEBUG = False
    # Forçar valores mais conservadores em produção
    MODEL_N_ESTIMATORS = 300
    MODEL_LEARNING_RATE = 0.05