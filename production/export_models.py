"""
Export models from notebook artifacts to production pickle files
This script should be run after training to save models
"""
import os
import json
import joblib
import numpy as np
from pathlib import Path


def create_dummy_models():
    """
    Create dummy models for production testing
    In real deployment, these would be loaded from trained notebook artifacts
    """
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    print("=" * 60)
    print("Creating placeholder models for production...")
    print("=" * 60)
    
    # ============================================
    # EMOTION DETECTION MODELS
    # ============================================
    print("\n📦 Creating emotion detection models...")
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import LabelEncoder
    
    # Create placeholder pipeline
    tfidf = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.9,
        lowercase=True,
        token_pattern=r"(?u)\b\w[\w'-]*\b"
    )
    
    base_svc = LinearSVC(class_weight="balanced", random_state=42, max_iter=5000)
    calibrated = CalibratedClassifierCV(estimator=base_svc, cv=3, method="sigmoid")
    
    emotion_pipeline = Pipeline([
        ("tfidf", tfidf),
        ("clf", calibrated)
    ])
    
    # Train on minimal sample data (placeholder)
    sample_texts = [
        "I love this!", "I feel happy", "This is great",
        "I'm sad", "This is bad", "I feel awful",
        "This is interesting", "I'm not sure", "Whatever"
    ]
    sample_emotions = [0, 0, 0, 1, 1, 1, 2, 2, 2]  # 0=joy, 1=sadness, 2=neutral
    
    emotion_pipeline.fit(sample_texts, sample_emotions)
    
    le = LabelEncoder()
    le.fit(["joy", "sadness", "neutral"])
    
    joblib.dump(emotion_pipeline, os.path.join(models_dir, "emotion_svm_pipeline.joblib"))
    joblib.dump(le, os.path.join(models_dir, "emotion_label_encoder.joblib"))
    
    print("   ✅ emotion_svm_pipeline.joblib")
    print("   ✅ emotion_label_encoder.joblib")
    
    # ============================================
    # REACH PREDICTION MODELS
    # ============================================
    print("\n📦 Creating reach prediction models...")
    
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.ensemble import VotingClassifier, RandomForestClassifier
    from xgboost import XGBClassifier
    from sklearn.base import BaseEstimator, ClassifierMixin
    from catboost import CatBoostClassifier
    
    # sklearn-compatible wrapper for CatBoost so type checkers accept it as a BaseEstimator
    class CatBoostSklearnWrapper(BaseEstimator, ClassifierMixin):
        def __init__(self, **kwargs):
            self.cb = CatBoostClassifier(**kwargs)
        def fit(self, X, y, **fit_params):
            # ensure silent training by default
            fit_params = dict(fit_params)
            fit_params.setdefault("verbose", False)
            self.cb.fit(X, y, **fit_params)
            return self
        def predict(self, X):
            return self.cb.predict(X)
        def predict_proba(self, X):
            return self.cb.predict_proba(X)
    
    # Create simple voting classifier with placeholder models
    logreg = LogisticRegression(max_iter=500, random_state=42)
    xgb_clf = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss', verbosity=0)
    cat_clf = CatBoostSklearnWrapper(iterations=100, random_state=42, verbose=False)
    
    # Create minimal training data
    X_dummy_reach = np.random.rand(50, 384 + 13)  # 384 dims embeddings + 13 numeric features
    y_dummy_reach = np.random.randint(0, 2, 50)
    
    logreg.fit(X_dummy_reach, y_dummy_reach)
    xgb_clf.fit(X_dummy_reach, y_dummy_reach)
    cat_clf.fit(X_dummy_reach, y_dummy_reach)
    
    voting_clf = VotingClassifier(
        estimators=[("XGB", xgb_clf), ("CatBoost", cat_clf), ("LogReg", logreg)],
        voting="soft"
    )
    voting_clf.fit(X_dummy_reach, y_dummy_reach)
    
    joblib.dump(voting_clf, os.path.join(models_dir, "reach_voting.joblib"))
    
    # Scaler and OHE
    scaler = StandardScaler(with_mean=False)
    scaler.fit(X_dummy_reach[:, -13:])
    joblib.dump(scaler, os.path.join(models_dir, "reach_scaler.joblib"))
    
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    ohe.fit(np.array([["", ""]]))  # Placeholder
    joblib.dump(ohe, os.path.join(models_dir, "reach_ohe.joblib"))
    
    # Metadata
    reach_meta = {
        "embedder": "all-MiniLM-L6-v2",
        "cat_cols": ["category", "language"],
        "num_cols": ["char_count", "word_count", "avg_word_len", "emoji_count",
                     "has_hashtag", "fk_grade", "hour", "dow", "is_weekend",
                     "hour_sin", "hour_cos", "dow_sin", "dow_cos"]
    }
    
    with open(os.path.join(models_dir, "reach_meta.json"), "w") as f:
        json.dump(reach_meta, f)
    
    joblib.dump({"best_thresh": 0.40}, os.path.join(models_dir, "reach_thresh.joblib"))
    
    print("   ✅ reach_voting.joblib")
    print("   ✅ reach_scaler.joblib")
    print("   ✅ reach_ohe.joblib")
    print("   ✅ reach_meta.json")
    print("   ✅ reach_thresh.joblib")
    
    # ============================================
    # STATUS (FAKE/REAL) DETECTION MODELS
    # ============================================
    print("\n📦 Creating status detection models...")
    
    import lightgbm as lgb
    
    # Create minimal training data (embedding + style features)
    X_dummy_status = np.random.rand(50, 384 + 10)  # 384 embedding + 10 style features
    y_dummy_status = np.random.randint(0, 2, 50)
    
    xgb_status = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss', verbosity=0)
    rf_status = RandomForestClassifier(n_estimators=100, random_state=42)
    lgb_status = lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    
    xgb_status.fit(X_dummy_status, y_dummy_status)
    rf_status.fit(X_dummy_status, y_dummy_status)
    lgb_status.fit(X_dummy_status, y_dummy_status)
    
    joblib.dump(xgb_status, os.path.join(models_dir, "status_xgb.joblib"))
    joblib.dump(rf_status, os.path.join(models_dir, "status_rf.joblib"))
    joblib.dump(lgb_status, os.path.join(models_dir, "status_lgb.joblib"))
    
    # Style features list
    status_style_features = [
        "text_length", "num_emojis", "punctuation_count", "has_links",
        "sentiment", "log_engagement", "avg_word_len", "num_hashtags",
        "num_mentions", "uppercase_ratio"
    ]
    joblib.dump(status_style_features, os.path.join(models_dir, "status_style_features.joblib"))
    
    # Metadata
    status_meta = {
        "best_threshold": 0.40,
        "random_seed": 42
    }
    
    with open(os.path.join(models_dir, "status_meta.json"), "w") as f:
        json.dump(status_meta, f)
    
    print("   ✅ status_xgb.joblib")
    print("   ✅ status_rf.joblib")
    print("   ✅ status_lgb.joblib")
    print("   ✅ status_style_features.joblib")
    print("   ✅ status_meta.json")
    
    print("\n" + "=" * 60)
    print("✅ All models created and saved to ./models/")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    create_dummy_models()
