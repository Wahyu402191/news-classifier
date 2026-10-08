"""
Web scraping utilities for extracting news articles
"""

import re
import trafilatura
from typing import Dict, Optional
from config import SCRAPER_CONFIG


def clean_html_content(raw_text: str) -> str:
    """
    Clean extracted text content by removing noise and unnecessary elements
    
    Args:
        raw_text: Raw extracted text from HTML
        
    Returns:
        Cleaned text content
    """
    if not raw_text:
        return ""
    
    lines = raw_text.split("\n")
    cleaned_paragraphs = []
    
    # Patterns untuk deteksi noise
    date_pattern = re.compile(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{2}:\d{2}\s*(WIB|WITA|WIT)\b",
        re.IGNORECASE
    )
    
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
    
    # Gabungkan paragraf
    full_text = "\n\n".join(cleaned_paragraphs)
    
    # Remove URLs
    full_text = re.sub(r"https?://\S+|www\.\S+", "", full_text)
    
    # Remove multiple spaces
    full_text = re.sub(r"\s+", " ", full_text).strip()
    
    return full_text


def scrape_article(url: str) -> Dict[str, Optional[str]]:
    """
    Extract news article content and metadata from URL
    
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
        # Download HTML with custom headers to avoid blocking
        import urllib.request
        
        # Create request with user agent
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': SCRAPER_CONFIG['user_agent']
            }
        )
        
        # Download page
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
        
        # Extract main content
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=False,  # Enable fallback for better extraction
            deduplicate=True
        )
        
        if not text:
            return {
                'url': url,
                'error': 'No content extracted from page. The page might be protected or have unusual structure.'
            }
        
        # Extract metadata
        metadata = trafilatura.extract_metadata(downloaded)
        
        # Clean content
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
    Validate if URL is properly formatted
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False
    
    url = url.strip()
    
    # Check if starts with http/https
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Basic URL pattern check
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    return bool(url_pattern.match(url))
