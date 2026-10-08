# Detik News Classifier - Streamlit Application

Web application untuk klasifikasi otomatis artikel berita Detikcom menggunakan Word2Vec Skip-Gram dan Support Vector Machine (SVM).

## Fitur Utama

- **Dual Input Mode**: Input URL atau paste teks langsung
- **Real-time Scraping**: Ekstraksi otomatis konten berita dari URL
- **NLP Pipeline**: Text preprocessing dengan Sastrawi (Bahasa Indonesia)
- **Word Embedding**: Skip-Gram Word2Vec (Dimensi 150, Window 3)
- **Classification**: Linear SVM dengan confidence scoring
- **Analytics Dashboard**: Visualisasi distribusi data dan performa model
- **Professional UI**: Clean, minimalist design tanpa emoji berlebihan

## Teknologi Stack

- **Frontend**: Streamlit 1.28+
- **ML/NLP**: Gensim (Word2Vec), Scikit-learn (SVM), Sastrawi
- **Web Scraping**: Trafilatura
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly

## Dataset

- **Training Data**: 180 artikel berita (90 Sport + 90 Finance)
- **Source**: Detikcom (hasil web scraping)
- **Preprocessing**: Sastrawi stopword removal & stemming
- **Split**: 80% training (144 docs), 20% testing (36 docs)

## Model Performance

- **Test Accuracy**: 97.2%
- **Sport Precision**: 96.7%
- **Finance Precision**: 97.8%
- **Model Size**: ~5.2 MB (Skip-Gram) + 68 KB (SVM)

## Installation

```bash
# Clone repository
git clone <repository-url>
cd news-classifier-streamlit

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## Deployment

### Streamlit Cloud (Gratis)

1. Push code ke GitHub
2. Login ke [share.streamlit.io](https://share.streamlit.io)
3. Klik "New app"
4. Select repository
5. Main file: `app.py`
6. Deploy!

**Link hasil**: `https://username-news-classifier.streamlit.app`

## Struktur Folder

```
news-classifier-streamlit/
├── app.py                      # Main Streamlit application
├── utils/
│   ├── scraper.py             # Web scraping utilities
│   ├── preprocessor.py        # Text preprocessing pipeline
│   ├── model_handler.py       # Model loading & prediction
│   └── visualizer.py          # Data visualization functions
├── models/
│   ├── skipgram_model.model   # Trained Skip-Gram Word2Vec
│   └── svm_classifier.joblib  # Trained SVM classifier
├── data/
│   ├── detik_sport_90.csv     # Sport dataset (90 articles)
│   └── detik_finance_90.csv   # Finance dataset (90 articles)
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## Configuration

Edit `config.py` untuk mengubah parameter:

```python
MODEL_CONFIG = {
    'vector_size': 150,
    'window': 3,
    'min_count': 2,
    'epochs': 50
}
```

## API Endpoints (untuk referensi)

Aplikasi ini menggunakan Streamlit (tidak ada REST API), namun memiliki fungsi-fungsi yang setara:

- `scrape_article(url)` - Ekstraksi konten dari URL
- `preprocess_text(text)` - Cleaning & preprocessing
- `classify_text(text)` - Prediksi kategori berita

## Credits

- **Developer**: Wahyu Pratama (230411100058)
- **Institution**: Universitas Trunojoyo Madura
- **Course**: Penambangan Web (Web Mining)
- **Year**: 2026

## License

Educational purpose only. Dataset © Detikcom.
