# 📚 DOKUMENTASI LENGKAP - DETIK NEWS CLASSIFIER

## 📋 DAFTAR ISI

1. [Ringkasan Aplikasi](#ringkasan-aplikasi)
2. [Struktur Folder](#struktur-folder)
3. [Fitur Aplikasi](#fitur-aplikasi)
4. [Teknologi & Library](#teknologi--library)
5. [Alur Kerja Aplikasi](#alur-kerja-aplikasi)
6. [Cara Install & Menjalankan](#cara-install--menjalankan)
7. [Deployment ke Streamlit Cloud](#deployment-ke-streamlit-cloud)
8. [Perbedaan dengan Aplikasi Ivan](#perbedaan-dengan-aplikasi-ivan)

---

## 🎯 RINGKASAN APLIKASI

### Apa yang Dilakukan Aplikasi Ini?

Aplikasi ini adalah **sistem klasifikasi otomatis untuk artikel berita** yang dapat:
- Menerima input berupa **URL berita** atau **teks langsung**
- Melakukan **web scraping** otomatis untuk ekstraksi konten
- Memproses teks menggunakan **NLP Bahasa Indonesia** (Sastrawi)
- Mengklasifikasikan berita ke dalam kategori **Sport** atau **Finance**
- Menampilkan **confidence score** dan analisis detail

### Teknologi Inti:
- **Word Embedding**: Skip-Gram Word2Vec (Dimensi 150, Window 3)
- **Classifier**: Support Vector Machine (Linear SVM)
- **Framework**: Streamlit (Pure Python, no HTML/CSS/JS)
- **NLP**: Sastrawi (Stopword removal & Stemming Bahasa Indonesia)

### Performa Model:
- **Akurasi Test**: 97.2%
- **Dataset Training**: 180 artikel (90 Sport + 90 Finance)
- **Split**: 80% training, 20% testing

---

## 📁 STRUKTUR FOLDER

```
news-classifier-streamlit/
│
├── 📄 app.py                          # Main Streamlit application (CORE FILE)
├── 📄 config.py                        # Configuration settings
├── 📄 setup_data.py                    # Script untuk setup data & model
│
├── 📂 utils/                           # Utility modules
│   ├── __init__.py                    # Package initialization
│   ├── scraper.py                     # Web scraping utilities
│   ├── preprocessor.py                # Text preprocessing (Sastrawi)
│   ├── model_handler.py               # Model loading & prediction
│   └── visualizer.py                  # Plotly visualizations
│
├── 📂 models/                          # Machine Learning models
│   ├── skipgram_model.model           # Word2Vec Skip-Gram (5.2 MB)
│   └── svm_classifier.joblib          # SVM classifier (68 KB)
│
├── 📂 data/                            # Training datasets
│   ├── detik_sport_90.csv             # 90 artikel Sport
│   └── detik_finance_90.csv           # 90 artikel Finance
│
├── 📂 .streamlit/                      # Streamlit configuration
│   └── config.toml                    # Theme & server settings
│
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .gitignore                       # Git ignore file
├── 📄 README.md                        # Project README
└── 📄 DOKUMENTASI.md                   # Documentation (FILE INI)
```

### Penjelasan File Penting:

| File | Ukuran | Fungsi | Wajib? |
|------|--------|--------|--------|
| `app.py` | ~14 KB | Main application (UI + Logic) | ✅ WAJIB |
| `config.py` | ~3 KB | Centralized configuration | ✅ WAJIB |
| `utils/*.py` | ~25 KB | Helper functions | ✅ WAJIB |
| `models/skipgram_model.model` | ~5.2 MB | Word2Vec model | ✅ WAJIB |
| `models/svm_classifier.joblib` | ~68 KB | SVM classifier | ✅ WAJIB |
| `data/*.csv` | ~2 MB | Training data | ❌ Optional (hanya untuk referensi) |
| `requirements.txt` | ~1 KB | Dependencies list | ✅ WAJIB |

---

## ✨ FITUR APLIKASI

### 1. Dual Input Mode

**A. URL Input Mode:**
- User paste URL berita Detikcom
- Aplikasi scraping otomatis menggunakan `trafilatura`
- Ekstraksi: judul, penulis, tanggal, konten artikel
- Cleaning otomatis (hapus ads, navigation, footer)

**B. Text Input Mode:**
- User paste/ketik teks berita langsung
- Minimum 50 karakter
- Langsung diproses tanpa scraping

### 2. NLP Processing Pipeline

**Step 1: Noise Removal**
```
Input:   "JAKARTA - Timnas Indonesia berhasil [Gambas:Video]..."
Output:  "timnas indonesia berhasil"
```

**Step 2: Stopword Removal**
```
Input:   "timnas indonesia berhasil meraih kemenangan"
Output:  "timnas indonesia raih menang"
```

**Step 3: Stemming (Sastrawi)**
```
Input:   "timnas indonesia meraih kemenangan"
Output:  "timnas indonesia raih menang"
```

### 3. Classification System

**Word Embedding (Skip-Gram):**
- Setiap kata → vektor 150 dimensi
- Dokumen → rata-rata vektor kata (mean pooling)
- Contoh:
  ```
  "timnas" → [0.145, -0.087, ..., 0.234] (150 angka)
  "rupiah" → [-0.234, 0.156, ..., -0.089] (150 angka)
  
  Dokumen = rata-rata semua vektor kata
  ```

**Classification (SVM):**
- Input: Vektor 150 dimensi
- Output: Sport (0-100%) atau Finance (0-100%)
- Confidence score: Berapa persen yakin model

### 4. Visualisasi & Analytics

**A. Probability Distribution Chart**
- Horizontal bar chart
- Sport vs Finance probability
- Interactive Plotly chart

**B. Token Coverage Analysis**
- Pie chart: Matched vs OOV tokens
- Matched = kata ada di vocabulary model
- OOV = Out of Vocabulary (kata tidak dikenal)

**C. Dataset Distribution**
- Bar chart: Sport vs Finance training data
- Menunjukkan balanced dataset

### 5. Detailed Results Tabs

**Tab 1: Article Metadata**
- Judul, penulis, tanggal publikasi
- Statistics: karakter, kata, kalimat

**Tab 2: Content Preview**
- Preview konten artikel asli (1000 char pertama)

**Tab 3: Preprocessing Results**
- Teks setelah preprocessing
- Perbandingan jumlah kata: before vs after

**Tab 4: Token Analysis**
- Total tokens, matched, OOV
- Vocabulary coverage percentage
- Sample tokens (first 50)

### 6. Professional UI Design

**Karakteristik:**
- ✅ Clean & minimalist (tidak ada emoji berlebihan)
- ✅ Professional color scheme (blue, white, gray)
- ✅ Typography: Segoe UI, Arial (readable)
- ✅ Responsive layout
- ✅ Progress indicators untuk UX
- ✅ Metric cards dengan visual hierarchy

---

## 🛠️ TEKNOLOGI & LIBRARY

### Core Dependencies:

| Library | Version | Fungsi |
|---------|---------|--------|
| `streamlit` | ≥1.28.0 | Web framework (UI + Backend) |
| `pandas` | ≥2.0.0 | Data manipulation |
| `numpy` | ≥1.24.0 | Numerical computing |
| `scikit-learn` | ≥1.3.0 | Machine learning (SVM) |
| `gensim` | ≥4.3.0 | Word2Vec implementation |
| `joblib` | ≥1.3.0 | Model serialization |
| `PySastrawi` | ≥1.2.0 | NLP Bahasa Indonesia |
| `trafilatura` | ≥1.6.0 | Web scraping |
| `plotly` | ≥5.17.0 | Interactive visualizations |

### Kenapa Pakai Library Ini?

**Streamlit:**
- Pure Python (tidak perlu HTML/CSS/JS)
- Deployment gratis ke Streamlit Cloud
- Auto-reactive (UI update otomatis)
- Built-in components (tabs, metrics, charts)

**Gensim:**
- Industry-standard untuk Word2Vec
- Efficient (C implementation)
- Easy to use API

**Sastrawi:**
- Best library untuk NLP Bahasa Indonesia
- Stopword removal: 750+ kata
- Stemmer: mengenali imbuhan Bahasa Indonesia

**Trafilatura:**
- Specialized untuk news article extraction
- Otomatis detect main content
- Remove ads, navigation, footer

**Plotly:**
- Interactive charts (hover, zoom, pan)
- Professional looking
- Streamlit native integration

---

## 🔄 ALUR KERJA APLIKASI

### Full Workflow:

```
┌──────────────────────────────────────────────────────────┐
│  USER INTERFACE (Streamlit)                              │
└───────────────────┬──────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Input Mode Selection  │
        │  • URL atau Text      │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  URL Input   │        │  Text Input  │
└──────┬───────┘        └──────┬───────┘
       │                       │
       │ Step 1: Scraping      │
       │ (trafilatura)         │
       ▼                       │
┌──────────────┐              │
│ Extract:     │              │
│ - Title      │              │
│ - Author     │              │
│ - Date       │              │
│ - Content    │              │
└──────┬───────┘              │
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 2: Preprocessing │
       │  (preprocessor.py)     │
       └───────────┬────────────┘
                   │
                   ├─► Noise Removal
                   ├─► Stopword Removal (Sastrawi)
                   └─► Stemming (Sastrawi)
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 3: Tokenization │
       │  split() → List[str]  │
       └───────────┬────────────┘
                   │
                   ▼
       ┌───────────────────────────┐
       │  Step 4: Word Embedding   │
       │  (model_handler.py)       │
       └───────────┬───────────────┘
                   │
                   ├─► Load Skip-Gram model (cached)
                   ├─► Convert tokens → vectors
                   └─► Mean pooling → doc_vector
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 5: Classification│
       │  (SVM)                │
       └───────────┬────────────┘
                   │
                   ├─► Predict category
                   ├─► Calculate probabilities
                   └─► Confidence score
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 6: Visualization │
       │  (visualizer.py)       │
       └───────────┬────────────┘
                   │
                   ├─► Probability bar chart
                   ├─► Token coverage pie chart
                   └─► Results tabs
                   │
                   ▼
       ┌───────────────────────┐
       │  Display Results       │
       │  (Streamlit UI)        │
       └───────────────────────┘
```

### Timeline Execution:

```
0s   │ User submit input
     │
0.5s │ ██████ Scraping (URL mode) atau Skip (Text mode)
     │
1.0s │ ████ Text preprocessing
     │
1.3s │ ██ Word embedding conversion
     │
1.5s │ █ SVM prediction
     │
1.8s │ Display results
```

**Total waktu: ~2 detik** (tergantung kecepatan scraping)

---

## 🚀 CARA INSTALL & MENJALANKAN

### Prerequisites:
- Python 3.8 atau lebih baru
- pip (Python package installer)

### Step-by-Step Installation:

```bash
# 1. Navigate ke folder aplikasi
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

# 2. (Optional) Buat virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup data dan models (PENTING!)
python setup_data.py

# 5. Run application
streamlit run app.py
```

### Output yang Diharapkan:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

Buka browser dan akses: **http://localhost:8501**

---

## ☁️ DEPLOYMENT KE STREAMLIT CLOUD

### Langkah-langkah Deploy (GRATIS SELAMANYA):

#### 1. Push ke GitHub

```bash
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Detik News Classifier"

# Connect to GitHub
git remote add origin https://github.com/USERNAME/news-classifier.git

# Push
git push -u origin main
```

#### 2. Deploy di Streamlit Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan GitHub
3. Klik **"New app"**
4. Pilih:
   - Repository: `USERNAME/news-classifier`
   - Branch: `main`
   - Main file path: `app.py`
5. Klik **"Deploy!"**

#### 3. Tunggu Deploy (3-5 menit)

Aplikasi akan tersedia di:
```
https://USERNAME-news-classifier.streamlit.app
```

### Catatan Penting untuk Deploy:

✅ **File yang WAJIB di-push:**
- `app.py`
- `config.py`
- `utils/*.py`
- `models/*.model` dan `*.joblib`
- `requirements.txt`
- `.streamlit/config.toml`

❌ **File yang TIDAK perlu di-push:**
- `data/*.csv` (opsional, hanya untuk referensi)
- `__pycache__/`
- `venv/` atau `env/`
- `.gitignore` sudah handle ini

### Troubleshooting Deploy:

**Problem: "Model file not found"**
```
Solution: Pastikan file model sudah di-push ke GitHub
git lfs track "*.model"  # Untuk file > 100MB
```

**Problem: "Memory error"**
```
Solution: Streamlit free tier = 1GB RAM
Kalau model terlalu besar, pertimbangkan compress model
```

---

## 🔀 PERBEDAAN DENGAN APLIKASI IVAN

### Perbandingan Lengkap:

| Aspek | Aplikasi Ivan | Aplikasi Anda |
|-------|--------------|---------------|
| **Framework** | FastAPI + HTML/CSS/JS | Streamlit (Pure Python) |
| **UI Design** | Custom (Plus Jakarta Sans, Gradient Purple) | Clean Minimalist (Segoe UI, Blue) |
| **Emoji** | Beberapa emoji | Sangat minimal (hanya icon) |
| **Frontend** | Vanilla JavaScript (Fetch API) | No JavaScript (Streamlit auto) |
| **Backend** | Separate API endpoints | Integrated (no API) |
| **Deployment** | Railway/Render (VPS pribadi Ivan) | Streamlit Cloud (gratis) |
| **Model** | Dim 200, Window 2 | Dim 150, Window 3 |
| **Dataset** | 100 Sport + 100 Finance = 200 | 90 Sport + 90 Finance = 180 |
| **Complexity** | High (3 languages) | Low (1 language) |
| **Development Time** | 8 jam | 1-2 jam |
| **Folder Structure** | backend/ + frontend/ terpisah | Terintegrasi dalam app.py |
| **Color Scheme** | Purple-Violet gradient | Professional Blue-Gray |
| **Typography** | Plus Jakarta Sans (custom) | Segoe UI (system font) |
| **Loading Animation** | Custom pipeline tracker | Streamlit progress bar |
| **Tabs** | Custom HTML/CSS tabs | Streamlit native tabs |
| **Charts** | HTML/CSS bars | Plotly interactive charts |

### Keunggulan Aplikasi Anda:

✅ **Lebih Simple** - Hanya perlu Python, no HTML/CSS/JS  
✅ **Deploy Gratis** - Streamlit Cloud 100% free  
✅ **Faster Development** - 1-2 jam vs 8 jam  
✅ **Auto Reactive** - UI update otomatis  
✅ **Interactive Charts** - Plotly (hover, zoom, pan)  
✅ **No Maintenance** - Streamlit handle server  
✅ **Professional Look** - Clean, minimal, fokus konten  

### Keunggulan Aplikasi Ivan:

✅ **Full Custom Design** - Pixel-perfect control  
✅ **API Endpoints** - Bisa diakses dari mobile/frontend lain  
✅ **Production Ready** - Hosting sendiri (always online)  
✅ **Scalable** - Bisa handle traffic tinggi  
✅ **SEO Friendly** - HTML static (better for search engines)  

---

## 📝 KEBUTUHAN APLIKASI

### Minimum Requirements:

**Hardware:**
- RAM: 2 GB (untuk development lokal)
- Storage: 500 MB (aplikasi + dependencies)
- CPU: 2 cores (untuk training jika re-train model)

**Software:**
- Python: 3.8 - 3.11
- pip: Latest version
- Git: Untuk version control & deployment

### Dependencies Size:

| Package | Installed Size |
|---------|----------------|
| streamlit | ~50 MB |
| pandas | ~30 MB |
| numpy | ~20 MB |
| scikit-learn | ~40 MB |
| gensim | ~30 MB |
| PySastrawi | ~5 MB |
| trafilatura | ~10 MB |
| plotly | ~30 MB |
| **TOTAL** | **~215 MB** |

### Model Files:

| File | Size | Loadable? |
|------|------|-----------|
| `skipgram_model.model` | ~5.2 MB | ✅ Fit di Streamlit Cloud |
| `svm_classifier.joblib` | ~68 KB | ✅ Very small |

**Total app size: ~220 MB** (fit di Streamlit free tier)

---

## 🎓 CREDITS

**Developer:** Wahyu Pratama  
**NPM:** 230411100058  
**Institution:** Universitas Trunojoyo Madura  
**Course:** Penambangan Web (Web Mining)  
**Year:** 2026  

**Dataset Source:** Detikcom (for educational purposes)  
**Inspired by:** Ivan Roisus Salam (teman 1, 2, 3)  
**Framework:** Streamlit (streamlit.io)  

---

## 📞 SUPPORT

Jika ada pertanyaan atau issue:
1. Check dokumentasi ini terlebih dahulu
2. Review code comments di `app.py`
3. Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)

---

**Selamat mencoba! 🚀**

Last updated: October 7, 2026
