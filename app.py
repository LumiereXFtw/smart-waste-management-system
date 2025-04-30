from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import joblib
import os
import logging

app = Flask(__name__)
CORS(app)

# Constants
MODEL_PATH = "waste_collection_model.joblib"
SCALER_PATH = "feature_scaler.joblib"
DATASET_PATH = "historical_data.csv"
METRICS_PATH = "model_metrics.csv"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WasteCollectionPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.is_trained = False
        self.historical_data = self.load_historical_data()
        self.load_or_initialize_model()

    def load_historical_data(self):
        if os.path.exists(DATASET_PATH):
            try:
                df = pd.read_csv(DATASET_PATH)
                if 'timestamp' not in df.columns or 'fillLevel' not in df.columns:
                    raise ValueError("Invalid dataset format. Required columns: timestamp, fillLevel")
                return df
            except Exception as e:
                logger.error(f"Error loading historical data: {e}")
        return pd.DataFrame(columns=['timestamp', 'fillLevel'])

    def load_or_initialize_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)
                self.is_trained = True
                logger.info("Model and scaler loaded successfully.")
                return
            except Exception as e:
                logger.error(f"Error loading model: {e}")
        self._initialize_new_model()
        if not self.historical_data.empty:
            self.train(self.historical_data)

    def _initialize_new_model(self):
        self.model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def create_features(self, df):
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df.dropna(subset=['timestamp'], inplace=True)
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['rolling_mean_7d'] = df['fillLevel'].rolling(window=min(7, len(df)), min_periods=1).mean()
        df['rolling_std_7d'] = df['fillLevel'].rolling(window=min(7, len(df)), min_periods=1).std()
        df.fillna(0, inplace=True)
        return df

    def prepare_features(self, df):
        feature_columns = ['day_of_week', 'day_of_month', 'month', 'is_weekend', 'rolling_mean_7d', 'rolling_std_7d']
        return df[feature_columns]

    def train(self, df):
        try:
            df = self.create_features(df)
            X = self.prepare_features(df)
            y = df['fillLevel']
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True
            joblib.dump(self.model, MODEL_PATH)
            joblib.dump(self.scaler, SCALER_PATH)
            logger.info("Model trained and saved successfully.")
        except Exception as e:
            logger.error(f"Training error: {e}")
            raise

    def predict(self, future_dates):
        if not self.is_trained:
            raise ValueError("Model is not trained")
        future_df = pd.DataFrame({'timestamp': future_dates})
        future_df['fillLevel'] = 0
        future_df = self.create_features(future_df)
        X_future = self.prepare_features(future_df)
        X_future_scaled = self.scaler.transform(X_future)
        predictions = self.model.predict(X_future_scaled)
        return predictions.tolist()

predictor = WasteCollectionPredictor()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def get_predictions():
    try:
        if not predictor.is_trained:
            return jsonify({'error': 'Model not trained. Please upload data first.'}), 400
        future_dates = [(datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(14)]
        predictions = predictor.predict(future_dates)
        response = [{'date': date, 'predicted_fill_level': round(pred, 2), 'should_collect': pred >= 75} for date, pred in zip(future_dates, predictions)]
        return jsonify(response)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    try:
        df = pd.read_csv(file)
        if 'timestamp' not in df.columns or 'fillLevel' not in df.columns:
            return jsonify({'error': 'Invalid CSV format. Required columns: timestamp, fillLevel'}), 400
        df.to_csv(DATASET_PATH, index=False)
        predictor.train(df)
        return jsonify({'message': 'File uploaded and model retrained successfully'}), 200
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/dataset/info', methods=['GET'])
def dataset_info():
    """Returns dataset details like record count and date range"""
    try:
        if predictor.historical_data.empty:
            return jsonify({'error': 'No dataset available'}), 400
        start_date = predictor.historical_data['timestamp'].min()
        end_date = predictor.historical_data['timestamp'].max()
        return jsonify({
            'total_records': len(predictor.historical_data),
            'date_range': {'start': start_date, 'end': end_date},
            'is_trained': predictor.is_trained
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def model_metrics():
    """Returns model performance metrics"""
    if not os.path.exists(METRICS_PATH):
        return jsonify({'error': 'No metrics available'}), 400
    try:
        metrics_df = pd.read_csv(METRICS_PATH)
        metrics = metrics_df.to_dict(orient='records')
        return jsonify({'metrics': metrics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
