"""
Modul untuk loading model dan melakukan prediksi
Load Skip-Gram Word2Vec dan SVM, lalu klasifikasi teks
"""

import numpy as np
import joblib
from gensim.models import Word2Vec
from pathlib import Path
from typing import Tuple, Dict, List
from config import PATHS, LABEL_MAPPING


class ModelHandler:
    """Singleton class untuk manajemen model (hanya load 1x)"""
    
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
        Load model Skip-Gram dan SVM dari folder models/
        Return True jika berhasil, False jika gagal
        """
        if self._is_loaded:
            return True  # Sudah di-load, tidak perlu load lagi
        
        try:
            # Load Skip-Gram Word2Vec model
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
        Ambil informasi model (dimensi vektor, vocab size, window, dll)
        Return dictionary berisi spesifikasi model
        """
        if not self._is_loaded:
            self.load_models()
        
        return {
            'vector_size': self._skipgram_model.vector_size if self._skipgram_model else 0,  # Dimensi embedding
            'vocab_size': len(self._skipgram_model.wv) if self._skipgram_model else 0,  # Jumlah kata
            'window': self._skipgram_model.window if self._skipgram_model else 0,  # Context window
            'epochs': self._skipgram_model.epochs if self._skipgram_model else 0,  # Training epochs
            'classes': list(self._svm_model.classes_) if self._svm_model and hasattr(self._svm_model, 'classes_') else []  # Kategori (Sport/Finance)
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
    Ubah dokumen (list token) menjadi vektor menggunakan mean word embedding
    Proses: ambil vektor setiap kata, lalu rata-rata (mean pooling)
    
    Args:
        tokens: List kata hasil tokenisasi
        skipgram_model: Model Skip-Gram yang sudah di-load
        
    Returns:
        Tuple (document_vector, matched_count, oov_count)
        - document_vector: vektor dokumen hasil mean pooling
        - matched_count: jumlah kata yang ditemukan di vocabulary
        - oov_count: jumlah kata yang tidak ditemukan (out-of-vocabulary)
    """
    if not tokens or not skipgram_model:
        vector_size = skipgram_model.vector_size if skipgram_model else 150
        return np.zeros(vector_size), 0, len(tokens)
    
    matched_vectors = []  # Simpan vektor kata yang ditemukan
    matched_count = 0
    oov_count = 0
    
    for token in tokens:
        if not token:
            continue
        
        # Cek apakah kata ada di vocabulary Skip-Gram
        if token in skipgram_model.wv:
            matched_vectors.append(skipgram_model.wv[token])  # Ambil vektor kata
            matched_count += 1
        else:
            oov_count += 1  # Kata tidak dikenali
    
    # Hitung mean vector dari semua kata yang ditemukan
    if len(matched_vectors) > 0:
        doc_vector = np.mean(matched_vectors, axis=0)  # Mean pooling
    else:
        doc_vector = np.zeros(skipgram_model.vector_size)  # Zero vector jika tidak ada kata yang match
    
    return doc_vector, matched_count, oov_count


def predict_category(tokens: List[str]) -> Dict:
    """
    Prediksi kategori untuk list token yang diberikan
    Pipeline: tokens -> Skip-Gram embedding -> mean pooling -> SVM prediction
    
    Args:
        tokens: List kata hasil preprocessing
        
    Returns:
        Dictionary berisi:
        - prediction: kategori hasil prediksi (Sport/Finance)
        - confidence: confidence score dalam persen
        - probabilities: probabilitas setiap kategori
        - matched_tokens: jumlah kata yang match di vocabulary
        - oov_tokens: jumlah kata out-of-vocabulary
        - total_tokens: total kata
        - vocab_coverage: persentase coverage vocabulary
    """
    skipgram_model, svm_model = load_models()
    
    # Konversi dokumen ke vektor
    doc_vector, matched_count, oov_count = doc_to_vector(tokens, skipgram_model)
    
    # Reshape untuk input SVM (harus 2D)
    vector_2d = doc_vector.reshape(1, -1)
    
    # Prediksi kategori menggunakan SVM
    prediction = svm_model.predict(vector_2d)[0]  # Output: 0 (Finance) atau 1 (Sport)
    
    # Ambil probabilitas dari SVM
    probabilities = {}
    confidence = 0.0
    
    # Jika SVM support probability (kernel linear dengan probability=True)
    if hasattr(svm_model, 'predict_proba'):
        proba = svm_model.predict_proba(vector_2d)[0]  # Probability setiap kelas
        for idx, class_label in enumerate(svm_model.classes_):
            label_name = LABEL_MAPPING.get(class_label, str(class_label))  # Mapping 0->Finance, 1->Sport
            probabilities[label_name] = float(proba[idx])
        confidence = float(max(proba))  # Confidence = probabilitas tertinggi
    
    # Fallback: jika tidak ada predict_proba, gunakan decision_function
    elif hasattr(svm_model, 'decision_function'):
        decision = svm_model.decision_function(vector_2d)[0]
        # Apply sigmoid untuk binary classification
        if isinstance(decision, (int, float)):
            prob_positive = 1 / (1 + np.exp(-decision))
            prob_negative = 1 - prob_positive
            probabilities['Sport'] = float(prob_positive)
            probabilities['Finance'] = float(prob_negative)
            confidence = float(max(prob_positive, prob_negative))
    
    # Mapping hasil prediksi ke label (0 -> Finance, 1 -> Sport)
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
