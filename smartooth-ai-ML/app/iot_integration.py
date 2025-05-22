from flask import request, jsonify
from datetime import datetime
import random
from typing import Dict, List

class ToothbrushTracker:
    def __init__(self):
        self.devices = {}
        
    def process_brushing_data(self, device_id: str, brushing_data: List[Dict]) -> Dict:
        """Processa dados de escovação de dispositivos IoT"""
        if not brushing_data:
            raise ValueError("No brushing data provided")
            
        # Analisar dados de escovação
        total_duration = sum(session.get('duration', 0) for session in brushing_data)
        avg_pressure = sum(session.get('pressure', 0) for session in brushing_data) / len(brushing_data)
        coverage = sum(session.get('coverage', 0) for session in brushing_data) / len(brushing_data)
        
        # Salvar dados do dispositivo
        self.devices[device_id] = {
            'last_sync': datetime.now().isoformat(),
            'metrics': {
                'daily_brushing_sessions': len(brushing_data),
                'avg_duration': total_duration / len(brushing_data),
                'avg_pressure': avg_pressure,
                'coverage_score': coverage
            }
        }
        
        return {
            'device_id': device_id,
            'habits': {
                'brushing_freq': len(brushing_data),
                'quality_score': min(10, (coverage * avg_pressure) / 10)
            },
            'metrics': self.devices[device_id]['metrics']
        }
    
    def get_active_devices_count(self) -> int:
        """Retorna número de dispositivos ativos"""
        return len(self.devices)
    
    def get_device_health(self, device_id: str) -> Dict:
        """Retorna métricas de saúde bucal baseadas no dispositivo"""
        if device_id not in self.devices:
            raise ValueError("Device not found")
            
        return self.devices[device_id]['metrics']

def init_iot(app):
    tracker = ToothbrushTracker()
    
    @app.route('/api/v1/iot/register', methods=['POST'])
    def register_device():
        device_id = request.json.get('device_id')
        if not device_id:
            return jsonify({"error": "device_id is required"}), 400
            
        tracker.devices[device_id] = {'registered_at': datetime.now().isoformat()}
        return jsonify({"status": "registered", "device_id": device_id})