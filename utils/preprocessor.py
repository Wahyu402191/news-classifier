"""
Modul preprocessing teks menggunakan Sastrawi NLP library
Pipeline: noise removal -> stopword removal -> stemming -> tokenization
"""

import re
from typing import List
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


# Singleton pattern untuk efisiensi (load Sastrawi hanya 1x)
_stopword_remover = None
_stemmer = None


def get_stopword_remover():
    """Ambil atau buat instance stopword remover (singleton)"""
    global _stopword_remover
    if _stopword_remover is None:
        factory = StopWordRemoverFactory()
        _stopword_remover = factory.create_stop_word_remover()  # Load 750+ stopwords Indonesia
    return _stopword_remover


def get_stemmer():
    """Ambil atau buat instance stemmer (singleton)"""
    global _stemmer
    if _stemmer is None:
        factory = StemmerFactory()
        _stemmer = factory.create_stemmer()  # Load stemmer Indonesia (berlari -> lari)
    return _stemmer


def clean_noise(text: str) -> str:
    """
    Hapus noise dari teks (HTML tags, special characters, watermark, dll)
    Step: hapus [Gambas], hapus URL, lowercase, hapus non-alphabet
    
    Args:
        text: Teks input
        
    Returns:
        Teks yang sudah bersih
    """
    if not text:
        return ""
    
    # Hapus tag [Gambas:Video] dan sejenisnya
    text = re.sub(r"\[Gambas:.*?\]", " ", text)
    
    # Hapus rekomendasi redaksi (Lihat juga, Baca juga, Simak Video)
    text = re.sub(r"(Lihat juga Video:|Baca juga:|Simak Video:).*?(\n|$)", " ", text)
    
    # Hapus dateline kota (JAKARTA - ...)
    text = re.sub(r"^[A-Z\s]+-\s*", " ", text)
    
    # Hapus watermark (detikcom, detikSport, detikFinance)
    text = re.sub(r"(detikcom|detikSport|detikFinance)", " ", text, flags=re.IGNORECASE)
    
    # Ubah ke lowercase
    text = text.lower()
    
    # Hapus karakter non-alphabet (hanya simpan huruf a-z dan spasi)
    text = re.sub(r"[^a-z\s]", " ", text)
    
    # Normalize whitespace (ganti multiple spasi jadi 1 spasi)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def remove_stopwords_and_stem(text: str) -> str:
    """
    Hapus stopwords Indonesia dan lakukan stemming
    Stopwords: kata umum seperti "yang", "di", "ke", "untuk", dll (750+ kata)
    Stemming: ubah kata ke bentuk dasar (berlari -> lari, bermain -> main)
    
    Args:
        text: Teks input
        
    Returns:
        Teks setelah stopword removal dan stemming
    """
    if not text:
        return ""
    
    # Hapus stopwords
    stopword_remover = get_stopword_remover()
    text = stopword_remover.remove(text)
    
    # Stemming (ubah ke bentuk dasar)
    stemmer = get_stemmer()
    text = stemmer.stem(text)
    
    return text


def preprocess_text(text: str) -> str:
    """
    Pipeline preprocessing lengkap
    Step 1: Bersihkan noise
    Step 2: Hapus stopwords dan stemming
    
    Args:
        text: Raw input text
        
    Returns:
        Teks hasil preprocessing (siap untuk tokenisasi)
    """
    # Step 1: Bersihkan noise
    cleaned = clean_noise(text)
    
    # Step 2: Hapus stopwords dan stemming
    processed = remove_stopwords_and_stem(cleaned)
    
    return processed


def tokenize_text(text: str) -> List[str]:
    """
    Tokenisasi teks yang sudah di-preprocess menjadi list kata
    Contoh: "bola basket final" -> ["bola", "basket", "final"]
    
    Args:
        text: Teks yang sudah di-preprocess
        
    Returns:
        List token (kata-kata)
    """
    if not text:
        return []
    
    tokens = [word.strip() for word in text.split() if word.strip()]
    return tokens


def get_text_statistics(text: str) -> dict:
    """
    Hitung statistik teks (jumlah karakter, kata, kalimat, rata-rata panjang kata)
    
    Args:
        text: Teks input
        
    Returns:
        Dictionary berisi statistik
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
