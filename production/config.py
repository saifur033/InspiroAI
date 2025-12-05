"""
InspiroAI Setup Configuration File
Contains all environment variables and configuration settings
"""

# ============================================================
# FACEBOOK API CONFIGURATION
# ============================================================

# Set these values to enable Facebook posting
FACEBOOK_ACCESS_TOKEN = None  # Your Facebook page access token
FACEBOOK_PAGE_ID = None       # Your Facebook page ID (numeric)

# API Endpoints
FACEBOOK_API_VERSION = "v18.0"
FACEBOOK_GRAPH_URL = "https://graph.facebook.com"

# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Model directories
MODELS_DIR = "models"
EMBEDDER_MODEL = "all-MiniLM-L6-v2"  # SentenceTransformer model ID

# Decision thresholds
REACH_THRESHOLD = 0.40               # Threshold for high/low reach classification
STATUS_THRESHOLD = 0.40              # Threshold for real/fake classification

# Ensemble weights for status detection
STATUS_ENSEMBLE_WEIGHTS = {
    "xgb": 0.5,      # XGBoost weight
    "rf": 0.3,       # Random Forest weight
    "lgb": 0.2       # LightGBM weight
}

# ============================================================
# FEATURE CONFIGURATION
# ============================================================

# Reach prediction features (exact order from notebooks)
REACH_NUMERIC_FEATURES = [
    "char_count",
    "word_count",
    "avg_word_len",
    "emoji_count",
    "has_hashtag",
    "fk_grade",
    "hour",
    "dow",
    "is_weekend",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
]

# Categorical features
REACH_CATEGORICAL_FEATURES = ["category", "language"]

# Status detection features
STATUS_STYLE_FEATURES = [
    "text_length",
    "num_emojis",
    "punctuation_count",
    "has_links",
    "sentiment",
    "log_engagement",
    "avg_word_len",
    "num_hashtags",
    "num_mentions",
    "uppercase_ratio",
]

# ============================================================
# EMOTION DETECTION CONFIGURATION
# ============================================================

# TF-IDF parameters (from emotion notebook)
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MIN_DF = 2
TFIDF_MAX_DF = 0.9

# Emotion classes
EMOTION_CLASSES = ["joy", "sadness", "anger", "neutral", "surprise", "fear"]

# ============================================================
# STREAMLIT UI CONFIGURATION
# ============================================================

# Page settings
PAGE_TITLE = "InspiroAI"
PAGE_ICON = "💠"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Colors & styling
PRIMARY_COLOR = "#667eea"
SECONDARY_COLOR = "#764ba2"
SUCCESS_COLOR = "#28a745"
WARNING_COLOR = "#ffc107"
ERROR_COLOR = "#f5576c"

# ============================================================
# PERFORMANCE CONFIGURATION
# ============================================================

# Cache settings
CACHE_EMBEDDINGS = True
EMBEDDER_BATCH_SIZE = 32
EMBEDDER_DEVICE = "cpu"  # or "cuda" for GPU

# Inference settings
INFERENCE_TIMEOUT = 30  # seconds
MAX_CAPTION_LENGTH = 5000  # characters

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

LOG_LEVEL = "INFO"
LOG_FILE = "inspiroai.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================
# DEPLOYMENT CONFIGURATION
# ============================================================

# Debug mode
DEBUG = False

# CORS settings for API
CORS_ORIGINS = ["*"]

# Rate limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds

# ============================================================
# ADVANCED SETTINGS
# ============================================================

# Hyperparameter tuning (if retraining)
RANDOM_STATE = 42
TEST_SIZE = 0.2
VAL_SIZE = 0.1

# Class weights
CLASS_WEIGHTS = "balanced"

# Cross-validation folds
CV_FOLDS = 5

# ============================================================
# INTEGRATION SETTINGS
# ============================================================

# For future expansions
ENABLE_INSTAGRAM = False
ENABLE_TIKTOK = False
ENABLE_TWITTER = False

# API integration
ENABLE_HUGGINGFACE_API = False
HUGGINGFACE_API_KEY = None

# ============================================================
# MONITORING & ANALYTICS
# ============================================================

# Track predictions
TRACK_PREDICTIONS = True
PREDICTIONS_LOG_FILE = "predictions.log"

# Model performance tracking
TRACK_MODEL_PERFORMANCE = True
PERFORMANCE_LOG_FILE = "performance.log"

# User feedback collection
COLLECT_USER_FEEDBACK = False
FEEDBACK_DB = "feedback.db"

# ============================================================
# SECURITY SETTINGS
# ============================================================

# API Security
REQUIRE_AUTH = False
SECRET_KEY = None  # Set if enabling auth

# Data retention
DELETE_OLD_LOGS_AFTER_DAYS = 90
DELETE_OLD_PREDICTIONS_AFTER_DAYS = 180

# ============================================================
# DEFAULTS & CONSTANTS
# ============================================================

DEFAULT_POSTING_HOUR = 12  # Noon
DEFAULT_POSTING_DAY = 2     # Wednesday

# Sentiment mapping
SENTIMENT_MAPPING = {
    "negative": -1,
    "neutral": 0,
    "positive": 1
}

# Status labels
STATUS_LABELS = ["Real", "Fake/Spam"]
REACH_LABELS = ["Low Reach", "High Reach"]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_config():
    """Load configuration from environment or defaults"""
    import os
    
    config = {
        "facebook_token": os.getenv("FACEBOOK_TOKEN", FACEBOOK_ACCESS_TOKEN),
        "facebook_page_id": os.getenv("FACEBOOK_PAGE_ID", FACEBOOK_PAGE_ID),
        "models_dir": os.getenv("MODELS_DIR", MODELS_DIR),
        "debug": os.getenv("DEBUG", DEBUG).lower() == "true",
        "embedder_device": os.getenv("EMBEDDER_DEVICE", EMBEDDER_DEVICE),
    }
    return config


def validate_config():
    """Validate configuration settings"""
    import os
    
    # Check models directory
    if not os.path.exists(MODELS_DIR):
        print(f"Warning: Models directory '{MODELS_DIR}' not found")
        return False
    
    # Check for required model files
    required_models = [
        "emotion_svm_pipeline.joblib",
        "reach_voting.joblib",
        "status_xgb.joblib",
    ]
    
    for model_file in required_models:
        model_path = os.path.join(MODELS_DIR, model_file)
        if not os.path.exists(model_path):
            print(f"Error: Required model '{model_file}' not found in {MODELS_DIR}")
            return False
    
    return True
