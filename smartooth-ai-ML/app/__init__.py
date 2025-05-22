from flask import Flask
from flask_cors import CORS
from config import Config

from app.routes import init_routes
from app.iot_integration import init_iot
from app.monitoring import init_monitoring
from app.services.reward_service import RewardService

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Habilitar CORS
    CORS(app)
    
    # Inicializar serviços
    app.reward_service = RewardService()
    
    # Inicializar componentes
    init_routes(app)
    init_iot(app)
    init_monitoring(app)
    
    # Rota de health check
    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'services': ['core', 'iot', 'rewards']
        }
    
    return app