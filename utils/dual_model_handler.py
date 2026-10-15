"""
Dual Model Handler: Skip-Gram dan TF-IDF
Support klasifikasi dengan 2 metode berbeda
"""

import numpy as np
import joblib
from gensim.models import Word2Vec
from pathlib import Path
from typing import Tuple, Dict, List
from config import PATHS, LABEL_MAPPING


class DualModelHandler:
    """Handler untuk Skip-Gram dan TF-IDF model"""
    
    _instance = None
    
    # Skip-Gram components
    _skipgram_model = None
    _svm_skipgram = None
    
    # TF-IDF components
    _tfidf_vectorizer = None
    _svm_tfidf = None
    
    _is_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DualModelHandler, cls).__new__(cls)
        return cls._instance
    
    def load_models(self) -> bool:
        """Load semua model (Skip-Gram dan TF-IDF)"""
        if self._is_loaded:
            return True
        
        try:
            # Load Skip-Gram Word2Vec
            skipgram_path = Path(PATHS['skipgram_model'])
            if skipgram_path.exists():
                self._skipgram_model = Word2Vec.load(str(skipgram_path))
            
            # Load SVM Skip-Gram
            svm_skipgram_path = Path(PATHS['svm_model'])
            if svm_skipgram_path.exists():
                self._svm_skipgram = joblib.load(str(svm_skipgram_path))
            
            # Load TF-IDF Vectorizer
            tfidf_path = Path('models/tfidf_vectorizer.joblib')
            if tfidf_path.exists():
                self._tfidf_vectorizer = joblib.load(str(tfidf_path))
            
            # Load SVM TF-IDF
            svm_tfidf_path = Path('models/svm_tfidf_classifier.joblib')
            if svm_tfidf_path.exists():
                self._svm_tfidf = joblib.load(str(svm_tfidf_path))
            
            self._is_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def get_skipgram_info(self) -> Dict:
        """Info model Skip-Gram"""
        if not self._is_loaded:
            self.load_models()
        
        if self._skipgram_model is None:
            return {}
        
        return {
            'method': 'Skip-Gram (Word2Vec)',
            'vector_size': self._skipgram_model.vector_size,
            'vocab_size': len(self._skipgram_model.wv),
            'window': self._skipgram_model.window,
            'representation': 'Mean Word Vector (Rata-rata Vektor Kata)'
        }
    
    def get_tfidf_info(self) -> Dict:
        """Info model TF-IDF"""
        if not self._is_loaded:
            self.load_models()
        
        if self._tfidf_vectorizer is None:
            return {}
        
        vocab_size = len(self._tfidf_vectorizer.vocabulary_) if hasattr(self._tfidf_vectorizer, 'vocabulary_') else 0
        
        return {
            'method': 'TF-IDF Vectorizer',
            'vocab_size': vocab_size,
            'representation': 'TF-IDF Matrix (Term Frequency - Inverse Document Frequency)'
        }
    
    def classify_skipgram(self, tokens: List[str]) -> Dict:
        """
        Klasifikasi menggunakan Skip-Gram
        Skip-Gram: TIDAK pakai stopword removal dan stemming (hanya noise removal)
        """
        if self._svm_skipgram is None or self._skipgram_model is None:
            raise RuntimeError("Model Skip-Gram belum dimuat")
        
        # Convert tokens ke vektor (mean pooling)
        matched_vectors = []
        matched_tokens = []
        oov_tokens = []
        
        for token in tokens:
            if not token:
                continue
            
            if token in self._skipgram_model.wv:
                matched_vectors.append(self._skipgram_model.wv[token])
                matched_tokens.append(token)
            else:
                oov_tokens.append(token)
        
        # Mean pooling
        if len(matched_vectors) > 0:
            doc_vector = np.mean(matched_vectors, axis=0)
        else:
            doc_vector = np.zeros(self._skipgram_model.vector_size)
        
        # Prediksi dengan SVM
        vector_2d = doc_vector.reshape(1, -1)
        prediction = self._svm_skipgram.predict(vector_2d)[0]
        
        # Probabilitas
        probabilities = {}
        if hasattr(self._svm_skipgram, 'predict_proba'):
            proba = self._svm_skipgram.predict_proba(vector_2d)[0]
            for idx, class_label in enumerate(self._svm_skipgram.classes_):
                label_name = LABEL_MAPPING.get(class_label, str(class_label))
                probabilities[label_name] = float(proba[idx]) * 100
        
        predicted_label = LABEL_MAPPING.get(prediction, str(prediction))
        confidence = max(probabilities.values()) if probabilities else 0.0
        
        return {
            'method': 'skipgram',
            'method_label': 'Skip-Gram (Word2Vec) + SVM',
            'prediction': predicted_label,
            'confidence': confidence,
            'probabilities': probabilities,
            'total_tokens': len(tokens),
            'matched_tokens': len(matched_tokens),
            'oov_tokens': len(oov_tokens),
            'matched_sample': matched_tokens[:20],
            'vocab_coverage': (len(matched_tokens) / len(tokens) * 100) if tokens else 0,
            'vector_dimension': self._skipgram_model.vector_size,
            'vector_sample': [round(float(v), 5) for v in doc_vector[:15]],  # Sample 15 nilai pertama
            'vector_full': doc_vector.tolist()  # Full vector
        }
    
    def classify_tfidf(self, processed_text: str) -> Dict:
        """
        Klasifikasi menggunakan TF-IDF
        TF-IDF: Pakai stopword removal dan stemming (preprocessing lengkap)
        """
        if self._svm_tfidf is None or self._tfidf_vectorizer is None:
            raise RuntimeError("Model TF-IDF belum dimuat")
        
        # Transform ke TF-IDF vector
        tfidf_vector = self._tfidf_vectorizer.transform([processed_text])
        
        # Prediksi dengan SVM
        prediction = self._svm_tfidf.predict(tfidf_vector)[0]
        
        # Probabilitas
        probabilities = {}
        if hasattr(self._svm_tfidf, 'predict_proba'):
            proba = self._svm_tfidf.predict_proba(tfidf_vector)[0]
            for idx, class_label in enumerate(self._svm_tfidf.classes_):
                label_name = LABEL_MAPPING.get(class_label, str(class_label))
                probabilities[label_name] = float(proba[idx]) * 100
        
        predicted_label = LABEL_MAPPING.get(prediction, str(prediction))
        confidence = max(probabilities.values()) if probabilities else 0.0
        
        # Ekstrak top TF-IDF features (kata dengan bobot tertinggi)
        top_features = []
        feature_names = self._tfidf_vectorizer.get_feature_names_out()
        row_idx, col_idx = tfidf_vector.nonzero()
        
        for col in col_idx:
            top_features.append({
                'word': str(feature_names[col]),
                'score': round(float(tfidf_vector[0, col]), 4)
            })
        
        # Sort by score
        top_features.sort(key=lambda x: x['score'], reverse=True)
        
        # Token statistics
        tokens = processed_text.split()
        total_vocab = len(self._tfidf_vectorizer.vocabulary_)
        active_features = len(col_idx)  # Fitur yang aktif (non-zero)
        
        # Vector sample (non-zero values only)
        vector_dense = tfidf_vector.toarray()[0]
        non_zero_indices = np.where(vector_dense > 0)[0]
        vector_sample = [
            {
                'feature': str(feature_names[idx]),
                'value': round(float(vector_dense[idx]), 5)
            }
            for idx in non_zero_indices[:15]  # Sample 15 pertama
        ]
        
        return {
            'method': 'tfidf',
            'method_label': 'TF-IDF Vectorizer + Model Klasifikasi',
            'prediction': predicted_label,
            'confidence': confidence,
            'probabilities': probabilities,
            'total_tokens': len(tokens),
            'active_features': active_features,
            'total_vocab': total_vocab,
            'top_features': top_features[:15],  # Top 15 keywords
            'vector_dimension': total_vocab,
            'vector_sample': vector_sample,
            'vector_full': vector_dense.tolist()  # Full vector
        }


# Global instance
_dual_handler = DualModelHandler()


def load_dual_models():
    """Load semua model"""
    return _dual_handler.load_models()


def get_skipgram_info():
    """Get Skip-Gram model info"""
    return _dual_handler.get_skipgram_info()


def get_tfidf_info():
    """Get TF-IDF model info"""
    return _dual_handler.get_tfidf_info()


def classify_with_method(tokens_or_text, method='skipgram'):
    """
    Klasifikasi dengan metode yang dipilih
    
    Args:
        tokens_or_text: List token (untuk skipgram) atau string (untuk tfidf)
        method: 'skipgram' atau 'tfidf'
    """
    if not _dual_handler._is_loaded:
        _dual_handler.load_models()
    
    if method.lower() == 'tfidf':
        # TF-IDF expects preprocessed string
        return _dual_handler.classify_tfidf(tokens_or_text)
    else:
        # Skip-Gram expects token list
        return _dual_handler.classify_skipgram(tokens_or_text)
