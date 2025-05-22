from datetime import datetime, timedelta
from typing import Dict, List

class RewardService:
    def __init__(self):
        self.rewards = [
            {"id": 1, "name": "Kit de Higiene Bucal", "points": 100, "stock": 50},
            {"id": 2, "name": "Desconto em Limpeza", "points": 200, "stock": 30},
            {"id": 3, "name": "Consulta Gratuita", "points": 300, "stock": 10}
        ]
        self.user_points = {}  # Em produção, substituir por banco de dados

    def get_available_rewards(self, user_id: str) -> List[Dict]:
        user_points = self.user_points.get(user_id, 0)
        return [r for r in self.rewards if r['points'] <= user_points and r['stock'] > 0]

    def add_points(self, user_id: str, points: int) -> Dict:
        if user_id not in self.user_points:
            self.user_points[user_id] = 0
        self.user_points[user_id] += points
        return {"user_id": user_id, "total_points": self.user_points[user_id]}

    def redeem_reward(self, user_id: str, reward_id: int) -> Dict:
        reward = next((r for r in self.rewards if r['id'] == reward_id), None)
        if not reward:
            return {"error": "Reward not found"}
        
        if reward['stock'] <= 0:
            return {"error": "Reward out of stock"}
        
        user_points = self.user_points.get(user_id, 0)
        if user_points < reward['points']:
            return {"error": "Not enough points"}
        
        # Atualizar pontos e estoque
        self.user_points[user_id] -= reward['points']
        reward['stock'] -= 1
        
        return {
            "success": True,
            "reward": reward['name'],
            "remaining_points": self.user_points[user_id]
        }

    def get_weekly_leaderboard(self) -> List[Dict]:
        # Simulação - em produção, buscar de um banco de dados
        return [
            {"user_id": "user1", "name": "João", "points": 450},
            {"user_id": "user2", "name": "Maria", "points": 380},
            {"user_id": "user3", "name": "Carlos", "points": 270}
        ]