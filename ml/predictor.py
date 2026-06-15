import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from security.strength import calculate_shannon_entropy, calculate_pool_size

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "rf_model.pkl")

def _extract_features(passwords):
    """Extract structural features for passwords."""
    features = []
    for p in passwords:
        length = len(p)
        entropy = calculate_shannon_entropy(p)
        pool_size = calculate_pool_size(p)
        num_digits = sum(c.isdigit() for c in p)
        num_upper = sum(c.isupper() for c in p)
        num_special = sum(not c.isalnum() for c in p)
        features.append([length, entropy, pool_size, num_digits, num_upper, num_special])
    return np.array(features)

def train_synthetic_model():
    """Trains a simple Random Forest model on synthetic data."""
    # Synthetic Data (Feature engineering approach)
    passwords = [
        "password", "123456", "qwerty", "admin123", # Weak (0)
        "Hello!123", "P@ssw0rd2026", "MyDogSpot1!", # Moderate (1)
        "c0rr3ct-h0rs3-b@tt3ry", "vEry$tr0ng!p@ssw0rd!!", "a8F#9kL!2pQz*1" # Strong (2)
    ]
    labels = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    
    # In a real scenario, we'd use a massive dataset. For this local MVP, we rely on structural features.
    X = _extract_features(passwords)
    y = np.array(labels)
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model

def predict_strength(password: str) -> dict:
    """Predicts password strength using the local ML model."""
    if not os.path.exists(MODEL_PATH):
        model = train_synthetic_model()
    else:
        try:
            model = joblib.load(MODEL_PATH)
        except Exception:
            model = train_synthetic_model()
            
    X = _extract_features([password])
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    score_map = {0: "Weak", 1: "Moderate", 2: "Strong"}
    
    # Calculate a 0-100 score based on class probabilities
    # 0 = 0-33, 1 = 34-66, 2 = 67-100
    if prediction == 0:
        score = int(probabilities[0] * 33)
    elif prediction == 1:
        score = 33 + int(probabilities[1] * 33)
    else:
        score = 66 + int(probabilities[2] * 34)
        
    return {
        "ml_score": score,
        "ml_label": score_map[prediction],
        "confidence": round(probabilities[prediction] * 100, 2)
    }
