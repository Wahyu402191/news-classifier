# 📰 Detik News Classifier

Aplikasi klasifikasi otomatis artikel berita Detikcom menggunakan **Skip-Gram Word2Vec** dan **Support Vector Machine (SVM)**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Fitur Utama

- ✅ **Dual Input Mode**: URL scraping atau text input langsung
- ✅ **NLP Processing**: Sastrawi (stopword removal + stemming Bahasa Indonesia)
- ✅ **Skip-Gram Word2Vec**: 150-dimensional word embedding, window size 3
- ✅ **SVM Classification**: Linear SVM dengan probability output
- ✅ **Interactive Visualizations**: Plotly charts (probability bars, token analysis)
- ✅ **Professional UI**: Clean, minimal design (blue/white theme)
- ✅ **Real-time Processing**: 2-3 detik per artikel
- ✅ **Detailed Analytics**: 4 tabs (Metadata, Content, Preprocessing, Tokens)

---

## 📊 Model Performance

- **Akurasi**: ~97% (pada test set)
- **Dataset**: 180 artikel (90 Sport + 90 Finance)
- **Split**: 80% training, 20% testing
- **Vector Dimension**: 150D
- **Vocabulary Size**: ~4,015 kata

---

## 🚀 Quick Start

### Lokal (Development)

```bash
# 1. Clone repository
git clone https://github.com/Wahyu402191/news-classifier-streamlit.git
cd news-classifier-streamlit

# 2. Create conda environment
conda create -n newsclassifier python=3.11 -y
conda activate newsclassifier

# 3. Install dependencies
conda install -c conda-forge gensim scikit-learn pandas numpy -y
pip install streamlit PySastrawi trafilatura plotly

# 4. Run aplikasi
streamlit run app.py
```

Buka browser: `http://localhost:8501`

---

## 🌐 Deploy ke Streamlit Cloud (Gratis!)

1. Push repository ke GitHub (sudah ada di `Wahyu402191/news-classifier-streamlit`)
2. Buka https://share.streamlit.io
3. Sign in dengan GitHub
4. New app → Pilih repository → Deploy!
5. Aplikasi akan online di: `https://[app-name].streamlit.app`

**Panduan lengkap:** Baca `DEPLOY_STREAMLIT_CLOUD.md`

---

## 📁 Struktur Project

```
news-classifier-streamlit/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .python-version             # Python version (3.11)
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── scraper.py             # Web scraping (trafilatura)
│   ├── preprocessor.py        # NLP preprocessing (Sastrawi)
│   ├── model_handler.py       # ML model loading & prediction
│   └── visualizer.py          # Plotly visualizations
│
├── models/                     # Machine Learning models
│   ├── skipgram_model.model   # Word2Vec Skip-Gram (6.2 MB)
│   └── svm_classifier.joblib  # SVM classifier (74 KB)
│
├── data/                       # Training datasets
│   ├── detik_sport_90.csv     # 90 artikel Sport
│   └── detik_finance_90.csv   # 90 artikel Finance
│
├── .streamlit/                 # Streamlit config
│   └── config.toml            # Theme & server settings
│
└── docs/                       # Documentation
    ├── DOKUMENTASI.md         # Dokumentasi lengkap (Bahasa Indonesia)
    ├── CARA_PENGGUNAAN.md     # User guide
    ├── DEPLOY_STREAMLIT_CLOUD.md
    └── INSTALL_MANUAL.md
```

---

## 🛠️ Teknologi

| Kategori | Library | Versi |
|----------|---------|-------|
| **Framework** | Streamlit | ≥1.28.0 |
| **ML/NLP** | Gensim | ≥4.3.0 |
| | Scikit-learn | ≥1.3.0 |
| | PySastrawi | ≥1.2.0 |
| **Data** | Pandas | ≥2.0.0 |
| | NumPy | ≥1.24.0 |
| **Scraping** | Trafilatura | ≥1.6.0 |
| **Visualization** | Plotly | ≥5.17.0 |
| **Utils** | Joblib | ≥1.3.0 |

---

## 📖 Cara Menggunakan

### Mode 1: URL Input
1. Paste URL artikel Detikcom
2. Klik "Classify Article"
3. Lihat hasil klasifikasi

### Mode 2: Text Input
1. Klik tab "Text Input"
2. Paste/ketik teks artikel (min 50 karakter)
3. Klik "Classify Text"
4. Lihat hasil klasifikasi

### Output
- **Category**: Sport atau Finance
- **Confidence**: Persentase keyakinan model (0-100%)
- **Vocabulary Coverage**: Persentase token yang dikenali
- **Visualizations**: Probability bar chart, token coverage pie chart
- **Details**: 4 tabs (Metadata, Content Preview, Preprocessing, Token Analysis)

---

## 🔬 Machine Learning Pipeline

```
Input Text
    ↓
1. Noise Removal (HTML, special chars, numbers)
    ↓
2. Stopword Removal (Sastrawi - 750+ stopwords)
    ↓
3. Stemming (Sastrawi - Indonesian stemmer)
    ↓
4. Tokenization (split into words)
    ↓
5. Word Embedding (Skip-Gram → 150D vectors)
    ↓
6. Document Vector (mean pooling)
    ↓
7. SVM Classification (Linear SVM)
    ↓
Output: Category + Probability
```

---

## 📝 Model Details

### Skip-Gram Word2Vec
- **Architecture**: Skip-gram (predicts context from word)
- **Dimension**: 150
- **Window**: 3
- **Min count**: 2
- **Epochs**: 50
- **Vocabulary**: ~4,015 unique words

### SVM Classifier
- **Kernel**: Linear
- **C**: 1.0
- **Probability**: True
- **Training accuracy**: ~97%

---

## 🎓 Credits

**Developer:** Wahyu Pratama  
**NPM:** 230411100058  
**Institution:** Universitas Trunojoyo Madura  
**Course:** Penambangan Web (Web Mining)  
**Year:** 2026

**Dataset Source:** Detikcom (educational purposes)  
**Framework:** Streamlit (streamlit.io)

---

## 📄 License

MIT License - Feel free to use for educational purposes.

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

- **Documentation**: Baca `DOKUMENTASI.md` untuk dokumentasi lengkap
- **Deployment Guide**: `DEPLOY_STREAMLIT_CLOUD.md`
- **User Guide**: `CARA_PENGGUNAAN.md`
- **Issues**: Open issue di GitHub

---

## 🌟 Acknowledgments

Terinspirasi dari best practices dalam:
- Natural Language Processing (NLP)
- Text Classification
- Web Mining
- Streamlit App Development

---

**⭐ Star this repository jika bermanfaat!**

Last updated: October 8, 2026
