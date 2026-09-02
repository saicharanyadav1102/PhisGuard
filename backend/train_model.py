import pandas as pd
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split 
import joblib
import os

def train_model(data_path): 
    print("Loading dataset...")
    df = pd.read_csv(data_path)

    print("Selecting features...")
    # Features mapped based on Appendix G
    feature_cols = ['redirect_count', 'roi_discrepancy', 'iframe_ratio', 'domain_age_days', 'ssl_active']
    X = df[feature_cols]
    y = df['label'] # 1 for Phish, 0 for Safe

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Initializing Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=200, 
        max_depth=30, 
        random_state=42
    )

    print("Fitting model...")
    rf.fit(X_train, y_train)

    print("Evaluating...")
    accuracy = rf.score(X_test, y_test)
    print(f"Model trained with {accuracy*100:.2f}% accuracy")

    print("Saving model...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(rf, 'models/phish_model.joblib')
    print("Model saved to models/phish_model.joblib")

if __name__ == "__main__":
    train_model('data/phishing_dataset.csv')
