from flask import jsonify, request
import pandas as pd
from app.ml_models import DentalAIModel
import os

ai_model = DentalAIModel()

PATIENTS_CSV = "smartooth-ai-ML/data/patient_data.csv"

def load_patients():
    if not os.path.exists(PATIENTS_CSV):
        df = pd.DataFrame(columns=['id', 'name', 'age', 'habits'])
        df.to_csv(PATIENTS_CSV, index=False)
    return pd.read_csv(PATIENTS_CSV)

def save_patients(df):
    df.to_csv(PATIENTS_CSV, index=False)

def init_routes(app):
    # CRUD Pacientes
    @app.route('/patients', methods=['GET'])
    def get_patients():
        df = load_patients()
        return jsonify(df.to_dict(orient='records'))

    @app.route('/patients/<int:patient_id>', methods=['GET'])
    def get_patient(patient_id):
        df = load_patients()
        patient = df[df['id'] == patient_id]
        if patient.empty:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify(patient.iloc[0].to_dict())

    @app.route('/patients', methods=['POST'])
    def create_patient():
        df = load_patients()
        data = request.get_json()
        required_fields = ['name', 'age', 'habits']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_id = 1 if df.empty else df['id'].max() + 1
        new_patient = {
            'id': new_id,
            'name': data['name'],
            'age': data['age'],
            'habits': data['habits']
        }
        df = df.append(new_patient, ignore_index=True)
        save_patients(df)
        return jsonify(new_patient), 201

    @app.route('/patients/<int:patient_id>', methods=['PUT'])
    def update_patient(patient_id):
        df = load_patients()
        idx = df.index[df['id'] == patient_id].tolist()
        if not idx:
            return jsonify({"error": "Patient not found"}), 404

        data = request.get_json()
        for field in ['name', 'age', 'habits']:
            if field in data:
                df.at[idx[0], field] = data[field]
        save_patients(df)
        return jsonify(df.iloc[idx[0]].to_dict())

    @app.route('/patients/<int:patient_id>', methods=['DELETE'])
    def delete_patient(patient_id):
        df = load_patients()
        if patient_id not in df['id'].values:
            return jsonify({"error": "Patient not found"}), 404
        df = df[df['id'] != patient_id]
        save_patients(df)
        return jsonify({"message": "Patient deleted"}), 200

    # Rotas principais (home, predição, dicas, etc)
    @app.route('/')
    def home():
        return jsonify({
            "message": "Bem vindo ao Smartooth AI - Solução Odontológica Inteligente",
            "version": "2.0",
            "features": [
                "Predição de saúde bucal",
                "Recomendações personalizadas",
                "Programa de recompensas",
                "Integração com dispositivos IoT"
            ]
        })

    @app.route('/predict', methods=['POST'])
    def predict_health():
        try:
            data = request.get_json()
            required_fields = ['age', 'history', 'severity']
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400
            
            result = ai_model.predict(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/v1/tips', methods=['GET'])
    def get_tips():
        patient_id = request.args.get('patient_id')
        if not patient_id:
            return jsonify({"error": "patient_id is required"}), 400

        patient_data = {
            'brushing_freq': request.args.get('brushing_freq', default=1, type=int),
            'flossing_freq': request.args.get('flossing_freq', default=0, type=int),
            'regular_checkups': request.args.get('checkups', default='false') == 'true'
        }
        
        tips = ai_model.get_personalized_tips(patient_data)
        return jsonify({"patient_id": patient_id, "tips": tips})

    @app.route('/filter_procedures', methods=['GET'])
    def filter_procedures():
        try:
            procedures = pd.read_csv("smartooth-ai-ML/data/procedures.csv")
            return jsonify(procedures.to_dict(orient='records'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/patient_recommendations', methods=['GET'])
    def patient_recommendations():
        try:
            patient_id = request.args.get('patient_id')
            if not patient_id:
                return jsonify({"error": "Missing patient_id"}), 400

            patients_df = load_patients()
            procedures_df = pd.read_csv("smartooth-ai-ML/data/procedures.csv")

            patient = patients_df[patients_df['id'] == int(patient_id)]
            if patient.empty:
                return jsonify({"error": "Patient not found"}), 404

            def get_dental_tips(pid):
                return ["Escove os dentes duas vezes ao dia", "Use fio dental diariamente"]

            def get_recommendations(pid):
                return ["Tratamento de canal", "Limpeza profissional"]

            dental_tips = get_dental_tips(patient_id)
            recommendations = get_recommendations(patient_id)

            plan = patient.iloc[0]['habits']
            filtered_procedures = procedures_df[procedures_df['plan'] == plan]

            return jsonify({
                "patient": patient.iloc[0].to_dict(),
                "dental_tips": dental_tips,
                "recommendations": recommendations,
                "filtered_procedures": filtered_procedures.to_dict(orient='records')
            })
        except Exception as e:
            return jsonify({"error": f"Error processing request: {str(e)}"}), 500