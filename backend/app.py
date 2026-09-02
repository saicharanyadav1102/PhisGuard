from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import logging
import os
import pandas as pd

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# Configure Logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/api.log', level=logging.INFO)

# Load the Random Forest model 
model = None
try:
    model = joblib.load('models/phish_model.joblib')
except FileNotFoundError:
    app.logger.error("Model file not found! Please run train_model.py first.")

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()

    if not data or 'features' not in data:
        return jsonify({"error": "Invalid payload"}), 400

    features = data['features']
    logging.info(f"Predicting for features: {features}")

    # Inference logic 
    try:
        # Convert list to DataFrame to avoid scikit-learn UserWarning
        feature_cols = ['redirect_count', 'roi_discrepancy', 'iframe_ratio', 'domain_age_days', 'ssl_active']
        features_df = pd.DataFrame([features], columns=feature_cols)

        # Prediction
        probability = model.predict_proba(features_df)[0][1] 
        verdict = "phish" if probability > 0.8 else "safe"

        return jsonify({ 
            "verdict": verdict,
            "confidence": round(probability, 4), 
            "status": "success"
        })
    except Exception as e: 
        app.logger.error(f"Inference error: {str(e)}")
        return jsonify({"error": "Model execution failed"}), 500

if __name__ == "__main__": 
    app.run(port=5000, debug=False)
