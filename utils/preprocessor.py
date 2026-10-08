"""
Text preprocessing utilities using Sastrawi NLP library
"""

import re
from typing import List
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


# Initialize Sastrawi components (singleton pattern)
_stopword_remover = None
_stemmer = None


def get_stopword_remover():
    """Get or create stopword remover instance"""
    global _stopword_remover
    if _stopword_remover is None:
        factory = StopWordRemoverFactory()
        _stopword_remover = factory.create_stop_word_remover()
    return _stopword_remover


def get_stemmer():
    """Get or create stemmer instance"""
    global _stemmer
    if _stemmer is None:
        factory = StemmerFactory()
        _stemmer = factory.create_stemmer()
    return _stemmer


def clean_noise(text: str) -> str:
    """
    Remove noise from text (HTML tags, special characters, etc)
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove [Gambas:...] tags
    text = re.sub(r"\[Gambas:.*?\]", " ", text)
    
    # Remove redaksi recommendations
    text = re.sub(r"(Lihat juga Video:|Baca juga:|Simak Video:).*?(\n|$)", " ", text)
    
    # Remove city dateline (JAKARTA - ...)
    text = re.sub(r"^[A-Z\s]+-\s*", " ", text)
    
    # Remove watermarks
    text = re.sub(r"(detikcom|detikSport|detikFinance)", " ", text, flags=re.IGNORECASE)
    
    # Lowercase
    text = text.lower()
    
    # Remove non-alphabetic characters
    text = re.sub(r"[^a-z\s]", " ", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def remove_stopwords_and_stem(text: str) -> str:
    """
    Remove Indonesian stopwords and apply stemming
    
    Args:
        text: Input text
        
    Returns:
        Processed text
    """
    if not text:
        return ""
    
    # Remove stopwords
    stopword_remover = get_stopword_remover()
    text = stopword_remover.remove(text)
    
    # Apply stemming
    stemmer = get_stemmer()
    text = stemmer.stem(text)
    
    return text


def preprocess_text(text: str) -> str:
    """
    Complete preprocessing pipeline
    
    Args:
        text: Raw input text
        
    Returns:
        Fully preprocessed text
    """
    # Step 1: Clean noise
    cleaned = clean_noise(text)
    
    # Step 2: Remove stopwords and stem
    processed = remove_stopwords_and_stem(cleaned)
    
    return processed


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize preprocessed text into list of words
    
    Args:
        text: Preprocessed text
        
    Returns:
        List of tokens
    """
    if not text:
        return []
    
    tokens = [word.strip() for word in text.split() if word.strip()]
    return tokens


def get_text_statistics(text: str) -> dict:
    """
    Get statistics about the text
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with statistics
    """
    if not text:
        return {
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0
        }
    
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    
    return {
        'char_count': len(text),
        'word_count': len(words),
        'sentence_count': len([s for s in sentences if s.strip()]),
        'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
    }
