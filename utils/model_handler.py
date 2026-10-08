"""
Model loading and prediction utilities
"""

import numpy as np
import joblib
from gensim.models import Word2Vec
from pathlib import Path
from typing import Tuple, Dict, List
from config import PATHS, LABEL_MAPPING


class ModelHandler:
    """Singleton class for model management"""
    
    _instance = None
    _skipgram_model = None
    _svm_model = None
    _is_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelHandler, cls).__new__(cls)
        return cls._instance
    
    def load_models(self) -> bool:
        """
        Load Skip-Gram and SVM models from disk
        
        Returns:
            True if successful, False otherwise
        """
        if self._is_loaded:
            return True
        
        try:
            # Load Skip-Gram model
            skipgram_path = Path(PATHS['skipgram_model'])
            if not skipgram_path.exists():
                raise FileNotFoundError(f"Skip-Gram model not found: {skipgram_path}")
            
            self._skipgram_model = Word2Vec.load(str(skipgram_path))
            
            # Load SVM model
            svm_path = Path(PATHS['svm_model'])
            if not svm_path.exists():
                raise FileNotFoundError(f"SVM model not found: {svm_path}")
            
            self._svm_model = joblib.load(str(svm_path))
            
            self._is_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def get_models(self) -> Tuple:
        """
        Get loaded models
        
        Returns:
            Tuple of (skipgram_model, svm_model)
        """
        if not self._is_loaded:
            self.load_models()
        return self._skipgram_model, self._svm_model
    
    def get_model_info(self) -> Dict:
        """
        Get model information
        
        Returns:
            Dictionary with model stats
        """
        if not self._is_loaded:
            self.load_models()
        
        return {
            'vector_size': self._skipgram_model.vector_size if self._skipgram_model else 0,
            'vocab_size': len(self._skipgram_model.wv) if self._skipgram_model else 0,
            'window': self._skipgram_model.window if self._skipgram_model else 0,
            'epochs': self._skipgram_model.epochs if self._skipgram_model else 0,
            'classes': list(self._svm_model.classes_) if self._svm_model and hasattr(self._svm_model, 'classes_') else []
        }


# Global instance
_model_handler = ModelHandler()


def load_models() -> Tuple:
    """
    Load and return models
    
    Returns:
        Tuple of (skipgram_model, svm_model)
    """
    return _model_handler.get_models()


def get_model_info() -> Dict:
    """
    Get model information
    
    Returns:
        Dictionary with model information
    """
    return _model_handler.get_model_info()


def doc_to_vector(tokens: List[str], skipgram_model) -> Tuple[np.ndarray, int, int]:
    """
    Convert document tokens to vector using mean word embedding
    
    Args:
        tokens: List of word tokens
        skipgram_model: Trained Word2Vec model
        
    Returns:
        Tuple of (document_vector, matched_count, oov_count)
    """
    if not tokens or not skipgram_model:
        vector_size = skipgram_model.vector_size if skipgram_model else 150
        return np.zeros(vector_size), 0, len(tokens)
    
    matched_vectors = []
    matched_count = 0
    oov_count = 0
    
    for token in tokens:
        if not token:
            continue
        
        # Check if word in vocabulary
        if token in skipgram_model.wv:
            matched_vectors.append(skipgram_model.wv[token])
            matched_count += 1
        else:
            oov_count += 1
    
    # Calculate mean vector
    if len(matched_vectors) > 0:
        doc_vector = np.mean(matched_vectors, axis=0)
    else:
        doc_vector = np.zeros(skipgram_model.vector_size)
    
    return doc_vector, matched_count, oov_count


def predict_category(tokens: List[str]) -> Dict:
    """
    Predict category for given tokens
    
    Args:
        tokens: List of word tokens
        
    Returns:
        Dictionary with prediction results
    """
    skipgram_model, svm_model = load_models()
    
    # Convert to vector
    doc_vector, matched_count, oov_count = doc_to_vector(tokens, skipgram_model)
    
    # Reshape for prediction
    vector_2d = doc_vector.reshape(1, -1)
    
    # Predict
    prediction = svm_model.predict(vector_2d)[0]
    
    # Get probabilities
    probabilities = {}
    confidence = 0.0
    
    if hasattr(svm_model, 'predict_proba'):
        proba = svm_model.predict_proba(vector_2d)[0]
        for idx, class_label in enumerate(svm_model.classes_):
            label_name = LABEL_MAPPING.get(class_label, str(class_label))
            probabilities[label_name] = float(proba[idx])
        confidence = float(max(proba))
    
    elif hasattr(svm_model, 'decision_function'):
        decision = svm_model.decision_function(vector_2d)[0]
        # Apply sigmoid for binary classification
        if isinstance(decision, (int, float)):
            prob_positive = 1 / (1 + np.exp(-decision))
            prob_negative = 1 - prob_positive
            probabilities['Sport'] = float(prob_positive)
            probabilities['Finance'] = float(prob_negative)
            confidence = float(max(prob_positive, prob_negative))
    
    # Map prediction to label
    predicted_label = LABEL_MAPPING.get(prediction, str(prediction))
    
    return {
        'prediction': predicted_label,
        'confidence': confidence * 100,  # Convert to percentage
        'probabilities': probabilities,
        'matched_tokens': matched_count,
        'oov_tokens': oov_count,
        'total_tokens': len(tokens),
        'vocab_coverage': (matched_count / len(tokens) * 100) if tokens else 0
    }
