"""
Configuration file for News Classifier Application
"""

# Model Configuration
MODEL_CONFIG = {
    'vector_size': 150,      # Dimensi vektor word embedding
    'window': 3,             # Context window size
    'min_count': 2,          # Minimum word frequency
    'epochs': 50,            # Training epochs
    'sg': 1,                 # Skip-gram (1) or CBOW (0)
    'workers': 4,            # Parallel processing
    'seed': 42               # Random seed for reproducibility
}

# SVM Configuration
SVM_CONFIG = {
    'kernel': 'linear',
    'C': 1.0,
    'probability': True,
    'random_state': 42
}

# Data Configuration
DATA_CONFIG = {
    'test_size': 0.2,        # 20% for testing
    'random_state': 42,
    'stratify': True         # Balanced split
}

# Scraping Configuration
SCRAPER_CONFIG = {
    'timeout': 10,           # Request timeout (seconds)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# UI Configuration
UI_CONFIG = {
    'page_title': 'Detik News Classifier',
    'page_icon': '📰',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Label Mapping
LABEL_MAPPING = {
    0: 'Finance',
    1: 'Sport',
    'finance': 0,
    'sport': 1
}

# Color Scheme (Professional, minimal)
COLOR_SCHEME = {
    'primary': '#1f77b4',    # Professional blue
    'secondary': '#2ca02c',  # Green
    'sport': '#ff7f0e',      # Orange
    'finance': '#1f77b4',    # Blue
    'background': '#f8f9fa',
    'text': '#2c3e50'
}

# Paths
PATHS = {
    'models': 'models/',
    'data': 'data/',
    'skipgram_model': 'models/skipgram_model.model',
    'svm_model': 'models/svm_classifier.joblib',
    'sport_data': 'data/detik_sport_90.csv',
    'finance_data': 'data/detik_finance_90.csv'
}
