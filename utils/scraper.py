"""
Modul untuk scraping artikel berita dari web
Menggunakan trafilatura library untuk ekstraksi konten
"""

import re
import trafilatura
from typing import Dict, Optional
from config import SCRAPER_CONFIG


def clean_html_content(raw_text: str) -> str:
    """
    Bersihkan teks hasil ekstraksi dari noise dan elemen yang tidak perlu
    Hapus: tanggal pendek, dateline kota, URL, line kosong
    
    Args:
        raw_text: Raw extracted text from HTML
        
    Returns:
        Cleaned text content
    """
    if not raw_text:
        return ""
    
    lines = raw_text.split("\n")
    cleaned_paragraphs = []
    
    # Regex pattern untuk deteksi noise (tanggal, waktu, dateline)
    date_pattern = re.compile(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{2}:\d{2}\s*(WIB|WITA|WIT)\b",
        re.IGNORECASE
    )
    
    # Pattern dateline kota (contoh: JAKARTA - ...)
    dateline_pattern = re.compile(
        r"^[A-Z\s,./()\-]+--?\s*|^[A-Z\s,./()\-]+\s*-\s*"
    )
    
    for line in lines:
        text = line.strip()
        
        # Skip empty lines
        if not text:
            continue
        
        words = text.split()
        
        # Skip lines yang terlalu pendek
        if len(words) < 5:
            continue
        
        # Skip lines yang hanya tanggal/waktu
        if date_pattern.search(text) and len(words) < 8:
            continue
        
        # Skip lines yang tidak berakhir dengan tanda baca
        if not text.endswith((".", '"', "'", "!", "?", "»", ")")):
            continue
        
        # Remove dateline prefix (JAKARTA - ...)
        text = dateline_pattern.sub("", text)
        
        cleaned_paragraphs.append(text)
    
    # Gabungkan semua paragraf yang sudah dibersihkan
    full_text = "\n\n".join(cleaned_paragraphs)
    
    # Hapus semua URL dari teks
    full_text = re.sub(r"https?://\S+|www\.\S+", "", full_text)
    
    # Hapus multiple spasi (ganti dengan 1 spasi)
    full_text = re.sub(r"\s+", " ", full_text).strip()
    
    return full_text


def scrape_article(url: str) -> Dict[str, Optional[str]]:
    """
    Ekstrak konten artikel dan metadata dari URL
    Return: dictionary berisi title, author, date, content, error
    
    Args:
        url: Article URL to scrape
        
    Returns:
        Dictionary containing article data:
        - url: Original URL
        - title: Article title
        - author: Article author
        - date: Publication date
        - content: Cleaned article content
        - error: Error message (if any)
    """
    try:
        # Download HTML dengan custom headers agar tidak di-block oleh website
        import urllib.request
        
        # Buat request dengan User-Agent (agar terlihat seperti browser biasa)
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': SCRAPER_CONFIG['user_agent']
            }
        )
        
        # Download halaman web (timeout 10 detik)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                downloaded = response.read().decode('utf-8')
        except Exception as download_error:
            return {
                'url': url,
                'error': f'Failed to download page: {str(download_error)}'
            }
        
        if not downloaded:
            return {
                'url': url,
                'error': 'Failed to download page content'
            }
        
        # Ekstrak konten utama artikel menggunakan trafilatura
        text = trafilatura.extract(
            downloaded,
            include_comments=False,  # Jangan ambil komentar
            include_tables=False,    # Jangan ambil tabel
            no_fallback=False,       # Gunakan fallback extraction kalau gagal
            deduplicate=True         # Hapus duplikasi konten
        )
        
        if not text:
            return {
                'url': url,
                'error': 'No content extracted from page. The page might be protected or have unusual structure.'
            }
        
        # Ekstrak metadata artikel (title, author, date)
        metadata = trafilatura.extract_metadata(downloaded)
        
        # Bersihkan konten dari noise
        cleaned_content = clean_html_content(text)
        
        if not cleaned_content or len(cleaned_content) < 100:
            # If cleaned content too short, use raw text
            cleaned_content = text if len(text) >= 100 else None
            
        if not cleaned_content:
            return {
                'url': url,
                'error': 'Content too short or empty after extraction'
            }
        
        return {
            'url': url,
            'title': metadata.title if metadata and metadata.title else 'No title',
            'author': metadata.author if metadata and metadata.author else 'Unknown',
            'date': metadata.date if metadata and metadata.date else 'Unknown',
            'content': cleaned_content,
            'word_count': len(cleaned_content.split()),
            'error': None
        }
        
    except Exception as e:
        return {
            'url': url,
            'error': f'Scraping error: {str(e)}'
        }


def validate_url(url: str) -> bool:
    """
    Validasi apakah URL sudah benar formatnya
    Cek: harus mulai dengan http/https, ada domain, struktur URL valid
    
    Args:
        url: String URL yang akan divalidasi
        
    Returns:
        True jika valid, False jika tidak valid
    """
    if not url:
        return False
    
    url = url.strip()
    
    # Cek apakah URL dimulai dengan http:// atau https://
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Regex pattern untuk validasi struktur URL
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    return bool(url_pattern.match(url))
