# Detik News Classifier

Aplikasi web untuk klasifikasi otomatis artikel berita Detikcom ke dalam kategori Sport atau Finance menggunakan Machine Learning.

## Deskripsi Aplikasi

Aplikasi ini menggunakan Natural Language Processing (NLP) dan Machine Learning untuk mengklasifikasikan artikel berita secara otomatis. Pengguna dapat memasukkan URL artikel atau teks langsung, kemudian sistem akan memproses dan memprediksi kategori berita tersebut (Sport atau Finance) beserta tingkat confidence-nya.

## Teknologi dan Framework

### Framework Utama
- **Streamlit**: Framework Python untuk membuat web aplikasi interaktif
  - Version: 1.28.0+
  - Digunakan untuk: Frontend dan Backend (all-in-one)
  - Deployment: Streamlit Cloud (gratis)

### Machine Learning Libraries
- **Gensim 4.3.0**: Library untuk training Word2Vec (Skip-Gram model)
- **scikit-learn 1.3.0**: Library untuk SVM classifier dan metrics
- **NumPy 1.24.0**: Library untuk komputasi array dan vektor
- **joblib 1.3.0**: Library untuk menyimpan/load model

### NLP Libraries
- **PySastrawi 1.2.0**: Library NLP Indonesia untuk:
  - Stopword removal (750+ stopwords bahasa Indonesia)
  - Stemming (mengubah kata ke bentuk dasar)
- **trafilatura 1.6.0**: Library untuk web scraping dan ekstraksi konten artikel

### Visualization
- **Plotly 5.17.0**: Library untuk membuat chart interaktif (bar chart, pie chart)

### Data Processing
- **Pandas 2.0.0**: Library untuk manipulasi data CSV

## Struktur Folder

```
news-classifier-streamlit/
├── app.py                    # File utama aplikasi (entry point)
├── config.py                 # Konfigurasi (model params, paths, colors)
├── requirements.txt          # Daftar dependencies Python
├── .python-version          # Python version untuk Streamlit Cloud (3.11.10)
├── .gitignore               # File yang diabaikan Git
├── run_app.bat              # Script untuk menjalankan aplikasi di Windows
│
├── data/                    # Dataset training
│   ├── detik_sport_90.csv   # 90 artikel Sport
│   └── detik_finance_90.csv # 90 artikel Finance
│
├── models/                  # Model Machine Learning
│   ├── skipgram_model.model # Skip-Gram Word2Vec (150D, Window 3)
│   └── svm_classifier.joblib # SVM classifier (linear kernel)
│
├── utils/                   # Modul utilitas
│   ├── __init__.py          # Init file untuk package
│   ├── scraper.py           # Web scraping dari URL
│   ├── preprocessor.py      # Text preprocessing (NLP pipeline)
│   ├── model_handler.py     # Load model dan prediksi
│   └── visualizer.py        # Visualisasi chart dengan Plotly
│
└── .streamlit/              # Konfigurasi Streamlit
    └── config.toml          # Theme dan pengaturan UI
```

## Penjelasan Setiap File

### File Utama

#### `app.py`
File utama aplikasi yang berisi:
- Konfigurasi halaman Streamlit
- CSS kustom untuk styling profesional (warna biru/putih/abu-abu)
- Fungsi untuk render sidebar (model info, dataset info)
- Fungsi untuk render tab input (URL dan Text)
- Fungsi untuk proses klasifikasi (URL atau Text)
- Fungsi untuk menampilkan hasil prediksi
- Entry point aplikasi (`main()`)

#### `config.py`
File konfigurasi yang berisi:
- **MODEL_CONFIG**: Parameter Skip-Gram (dimensi 150, window 3, epochs 50)
- **SVM_CONFIG**: Parameter SVM (kernel linear, C=1.0, probability=True)
- **DATA_CONFIG**: Split ratio (80% train, 20% test)
- **SCRAPER_CONFIG**: Timeout dan User-Agent untuk web scraping
- **UI_CONFIG**: Konfigurasi UI Streamlit
- **LABEL_MAPPING**: Mapping label (0=Finance, 1=Sport)
- **COLOR_SCHEME**: Warna tema aplikasi
- **PATHS**: Path ke model dan data

### Folder Utils

#### `utils/scraper.py`
Modul untuk web scraping artikel:
- **scrape_article()**: Ekstrak konten dari URL menggunakan trafilatura
- **validate_url()**: Validasi format URL (harus http/https)
- **clean_html_content()**: Bersihkan noise dari hasil scraping

**Proses Scraping:**
1. Download HTML dari URL dengan custom User-Agent
2. Ekstrak konten utama dengan trafilatura
3. Ekstrak metadata (title, author, date)
4. Bersihkan noise (tanggal pendek, dateline, URL)
5. Return dictionary berisi konten dan metadata

#### `utils/preprocessor.py`
Modul untuk preprocessing teks:
- **preprocess_text()**: Pipeline lengkap (noise removal + stopwords + stemming)
- **clean_noise()**: Hapus [Gambas], watermark, special characters, lowercase
- **remove_stopwords_and_stem()**: Hapus stopwords dan stemming dengan Sastrawi
- **tokenize_text()**: Split teks menjadi list kata
- **get_text_statistics()**: Hitung statistik teks (char, word, sentence count)

**Pipeline Preprocessing:**
1. Noise Removal: Hapus [Gambas:Video], dateline (JAKARTA -), watermark
2. Lowercase: Ubah semua huruf jadi kecil
3. Remove Non-Alphabet: Hapus angka dan special characters
4. Stopword Removal: Hapus kata umum ("yang", "di", "ke", "untuk", dll)
5. Stemming: Ubah ke bentuk dasar (berlari → lari, bermain → main)
6. Tokenization: Split jadi list kata

#### `utils/model_handler.py`
Modul untuk load model dan prediksi:
- **ModelHandler class**: Singleton pattern untuk manage model (load 1x saja)
- **load_models()**: Load Skip-Gram dan SVM dari folder models/
- **get_model_info()**: Ambil info model (dimensi, vocab size, window)
- **doc_to_vector()**: Ubah dokumen jadi vektor (mean word embedding)
- **predict_category()**: Prediksi kategori dengan SVM

**Pipeline Prediksi:**
1. Load model Skip-Gram dan SVM (singleton, hanya 1x)
2. Untuk setiap token, ambil vektor dari Skip-Gram (150 dimensi)
3. Hitung rata-rata vektor (mean pooling) → document vector
4. Masukkan document vector ke SVM
5. SVM prediksi kategori (0=Finance, 1=Sport)
6. Hitung confidence score dan probability distribution
7. Return hasil prediksi

#### `utils/visualizer.py`
Modul untuk visualisasi dengan Plotly:
- **plot_probability_distribution()**: Horizontal bar chart untuk probabilitas klasifikasi
- **plot_token_statistics()**: Pie chart untuk coverage vocabulary (matched vs OOV)
- **plot_dataset_distribution()**: Bar chart untuk distribusi dataset training

### Folder Models

#### `skipgram_model.model`
Model Skip-Gram Word2Vec yang sudah di-training:
- **Dimensi**: 150D (setiap kata direpresentasikan sebagai vektor 150 dimensi)
- **Window**: 3 (context window kiri-kanan)
- **Vocabulary**: ~3000-5000 kata (tergantung min_count)
- **Training**: 50 epochs pada 180 artikel (90 Sport + 90 Finance)

#### `svm_classifier.joblib`
Model SVM (Support Vector Machine) untuk klasifikasi:
- **Kernel**: Linear
- **Classes**: 2 (Finance=0, Sport=1)
- **Probability**: True (untuk confidence score)
- **Input**: Vektor 150 dimensi dari Skip-Gram
- **Output**: Kategori (Sport/Finance) + probability

### Folder Data

Dataset CSV dengan struktur kolom: `judul, link, waktu, isi_berita`

#### `detik_sport_90.csv`
90 artikel olahraga dari detik.com (kategori: sepakbola, basket, badminton, dll)

#### `detik_finance_90.csv`
90 artikel ekonomi/bisnis dari detik.com (kategori: moneter, bisnis, investasi, dll)

**Total Dataset**: 180 artikel (balanced)
**Split**: 80% training (144 artikel), 20% testing (36 artikel)

## Metode Machine Learning

### Skip-Gram Word2Vec

**Apa itu Skip-Gram?**

Skip-Gram adalah salah satu metode Word Embedding yang mengubah kata menjadi vektor numerik. Word embedding adalah representasi kata dalam bentuk vektor yang bisa ditangani komputer.

**Cara Kerja Skip-Gram:**
1. Input: 1 kata (center word)
2. Output: Prediksi kata-kata di sekitarnya (context words)
3. Training: Model belajar memprediksi context dari center word
4. Hasil: Setiap kata direpresentasikan sebagai vektor 150 dimensi

**Contoh:**
```
Kalimat: "Timnas Indonesia menang lawan Thailand"
Center word: "Indonesia"
Context (window=3): "Timnas", "menang", "lawan"

Skip-Gram belajar:
"Indonesia" → prediksi "Timnas", "menang", "lawan"
```

**Hasil Training:**
- Kata "Indonesia" = vektor [0.23, -0.45, 0.67, ..., 0.12] (150 angka)
- Kata "menang" = vektor [-0.34, 0.56, 0.23, ..., 0.45] (150 angka)

**Keunggulan Skip-Gram:**
- Kata dengan makna serupa punya vektor yang mirip
- Contoh: vektor("sepakbola") ≈ vektor("bola") ≈ vektor("pertandingan")
- Bisa menangkap semantic meaning (makna kata)

### TF-IDF (Tidak Digunakan di Aplikasi Ini)

**Apa itu TF-IDF?**

TF-IDF (Term Frequency-Inverse Document Frequency) adalah metode lain untuk representasi teks dalam bentuk angka.

**Cara Kerja TF-IDF:**
1. **TF (Term Frequency)**: Hitung berapa kali kata muncul dalam dokumen
2. **IDF (Inverse Document Frequency)**: Hitung seberapa jarang kata muncul di semua dokumen
3. **TF-IDF Score**: TF × IDF (kata yang sering muncul tapi jarang di dokumen lain = score tinggi)

**Contoh:**
```
Dokumen 1: "bola basket final seru"
Dokumen 2: "bola sepak final liga"

Kata "final" muncul di kedua dokumen → IDF rendah → TF-IDF rendah
Kata "basket" hanya muncul di Dokumen 1 → IDF tinggi → TF-IDF tinggi
```

**Perbedaan Skip-Gram vs TF-IDF:**

| Aspek | Skip-Gram | TF-IDF |
|-------|-----------|---------|
| Representasi | Dense vector (150 angka) | Sparse vector (ribuan angka, banyak yang 0) |
| Semantic | Tangkap makna kata | Hanya frekuensi |
| Kata serupa | Vektor mirip | Tidak tahu hubungan |
| Dimensi | Kecil (150D) | Besar (vocab_size) |
| Contoh | "sepakbola" ≈ "bola" | "sepakbola" ≠ "bola" |

**Mengapa Aplikasi Ini Pakai Skip-Gram Saja?**
- Skip-Gram lebih baik menangkap semantic meaning
- Vector lebih compact (150D vs ribuan dimensi)
- Hasil klasifikasi lebih akurat untuk teks pendek-menengah
- Lebih modern dan state-of-the-art

### Support Vector Machine (SVM)

**Apa itu SVM?**

SVM adalah algoritma supervised learning untuk klasifikasi. SVM mencari hyperplane (garis/bidang pemisah) terbaik yang memisahkan data dari 2 kelas.

**Cara Kerja SVM:**
1. Input: Vektor fitur (dari Skip-Gram, 150 dimensi)
2. Training: Cari hyperplane yang memisahkan Sport vs Finance dengan margin maksimal
3. Prediksi: Tentukan posisi vektor baru terhadap hyperplane
4. Output: Kategori (Sport/Finance) + confidence score

**Ilustrasi:**
```
     Finance (biru)         |         Sport (oranye)
  •  •  •  •  •  •          |          •  •  •  •  •
                            |
                      Hyperplane (SVM)
                      (garis pemisah)
```

**Keunggulan SVM:**
- Efektif untuk high-dimensional data (150D)
- Robust terhadap overfitting
- Bisa kasih probability score

## Fungsi Skip-Gram dan SVM di Aplikasi Ini

### Fungsi Skip-Gram
1. **Word Embedding**: Mengubah kata menjadi vektor numerik 150 dimensi
2. **Semantic Representation**: Menangkap makna dan konteks kata
3. **Document Vector**: Rata-rata vektor kata = vektor dokumen

**Contoh Proses:**
```
Input artikel: "Timnas Indonesia menang 3-0 lawan Thailand di final"

Setelah preprocessing: ["timnas", "indonesia", "menang", "lawan", "thailand", "final"]

Skip-Gram embedding:
- "timnas"    → [0.23, -0.45, ..., 0.12] (150D)
- "indonesia" → [-0.34, 0.56, ..., 0.45] (150D)
- "menang"    → [0.67, 0.23, ..., -0.23] (150D)
- ...

Document vector (mean): [0.15, 0.11, ..., 0.08] (150D)
```

### Fungsi SVM
1. **Klasifikasi**: Memisahkan Sport vs Finance
2. **Confidence Score**: Menghitung seberapa yakin prediksi
3. **Probability Distribution**: Probabilitas setiap kategori

**Contoh Proses:**
```
Document vector: [0.15, 0.11, ..., 0.08] (150D)
        ↓
    SVM Classifier
        ↓
Output:
- Kategori: Sport
- Confidence: 92.5%
- Probability: Sport=92.5%, Finance=7.5%
```

## Fitur Aplikasi

### 1. Input URL
- Paste URL artikel dari detik.com atau website berita lain
- Otomatis scraping konten artikel
- Ekstrak metadata (title, author, date)
- Tombol contoh URL (Sport dan Finance)

### 2. Input Text Langsung
- Paste atau ketik teks artikel langsung (minimal 50 karakter)
- Tidak perlu scraping, langsung ke preprocessing
- Cocok untuk testing dengan teks custom

### 3. Preprocessing Pipeline
- Noise removal otomatis
- Stopword removal (750+ stopwords Indonesia)
- Stemming (bentuk dasar kata)
- Tokenization

### 4. Klasifikasi Real-time
- Prediksi kategori (Sport/Finance)
- Confidence score (persentase keyakinan)
- Vocabulary coverage (berapa % kata dikenali)
- Progress bar untuk tracking proses

### 5. Visualisasi Interaktif
- **Probability Distribution**: Horizontal bar chart probabilitas setiap kategori
- **Token Coverage**: Pie chart matched vs out-of-vocabulary tokens
- **Dataset Distribution**: Bar chart distribusi dataset training

### 6. Detail Hasil
- **Article Metadata**: Title, author, tanggal publish, URL
- **Content Statistics**: Jumlah karakter, kata, kalimat, rata-rata panjang kata
- **Content Preview**: 1000 karakter pertama dari artikel asli
- **Preprocessing Results**: Teks setelah preprocessing, perbandingan sebelum-sesudah
- **Token Analysis**: Total tokens, matched, OOV, sample 50 token pertama

### 7. Model Information (Sidebar)
- Model status (loaded/error)
- Vector dimension (150D)
- Vocabulary size (~3000-5000 kata)
- Context window (3)
- Training dataset info (90+90 artikel)

## Cara Menjalankan Aplikasi

### Persiapan Environment

1. **Install Miniconda** (sudah done)
2. **Activate environment:**
   ```bash
   conda activate newsclassifier
   ```

### Menjalankan Lokal

**Opsi 1: Menggunakan Batch File**
```bash
run_app.bat
```

**Opsi 2: Manual Command**
```bash
streamlit run app.py
```

**Akses Aplikasi:**
- URL: http://localhost:8501
- Jika port 8501 sudah dipakai, Streamlit akan otomatis pakai port lain (8502, 8503, dll)

### Cara Menggunakan Aplikasi

#### Input dari URL:
1. Pilih tab "URL Input"
2. Paste URL artikel atau klik tombol contoh
3. Klik "Classify Article"
4. Tunggu proses scraping → preprocessing → klasifikasi
5. Lihat hasil prediksi dan detail analisis

#### Input Text Langsung:
1. Pilih tab "Text Input"
2. Paste atau ketik teks artikel (minimal 50 karakter)
3. Klik "Classify Text"
4. Tunggu proses preprocessing → klasifikasi
5. Lihat hasil prediksi dan detail analisis

**Flow Proses:**
```
URL/Text Input
    ↓
[Scraping] (jika URL)
    ↓
Preprocessing:
  - Noise removal
  - Stopword removal
  - Stemming
  - Tokenization
    ↓
Skip-Gram Embedding:
  - Ubah token jadi vektor
  - Mean pooling → document vector
    ↓
SVM Classification:
  - Prediksi kategori
  - Hitung confidence
    ↓
Tampilkan Hasil:
  - Kategori + confidence
  - Visualisasi probabilitas
  - Detail preprocessing
  - Token analysis
```

## Deployment ke Streamlit Cloud

### Persiapan

1. **Repository GitHub**: https://github.com/Wahyu402191/news-classifier.git
2. **File penting**:
   - `.python-version` → 3.11.10 (untuk kompatibilitas gensim)
   - `requirements.txt` → semua dependencies
   - `app.py` → entry point aplikasi

### Langkah Deploy

1. **Login Streamlit Cloud**: https://share.streamlit.io/
2. **New app** → pilih repository GitHub
3. **Settings**:
   - Repository: `Wahyu402191/news-classifier`
   - Branch: `main`
   - Main file path: `app.py`
   - Python version: Otomatis detect dari `.python-version` (3.11.10)
4. **Deploy** → tunggu proses build
5. **URL aplikasi**: https://wahyu402191-news-classifier.streamlit.app/

### Cara Update Deployment

Ketika ada perubahan code dan ingin update di Streamlit Cloud:

1. **Push perubahan ke GitHub:**
   ```bash
   git add .
   git commit -m "Update aplikasi"
   git push origin main
   ```

2. **Otomatis Re-deploy:**
   - Streamlit Cloud otomatis detect perubahan di GitHub
   - Akan langsung rebuild dan redeploy
   - Tidak perlu setting ulang

3. **Manual Reboot (jika perlu):**
   - Buka Streamlit Cloud dashboard
   - Pilih aplikasi Anda
   - Klik "Reboot app" atau "Manage app" → "Reboot"

4. **Monitor Build Log:**
   - Klik "Manage app"
   - Lihat "Logs" untuk cek proses build
   - Pastikan tidak ada error

## Kebutuhan Sistem

### Development (Lokal)
- **OS**: Windows 10/11
- **Python**: 3.11.10 (install via Miniconda)
- **RAM**: Minimal 4 GB (recommended 8 GB)
- **Storage**: ~500 MB (untuk environment + models)
- **Internet**: Diperlukan untuk scraping URL

### Production (Streamlit Cloud)
- **Python**: 3.11.10 (otomatis dari `.python-version`)
- **RAM**: 1 GB (free tier Streamlit Cloud)
- **Storage**: 100 MB limit untuk repository
- **Build Time**: ~3-5 menit
- **URL**: Publik, bisa diakses siapa saja

## Dependencies

Lihat `requirements.txt` untuk daftar lengkap. Dependencies utama:
- streamlit >= 1.28.0
- gensim >= 4.3.0
- scikit-learn >= 1.3.0
- PySastrawi >= 1.2.0
- trafilatura >= 1.6.0
- plotly >= 5.17.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- joblib >= 1.3.0

## Troubleshooting

### Error: Port 8501 sudah digunakan
```bash
# Matikan proses Streamlit yang sedang jalan
taskkill /F /IM streamlit.exe

# Atau jalankan di port lain
streamlit run app.py --server.port 8502
```

### Error: Model not found
- Pastikan folder `models/` ada dan berisi `skipgram_model.model` dan `svm_classifier.joblib`
- Cek path di `config.py`

### Error: Scraping gagal
- Cek koneksi internet
- Beberapa website punya protection anti-scraping
- Gunakan input text langsung sebagai alternatif

### Error: gensim build failed (Streamlit Cloud)
- Pastikan `.python-version` berisi `3.11.10`
- Python 3.12+ tidak support gensim 4.4.0

## Informasi Tambahan

**Developer**: Wahyu Pratama
**GitHub**: https://github.com/Wahyu402191
**Repository**: https://github.com/Wahyu402191/news-classifier
**Year**: 2026
**License**: MIT

## Credits

Dataset dikumpulkan dari detik.com (Sport dan Finance section) untuk keperluan edukasi dan penelitian.
