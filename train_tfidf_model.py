"""
Script untuk training TF-IDF model + SVM Classifier
Run this once to generate tfidf_vectorizer.joblib and svm_tfidf_classifier.joblib
"""

import pandas as pd
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from utils.preprocessor import preprocess_text

# Paths
DATA_DIR = Path(__file__).parent / 'data'
MODEL_DIR = Path(__file__).parent / 'models'

def load_dataset():
    """Load dan combine dataset Sport + Finance"""
    print("Loading datasets...")
    
    # Load Sport
    sport_df = pd.read_csv(DATA_DIR / 'detik_sport_90.csv')
    sport_df['label'] = 1  # Sport = 1
    sport_df['category'] = 'Sport'
    
    # Load Finance
    finance_df = pd.read_csv(DATA_DIR / 'detik_finance_90.csv')
    finance_df['label'] = 0  # Finance = 0
    finance_df['category'] = 'Finance'
    
    # Combine
    df = pd.concat([sport_df, finance_df], ignore_index=True)
    
    print(f"Total articles: {len(df)}")
    print(f"Sport: {len(sport_df)}, Finance: {len(finance_df)}")
    
    return df

def preprocess_dataset(df):
    """Preprocess semua teks dalam dataset"""
    print("\nPreprocessing texts...")
    
    # Apply preprocessing (stopword removal + stemming)
    df['processed_text'] = df['isi_berita'].apply(preprocess_text)
    
    # Filter out empty processed texts
    df = df[df['processed_text'].str.len() > 10]
    
    print(f"After preprocessing: {len(df)} valid articles")
    
    return df

def train_tfidf_model(df):
    """Train TF-IDF Vectorizer + SVM"""
    print("\nTraining TF-IDF + SVM model...")
    
    X = df['processed_text']
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)}, Test set: {len(X_test)}")
    
    # TF-IDF Vectorizer
    print("\nCreating TF-IDF vectors...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=3000,  # Limit vocabulary
        min_df=2,           # Minimum document frequency
        max_df=0.8,         # Maximum document frequency
        ngram_range=(1, 2)  # Unigram + bigram
    )
    
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)
    
    print(f"TF-IDF vocabulary size: {len(tfidf_vectorizer.vocabulary_)}")
    print(f"TF-IDF vector shape: {X_train_tfidf.shape}")
    
    # Train SVM
    print("\nTraining SVM classifier...")
    svm_tfidf = SVC(
        kernel='linear',
        C=1.0,
        probability=True,  # Enable probability estimates
        random_state=42
    )
    
    svm_tfidf.fit(X_train_tfidf, y_train)
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred = svm_tfidf.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Finance', 'Sport']))
    
    # Save models
    print("\nSaving models...")
    tfidf_path = MODEL_DIR / 'tfidf_vectorizer.joblib'
    svm_tfidf_path = MODEL_DIR / 'svm_tfidf_classifier.joblib'
    
    joblib.dump(tfidf_vectorizer, tfidf_path)
    joblib.dump(svm_tfidf, svm_tfidf_path)
    
    print(f"✓ TF-IDF Vectorizer saved: {tfidf_path}")
    print(f"✓ SVM TF-IDF Classifier saved: {svm_tfidf_path}")
    
    return tfidf_vectorizer, svm_tfidf, accuracy

def main():
    """Main training pipeline"""
    print("="*60)
    print("TF-IDF MODEL TRAINING")
    print("="*60)
    
    # Load dataset
    df = load_dataset()
    
    # Preprocess
    df = preprocess_dataset(df)
    
    # Train model
    tfidf_vectorizer, svm_tfidf, accuracy = train_tfidf_model(df)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nFinal Accuracy: {accuracy*100:.2f}%")
    print(f"\nGenerated files:")
    print(f"  - models/tfidf_vectorizer.joblib")
    print(f"  - models/svm_tfidf_classifier.joblib")
    print(f"\nYou can now run the Streamlit app with TF-IDF support!")

if __name__ == "__main__":
    main()
