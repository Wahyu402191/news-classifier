# Detik News Classifier

Aplikasi web klasifikasi otomatis artikel berita Detikcom menggunakan dua metode Machine Learning: Skip-Gram Word2Vec dan TF-IDF Vectorizer.

## Deskripsi Aplikasi

Sistem klasifikasi artikel berita berbasis Natural Language Processing (NLP) dan Machine Learning dengan dukungan dua metode berbeda. Pengguna dapat memilih metode klasifikasi (Skip-Gram atau TF-IDF), memasukkan URL artikel atau teks langsung, kemudian sistem akan memproses dan memprediksi kategori berita (Sport atau Finance) beserta confidence score, probabilitas, dan representasi vektor lengkap.

## Teknologi dan Framework

### Framework Utama

**Streamlit 1.28.0+**
- Framework Python untuk web aplikasi interaktif
- Fungsi: Frontend dan Backend terintegrasi (all-in-one framework)
- Deployment: Streamlit Cloud (gratis, auto-update dari GitHub)
- Keunggulan: Tidak perlu HTML/CSS/JavaScript manual, UI otomatis dari Python

### Machine Learning Libraries

**Gensim 4.3.0**
- Library untuk Word2Vec (Skip-Gram model training dan inference)
- Fungsi: Word embedding, representasi kata dalam bentuk vektor dense
- Digunakan untuk metode Skip-Gram

**scikit-learn 1.3.0**
- Library untuk machine learning (SVM classifier, TF-IDF vectorizer, model evaluation)
- Fungsi: Klasifikasi dengan SVM, transformasi TF-IDF, train-test split, metrics
- Digunakan untuk kedua metode (Skip-Gram dan TF-IDF)

**NumPy 1.24.0**
- Library untuk komputasi array dan operasi numerik
- Fungsi: Manipulasi vektor, mean pooling, matrix operations

**joblib 1.3.0**
- Library untuk serialisasi model
- Fungsi: Save dan load model (.joblib files)

### NLP Libraries

**PySastrawi 1.2.0**
- Library NLP Bahasa Indonesia
- Fungsi:
  - Stopword Removal: Menghapus 750+ kata umum Indonesia (yang, di, ke, untuk, dll)
  - Stemming: Mengubah kata ke bentuk dasar (berlari -> lari, bermain -> main)
- Hanya digunakan untuk metode TF-IDF (Skip-Gram tidak pakai preprocessing ini)

**trafilatura 1.6.0**
- Library untuk web scraping dan ekstraksi konten artikel
- Fungsi: Extract clean text dari HTML, remove boilerplate, ekstrak metadata

### Visualization

**Plotly 5.17.0**
- Library untuk visualisasi interaktif
- Fungsi: Bar chart (probability distribution, dataset distribution), pie chart (token coverage)

### Data Processing

**Pandas 2.0.0**
- Library untuk manipulasi data tabular
- Fungsi: Load CSV dataset, preprocessing dataframe

## Arsitektur Aplikasi

### Streamlit All-in-One Architecture

Aplikasi ini menggunakan Streamlit yang merupakan framework full-stack (frontend dan backend menjadi satu). Tidak dapat dipisah menjadi backend dan frontend terpisah seperti FastAPI + HTML/CSS/JS.

**Struktur:**
```
Streamlit Application (app.py)
├── Frontend: UI components (otomatis generated dari Python)
├── Backend: Business logic, model inference, data processing
└── Session State: State management untuk user interaction
```

**Alur Request:**
```
User Input (URL/Text)
    ↓
Streamlit Session State
    ↓
Backend Processing (utils modules)
    ↓
Model Inference (Skip-Gram / TF-IDF)
    ↓
Frontend Rendering (Streamlit components)
    ↓
Display Results
```

## Struktur Folder

```
news-classifier-streamlit/
├── app.py                          # File utama aplikasi (entry point)
├── config.py                       # Konfigurasi aplikasi (paths, parameters, colors)
├── requirements.txt                # Dependencies Python
├── .python-version                 # Python version untuk Streamlit Cloud (3.11.10)
├── .gitignore                      # File yang diabaikan Git
├── run_app.bat                     # Script untuk menjalankan aplikasi (Windows)
├── train_tfidf_model.py            # Script training model TF-IDF
├── README.md                       # Dokumentasi lengkap (file ini)
│
├── data/                           # Dataset training
│   ├── detik_sport_90.csv          # 90 artikel Sport
│   └── detik_finance_90.csv        # 90 artikel Finance
│
├── models/                         # Model Machine Learning
│   ├── skipgram_model.model        # Skip-Gram Word2Vec (150D, Window 3)
│   ├── svm_classifier.joblib       # SVM classifier untuk Skip-Gram
│   ├── tfidf_vectorizer.joblib     # TF-IDF Vectorizer (3000 features)
│   └── svm_tfidf_classifier.joblib # SVM classifier untuk TF-IDF
│
├── utils/                          # Modul utilitas
│   ├── __init__.py                 # Init file untuk package
│   ├── scraper.py                  # Web scraping dari URL
│   ├── preprocessor.py             # Text preprocessing (NLP pipeline)
│   ├── model_handler.py            # Legacy handler (deprecated)
│   ├── dual_model_handler.py       # Handler untuk Skip-Gram DAN TF-IDF
│   └── visualizer.py               # Visualisasi chart dengan Plotly
│
└── .streamlit/                     # Konfigurasi Streamlit
    └── config.toml                 # Theme dan pengaturan UI
```

## Penjelasan Detail Setiap File

### File Utama

#### `app.py` (500+ lines)

**Fungsi:** Entry point aplikasi, mengatur UI dan alur klasifikasi

**Komponen Utama:**

1. **Imports dan Setup** (line 1-20)
   - Import semua modul yang dibutuhkan
   - Import utilities (scraper, preprocessor, dual_model_handler, visualizer)
   - Set page config Streamlit

2. **load_custom_css()** (line 23-90)
   - Definisi CSS kustom untuk styling profesional
   - Atur warna biru/putih/abu-abu
   - Style untuk scrollable text, vector display, badges

3. **initialize_models()** (line 93-99)
   - Function dengan decorator @st.cache_resource
   - Load Skip-Gram dan TF-IDF model hanya sekali
   - Return success status dan model info
   - Cached agar tidak reload setiap rerun

4. **render_sidebar()** (line 102-155)
   - Tampilkan sidebar dengan informasi sistem
   - Model status (Skip-Gram dan TF-IDF info)
   - Dataset distribution (90+90 articles)
   - Visualisasi dataset dengan Plotly
   - About section

5. **render_method_selection()** (line 158-177)
   - Radio button untuk pilih metode (Skip-Gram / TF-IDF)
   - Info box menjelaskan preprocessing masing-masing metode
   - Return pilihan metode user

6. **render_input_section()** (line 180-217)
   - Tab 1: URL Input dengan contoh Sport/Finance
   - Tab 2: Direct text input
   - Session state untuk menyimpan URL
   - Tombol example untuk load URL contoh
   - Return tuple (input_type, input_data)

7. **process_classification()** (line 220-287)
   - Fungsi utama untuk proses klasifikasi
   - Step 1: Extract content (scraping jika URL, langsung jika text)
   - Step 2: Preprocessing berbeda per metode
     - Skip-Gram: Hanya clean_noise() -> tokens
     - TF-IDF: Full preprocess_text() -> string
   - Step 3: Classification dengan method yang dipilih
   - Step 4: Display results
   - Progress bar untuk tracking

8. **display_results()** (line 290-450)
   - Tampilkan hasil klasifikasi lengkap
   - Metric cards: Category, Confidence, Coverage/Features
   - Probability distribution chart (Plotly)
   - 3 Tabs:
     - Tab 1: Extracted Content (metadata, original text scrollable & copyable)
     - Tab 2: Preprocessing Result (method info, stats, processed text scrollable & copyable)
     - Tab 3: Feature Representation (vector values, top keywords, full vector)

9. **main()** (line 453-472)
   - Entry point aplikasi
   - Load CSS, render sidebar
   - Render method selection
   - Render input section
   - Tombol classify dan call process_classification()

#### `config.py` (100+ lines)

**Fungsi:** Konfigurasi terpusat untuk seluruh aplikasi

**Isi:**

1. **MODEL_CONFIG** (Skip-Gram parameters)
   ```python
   vector_size: 150     # Dimensi embedding
   window: 3            # Context window kiri-kanan
   min_count: 2         # Minimum word frequency
   epochs: 50           # Training iterations
   sg: 1                # Skip-gram (bukan CBOW)
   ```

2. **SVM_CONFIG** (SVM parameters)
   ```python
   kernel: 'linear'     # Linear kernel
   C: 1.0               # Regularization
   probability: True    # Enable probability estimates
   ```

3. **DATA_CONFIG** (Train-test split)
   ```python
   test_size: 0.2       # 20% untuk testing
   stratify: True       # Balanced split
   ```

4. **SCRAPER_CONFIG** (Web scraping settings)
   ```python
   timeout: 10          # Request timeout seconds
   user_agent: '...'    # Browser user agent
   ```

5. **UI_CONFIG** (Streamlit UI settings)
   ```python
   page_title, page_icon, layout, sidebar_state
   ```

6. **LABEL_MAPPING** (Class label mapping)
   ```python
   0: 'Finance', 1: 'Sport'
   ```

7. **COLOR_SCHEME** (UI color theme)
   ```python
   primary, secondary, sport, finance, background, text colors
   ```

8. **PATHS** (File paths)
   ```python
   Paths ke models, data, CSV files
   ```

#### `train_tfidf_model.py` (150+ lines)

**Fungsi:** Script training model TF-IDF (run sekali untuk generate model)

**Pipeline:**

1. **load_dataset()** (line 15-35)
   - Load detik_sport_90.csv dan detik_finance_90.csv
   - Add label column (Sport=1, Finance=0)
   - Combine kedua dataset
   - Return dataframe gabungan

2. **preprocess_dataset()** (line 37-50)
   - Apply preprocess_text() ke semua artikel
   - Filter artikel yang terlalu pendek (< 10 char)
   - Return cleaned dataframe

3. **train_tfidf_model()** (line 52-110)
   - Split data 80-20 train-test (stratified)
   - Create TF-IDF vectorizer:
     - max_features: 3000 (batasi vocabulary)
     - min_df: 2 (minimum document frequency)
     - max_df: 0.8 (maximum document frequency)
     - ngram_range: (1,2) (unigram dan bigram)
   - Fit vectorizer pada training set
   - Transform training dan test set
   - Train SVM classifier (linear kernel, probability=True)
   - Evaluate accuracy dan classification report
   - Save models: tfidf_vectorizer.joblib, svm_tfidf_classifier.joblib

4. **main()** (line 112-130)
   - Orchestrate training pipeline
   - Print training progress dan final accuracy

**Output:**
- `models/tfidf_vectorizer.joblib` (TF-IDF vectorizer dengan 3000 features)
- `models/svm_tfidf_classifier.joblib` (SVM model untuk TF-IDF)

### Folder Utils

#### `utils/scraper.py` (200+ lines)

**Fungsi:** Web scraping artikel dari URL

**Functions:**

1. **clean_html_content()** (line 10-75)
   - Input: Raw text hasil ekstraksi HTML
   - Proses:
     - Split text per line
     - Filter lines yang terlalu pendek (< 5 words)
     - Filter lines hanya tanggal/waktu
     - Filter lines tanpa punctuation
     - Remove dateline prefix (JAKARTA - ...)
     - Join paragraphs, remove URLs, normalize spaces
   - Output: Cleaned text content

2. **scrape_article()** (line 78-145)
   - Input: URL artikel
   - Proses:
     - Create HTTP request dengan User-Agent
     - Download HTML dengan urllib (timeout 10s)
     - Extract content dengan trafilatura.extract()
     - Extract metadata (title, author, date) dengan trafilatura.extract_metadata()
     - Clean content dengan clean_html_content()
     - Validasi minimal 100 characters
   - Output: Dictionary berisi url, title, author, date, content, error

3. **validate_url()** (line 148-170)
   - Input: URL string
   - Proses:
     - Check starts with http:// atau https://
     - Regex validation untuk struktur URL
     - Check domain, port, path validity
   - Output: Boolean (True jika valid)

#### `utils/preprocessor.py` (150+ lines)

**Fungsi:** Text preprocessing dengan NLP pipeline

**Global Variables:**

1. **_stopword_remover, _stemmer** (line 10-12)
   - Singleton instances untuk efisiensi
   - Load sekali, digunakan berulang kali

**Functions:**

1. **get_stopword_remover()** (line 15-22)
   - Lazy initialization stopword remover dari Sastrawi
   - Return singleton instance
   - Load 750+ stopwords Bahasa Indonesia

2. **get_stemmer()** (line 25-32)
   - Lazy initialization stemmer dari Sastrawi
   - Return singleton instance
   - Stemmer untuk ubah kata ke bentuk dasar

3. **clean_noise()** (line 35-70)
   - Input: Raw text
   - Proses:
     - Remove [Gambas:Video] tags dengan regex
     - Remove "Lihat juga", "Baca juga" sections
     - Remove dateline (JAKARTA - ...)
     - Remove watermarks (detikcom, detikSport, detikFinance)
     - Lowercase semua text
     - Remove non-alphabetic characters (hanya huruf dan spasi)
     - Normalize multiple spaces menjadi single space
   - Output: Cleaned text (noise removed)

4. **remove_stopwords_and_stem()** (line 73-95)
   - Input: Cleaned text
   - Proses:
     - Remove stopwords dengan Sastrawi (yang, di, ke, untuk, dll)
     - Stemming dengan Sastrawi (berlari -> lari, bermain -> main)
   - Output: Processed text (stopwords removed, stemmed)

5. **preprocess_text()** (line 98-115)
   - Input: Raw text
   - Proses:
     - Step 1: clean_noise()
     - Step 2: remove_stopwords_and_stem()
   - Output: Fully preprocessed text
   - Digunakan untuk TF-IDF (full preprocessing)

6. **tokenize_text()** (line 118-132)
   - Input: Preprocessed text string
   - Proses: Split by space, filter empty tokens
   - Output: List of tokens

7. **get_text_statistics()** (line 135-160)
   - Input: Text string
   - Proses: Hitung char count, word count, sentence count, avg word length
   - Output: Dictionary dengan statistik

#### `utils/dual_model_handler.py` (400+ lines)

**Fungsi:** Handler untuk Skip-Gram DAN TF-IDF model (dual-method support)

**Class DualModelHandler:**

1. **__new__()** (line 23-28)
   - Singleton pattern: hanya satu instance di seluruh aplikasi
   - Mencegah multiple model loading

2. **load_models()** (line 30-60)
   - Load semua model:
     - Skip-Gram Word2Vec dari models/skipgram_model.model
     - SVM Skip-Gram dari models/svm_classifier.joblib
     - TF-IDF Vectorizer dari models/tfidf_vectorizer.joblib
     - SVM TF-IDF dari models/svm_tfidf_classifier.joblib
   - Set flag _is_loaded = True
   - Return success boolean

3. **get_skipgram_info()** (line 62-77)
   - Return dictionary dengan info Skip-Gram:
     - method, vector_size, vocab_size, window, representation
   - Digunakan untuk display di sidebar

4. **get_tfidf_info()** (line 79-93)
   - Return dictionary dengan info TF-IDF:
     - method, vocab_size, representation
   - Digunakan untuk display di sidebar

5. **classify_skipgram()** (line 95-155)
   - Input: List of tokens (hasil clean_noise + tokenize)
   - Proses:
     - Loop setiap token, cek apakah ada di vocabulary Skip-Gram
     - Jika ada: ambil vektor 150D, masukkan ke matched_vectors
     - Jika tidak: masukkan ke oov_tokens
     - Mean pooling: hitung rata-rata semua matched_vectors
     - Reshape vector menjadi 2D (1, 150)
     - Prediksi dengan SVM Skip-Gram
     - Extract probabilities (predict_proba atau decision_function)
   - Output: Dictionary dengan prediction, confidence, probabilities, token stats, vector sample, vector full

6. **classify_tfidf()** (line 157-235)
   - Input: Preprocessed text string (hasil full preprocessing)
   - Proses:
     - Transform text ke TF-IDF vector (sparse matrix 3000D)
     - Prediksi dengan SVM TF-IDF
     - Extract probabilities
     - Extract top TF-IDF features (kata dengan score tertinggi)
     - Get non-zero indices dan values
     - Buat vector sample (15 features pertama dengan values)
   - Output: Dictionary dengan prediction, confidence, probabilities, active features, top keywords, vector sample, vector full

**Module Functions:**

1. **load_dual_models()** (line 240-245)
   - Wrapper untuk _dual_handler.load_models()

2. **get_skipgram_info()** (line 248-252)
   - Wrapper untuk _dual_handler.get_skipgram_info()

3. **get_tfidf_info()** (line 255-259)
   - Wrapper untuk _dual_handler.get_tfidf_info()

4. **classify_with_method()** (line 262-280)
   - Input: tokens_or_text (list untuk skipgram, string untuk tfidf), method
   - Decision: call classify_skipgram() atau classify_tfidf()
   - Output: Classification result dictionary

#### `utils/visualizer.py` (200+ lines)

**Fungsi:** Visualisasi data dengan Plotly

**Functions:**

1. **plot_probability_distribution()** (line 10-60)
   - Input: Dictionary probabilitas (Sport: 89.4, Finance: 10.6)
   - Proses:
     - Extract categories dan values (TIDAK dikali 100 lagi, sudah persen)
     - Get colors dari config (Sport=orange, Finance=blue)
     - Create horizontal bar chart dengan Plotly
     - Set xaxis range [0, 100]
   - Output: Plotly figure object

2. **plot_token_statistics()** (line 95-125)
   - Input: matched count, oov count
   - Proses:
     - Create pie chart dengan 2 slices
     - Colors: green (matched), orange (oov)
   - Output: Plotly figure object

3. **plot_dataset_distribution()** (line 128-160)
   - Input: sport_count, finance_count
   - Proses:
     - Create vertical bar chart
     - Colors: orange (sport), blue (finance)
   - Output: Plotly figure object

### Folder Data

#### `data/detik_sport_90.csv` (90 rows)

**Struktur:**
```
judul, link, waktu, isi_berita
```

**Konten:**
- 90 artikel olahraga dari detik.com
- Kategori: sepakbola, basket, badminton, tenis, MotoGP, Formula 1
- Sumber: sport.detik.com
- Format: CSV dengan delimiter koma

#### `data/detik_finance_90.csv` (90 rows)

**Struktur:**
```
judul, link, waktu, isi_berita
```

**Konten:**
- 90 artikel ekonomi/bisnis dari detik.com  
- Kategori: moneter, bisnis, investasi, perbankan, pasar modal
- Sumber: finance.detik.com
- Format: CSV dengan delimiter koma

**Total Dataset:** 180 artikel (balanced)
**Split:** 80% training (144), 20% testing (36)

### Folder Models

#### `models/skipgram_model.model` (6.2 MB)

**Jenis:** Gensim Word2Vec model (Skip-Gram architecture)

**Spesifikasi:**
- Dimensi: 150D (setiap kata = vektor 150 angka float)
- Vocabulary: ~4015 kata unik
- Window: 3 (context window kiri-kanan)
- Min Count: 2 (kata minimal muncul 2x)
- Epochs: 50 (training iterations)
- Algorithm: Skip-Gram (prediksi context dari center word)

**Training:**
- Data: 180 artikel (90 Sport + 90 Finance)
- Preprocessing: Noise removal only (NO stopwords, NO stemming)
- Training time: ~2-5 menit

**Fungsi:**
- Mengubah kata menjadi vektor 150D
- Kata dengan makna serupa punya vektor mirip
- Digunakan untuk metode Skip-Gram classification

#### `models/svm_classifier.joblib` (500 KB)

**Jenis:** scikit-learn SVM model untuk Skip-Gram

**Spesifikasi:**
- Algorithm: Support Vector Machine
- Kernel: Linear
- C: 1.0 (regularization parameter)
- Probability: True (enable probability estimates)
- Classes: [0, 1] (Finance=0, Sport=1)

**Input:** Document vector 150D (hasil mean pooling Skip-Gram)
**Output:** Class prediction + probabilities

**Training:**
- Data: 144 articles (80% dari 180)
- Features: 150D vectors dari Skip-Gram
- Accuracy: ~95-100% (depending on split)

#### `models/tfidf_vectorizer.joblib` (1.5 MB)

**Jenis:** scikit-learn TfidfVectorizer

**Spesifikasi:**
- Max Features: 3000 (vocabulary dibatasi 3000 kata)
- Min DF: 2 (kata minimal muncul di 2 dokumen)
- Max DF: 0.8 (kata maksimal muncul di 80% dokumen)
- Ngram Range: (1, 2) (unigram dan bigram)
- Vocabulary: ~3000 features

**Training:**
- Data: 144 articles (80% dari 180)
- Preprocessing: Full (noise + stopwords + stemming)

**Fungsi:**
- Transform text menjadi TF-IDF vector (sparse 3000D)
- TF (Term Frequency): seberapa sering kata muncul di dokumen
- IDF (Inverse Document Frequency): seberapa jarang kata di corpus
- TF-IDF = TF × IDF

#### `models/svm_tfidf_classifier.joblib` (2 MB)

**Jenis:** scikit-learn SVM model untuk TF-IDF

**Spesifikasi:**
- Algorithm: Support Vector Machine
- Kernel: Linear
- C: 1.0
- Probability: True
- Classes: [0, 1] (Finance=0, Sport=1)

**Input:** TF-IDF vector 3000D (sparse matrix)
**Output:** Class prediction + probabilities

**Training:**
- Data: 144 articles
- Features: 3000D TF-IDF vectors
- Accuracy: 100% (on test set)

## Metode Machine Learning

### Skip-Gram Word2Vec

**Definisi:**

Skip-Gram adalah metode word embedding yang mengubah kata menjadi vektor numerik dense (padat). Word embedding adalah representasi kata dalam bentuk vektor yang dapat diproses oleh algoritma machine learning.

**Arsitektur:**

```
Input: Center Word (1 kata)
    ↓
Embedding Layer (lookup table)
    ↓
Hidden Layer (150 neurons)
    ↓
Output Layer (softmax)
    ↓
Output: Context Words (prediksi kata di sekitar center word)
```

**Cara Kerja:**

1. **Training Phase:**
   - Input: 1 center word
   - Target: Prediksi kata-kata di window context (kiri-kanan)
   - Window size: 3 (3 kata kiri, 3 kata kanan)
   - Loss: Maximize probability of context words given center word
   - Update: Backpropagation untuk update embedding weights

2. **Inference Phase:**
   - Setiap kata diubah menjadi vektor 150D
   - Lookup dari embedding layer (weight matrix)
   - Kata yang tidak ada di vocabulary = Out-of-Vocabulary (OOV)

**Contoh:**

```
Kalimat: "Timnas Indonesia menang lawan Thailand"
Center word: "Indonesia"
Context (window=3): "Timnas", "menang", "lawan"

Skip-Gram training:
Input: "Indonesia" → [embedding vector 150D]
Output: Prediksi "Timnas", "menang", "lawan"

Setelah training:
- "Indonesia" → [0.23, -0.45, 0.67, ..., 0.12] (150 angka)
- "menang" → [-0.34, 0.56, 0.23, ..., 0.45] (150 angka)
- "Thailand" → [0.12, 0.34, -0.67, ..., 0.89] (150 angka)
```

**Keunggulan:**

1. **Semantic Meaning:**
   - Kata dengan makna serupa punya vektor yang mirip
   - Contoh: cos_similarity("sepakbola", "bola") > 0.8
   - Bisa tangkap hubungan: "raja" - "laki-laki" + "perempuan" ≈ "ratu"

2. **Dense Representation:**
   - Hanya 150 dimensi (compact)
   - Semua nilai non-zero (dense vector)
   - Efisien untuk komputasi

3. **Context-Aware:**
   - Belajar dari context kata di sekitarnya
   - Tangkap syntactic dan semantic patterns

**Preprocessing untuk Skip-Gram:**

- Hanya noise removal (hapus tag HTML, watermark, special characters)
- TIDAK pakai stopword removal
- TIDAK pakai stemming
- Alasan: Word embedding butuh context penuh, stopwords bisa penting untuk context

**Document Vector (Mean Pooling):**

```
Tokens: ["timnas", "indonesia", "menang", "lawan", "thailand"]

Step 1: Ambil vektor setiap kata
- "timnas" → v1 = [0.23, -0.45, 0.67, ...]
- "indonesia" → v2 = [-0.34, 0.56, 0.23, ...]
- "menang" → v3 = [0.67, 0.23, -0.23, ...]
- "lawan" → v4 = [0.12, 0.89, 0.34, ...]
- "thailand" → v5 = [0.45, -0.12, 0.67, ...]

Step 2: Mean Pooling (rata-rata)
Document Vector = (v1 + v2 + v3 + v4 + v5) / 5
                = [0.15, 0.11, 0.08, ...] (150D)

Step 3: Klasifikasi
SVM Input: [0.15, 0.11, 0.08, ...]
SVM Output: Sport (89.4%)
```

### TF-IDF Vectorizer

**Definisi:**

TF-IDF (Term Frequency - Inverse Document Frequency) adalah metode representasi teks berdasarkan statistik frekuensi kata. Mengubah dokumen menjadi vektor sparse (banyak nilai 0) dengan dimensi besar.

**Formula:**

```
TF-IDF(t, d) = TF(t, d) × IDF(t)

TF (Term Frequency):
TF(t, d) = (jumlah kemunculan term t di dokumen d) / (total term di dokumen d)

IDF (Inverse Document Frequency):
IDF(t) = log( (total dokumen) / (jumlah dokumen yang mengandung term t) )
```

**Cara Kerja:**

1. **Vocabulary Building:**
   - Ekstrak semua unique words dari corpus
   - Batasi max_features = 3000 (vocabulary size)
   - Filter min_df = 2 (kata harus muncul minimal di 2 dokumen)
   - Filter max_df = 0.8 (kata tidak boleh muncul di >80% dokumen)

2. **TF Calculation:**
   - Hitung frekuensi setiap kata di dokumen
   - Normalize dengan total kata

3. **IDF Calculation:**
   - Hitung inverse document frequency
   - Kata yang jarang = IDF tinggi
   - Kata yang umum = IDF rendah

4. **TF-IDF Score:**
   - Kalikan TF dengan IDF
   - Kata yang sering di dokumen ini TAPI jarang di corpus = score tinggi

**Contoh:**

```
Corpus: 100 dokumen

Dokumen: "taksi online vietnam xanh sm xanh sm sudah..."

Kata "taksi":
- TF = 1/173 = 0.0058 (muncul 1x dari 173 kata)
- IDF = log(100/50) = 0.30 (muncul di 50 dari 100 dokumen)
- TF-IDF = 0.0058 × 0.30 = 0.0017

Kata "vietnam":
- TF = 1/173 = 0.0058
- IDF = log(100/5) = 1.30 (hanya muncul di 5 dokumen, jarang)
- TF-IDF = 0.0058 × 1.30 = 0.0075 (lebih tinggi!)

Vector TF-IDF (3000D):
[0, 0, 0.0075, ..., 0, 0.0017, ..., 0] (banyak nilai 0)
```

**Keunggulan:**

1. **Importance Weighting:**
   - Kata penting di dokumen mendapat score tinggi
   - Kata umum (stopwords) mendapat score rendah

2. **Interpretable:**
   - Bisa lihat kata mana yang penting (top TF-IDF keywords)
   - Mudah explain hasil klasifikasi

3. **Proven Effectiveness:**
   - Sudah terbukti efektif untuk text classification
   - Baseline yang baik untuk NLP tasks

**Kelemahan:**

1. **Sparse Representation:**
   - Vector dimensi tinggi (3000D)
   - Banyak nilai 0 (sparse matrix)
   - Memory intensive

2. **No Semantic Understanding:**
   - "sepakbola" dan "bola" dianggap completely different
   - Tidak tangkap similarity atau hubungan antar kata

3. **Order Ignored:**
   - Bag-of-words approach
   - Tidak peduli urutan kata

**Preprocessing untuk TF-IDF:**

- Full preprocessing: noise removal + stopword removal + stemming
- Alasan: TF-IDF berbasis frekuensi, stopwords akan dapat score rendah (IDF rendah), tapi tetap occupy dimensi. Lebih baik dihapus untuk efisiensi.

**Vector Representation:**

```
Text: "menteri hubung dudy purwagandhi buka suara soal kehadiran taksi online asal vietnam xanh sm..."

Preprocessing: noise removal + stopwords + stemming

TF-IDF Transform:
- Vocabulary: 3000 features
- Active features: 62 (non-zero values)
- Zero features: 2938

Top Keywords (dengan bobot):
- taksi: 0.5174
- dudy: 0.5187
- layan: 0.2228
- online: 0.2218
- vietnam: 0.2217
- ...

Vector (3000D sparse):
[0, 0, 0.5174, 0, 0, 0.2228, ..., 0] (mayoritas 0)

SVM Input: Sparse vector 3000D
SVM Output: Finance (58.7%)
```

### Perbandingan Skip-Gram vs TF-IDF

| Aspek | Skip-Gram | TF-IDF |
|-------|-----------|---------|
| **Representasi** | Dense vector (150D, semua non-zero) | Sparse vector (3000D, banyak 0) |
| **Semantic** | Tangkap semantic meaning (kata serupa = vektor mirip) | Tidak tangkap semantic (kata serupa = berbeda total) |
| **Dimensi** | Kecil (150D) | Besar (3000D) |
| **Preprocessing** | Minimal (noise only) | Full (noise + stopwords + stemming) |
| **Training** | Butuh unsupervised pre-training (Word2Vec) | Langsung fit pada data |
| **Interpretability** | Sulit (vector values tidak punya makna langsung) | Mudah (bisa lihat top keywords) |
| **Memory** | Efisien (dense, dimensi kecil) | Intensive (sparse tapi dimensi besar) |
| **Context** | Context-aware (belajar dari window) | Bag-of-words (tidak peduli order) |
| **OOV Handling** | Masalah (kata tidak di vocab = diabaikan) | Tidak masalah (TF=0 untuk kata baru) |

### Support Vector Machine (SVM)

**Definisi:**

SVM adalah algoritma supervised learning untuk klasifikasi. Mencari hyperplane (bidang pemisah) terbaik yang memisahkan data dari dua kelas dengan margin maksimal.

**Cara Kerja:**

1. **Training Phase:**
   - Input: Vectors (150D untuk Skip-Gram, 3000D untuk TF-IDF)
   - Label: 0 (Finance) atau 1 (Sport)
   - Objective: Cari hyperplane w·x + b = 0 yang memisahkan kedua kelas
   - Constraint: Maximize margin (jarak ke support vectors)
   - Optimization: Quadratic programming

2. **Inference Phase:**
   - Input: New vector x
   - Decision: Sign(w·x + b)
     - Jika w·x + b > 0 → Class 1 (Sport)
     - Jika w·x + b < 0 → Class 0 (Finance)
   - Probability: Sigmoid transformation dari decision value (jika probability=True)

**Linear Kernel:**

```
Hyperplane: w1*x1 + w2*x2 + ... + w150*x150 + b = 0

Untuk Skip-Gram (150D):
Decision = w1*v1 + w2*v2 + ... + w150*v150 + b

Jika Decision > 0 → Sport
Jika Decision < 0 → Finance

Probability:
P(Sport) = 1 / (1 + exp(-Decision))
P(Finance) = 1 - P(Sport)
```

**Keunggulan:**

1. **Effective in High Dimensions:**
   - Bekerja baik untuk data high-dimensional (150D, 3000D)
   - Tidak mudah overfit (karena maximize margin)

2. **Memory Efficient:**
   - Hanya simpan support vectors (sebagian kecil dari training data)
   - Inference cepat

3. **Kernel Trick:**
   - Bisa gunakan kernel non-linear (RBF, polynomial)
   - Untuk data non-linearly separable

**Aplikasi di Proyek Ini:**

- Dua SVM terpisah: satu untuk Skip-Gram, satu untuk TF-IDF
- Kernel: Linear (data cukup linearly separable)
- Hyperparameter C=1.0 (regularization)
- Probability=True (untuk confidence score)

## Alur Klasifikasi Lengkap

### Metode Skip-Gram

```
Input: URL atau Text
    ↓
[Scraping] (jika URL)
    ↓
Raw Text: "JAKARTA - Timnas Indonesia U-23 menang 3-0 lawan Guinea..."
    ↓
[Noise Removal]
- Remove [Gambas:Video]
- Remove watermark (detikcom)
- Remove dateline (JAKARTA - )
- Lowercase
- Remove non-alphabet
    ↓
Cleaned Text: "timnas indonesia menang lawan guinea skor akhir"
    ↓
[Tokenization]
    ↓
Tokens: ["timnas", "indonesia", "menang", "lawan", "guinea", "skor", "akhir"]
    ↓
[Skip-Gram Embedding]
- "timnas" → [0.23, -0.45, 0.67, ..., 0.12] (150D) ✓ Matched
- "indonesia" → [-0.34, 0.56, 0.23, ..., 0.45] (150D) ✓ Matched
- "menang" → [0.67, 0.23, -0.23, ..., 0.11] (150D) ✓ Matched
- "lawan" → [0.12, 0.89, 0.34, ..., 0.56] (150D) ✓ Matched
- "guinea" → TIDAK ADA DI VOCABULARY → ✗ OOV
- "skor" → [0.45, -0.12, 0.67, ..., 0.34] (150D) ✓ Matched
- "akhir" → [0.23, 0.45, -0.12, ..., 0.67] (150D) ✓ Matched
    ↓
Statistics:
- Total tokens: 7
- Matched: 6
- OOV: 1
- Coverage: 85.7%
    ↓
[Mean Pooling]
Document Vector = (v1 + v2 + v3 + v4 + v6 + v7) / 6
                = [0.15, 0.11, 0.08, ..., 0.23] (150D)
    ↓
[SVM Classification]
Input: [0.15, 0.11, 0.08, ..., 0.23]
Decision Function: w·x + b = 2.34
Probability: P(Sport) = 1/(1+exp(-2.34)) = 0.912 = 91.2%
             P(Finance) = 1 - 0.912 = 0.088 = 8.8%
    ↓
Output:
- Category: Sport
- Confidence: 91.2%
- Probabilities: {Sport: 91.2%, Finance: 8.8%}
- Vector: [0.15, 0.11, 0.08, ...]
```

### Metode TF-IDF

```
Input: URL atau Text
    ↓
[Scraping] (jika URL)
    ↓
Raw Text: "Menteri Perhubungan Dudy Purwagandhi buka suara soal kehadiran taksi online asal Vietnam..."
    ↓
[Noise Removal]
    ↓
Cleaned Text: "menteri perhubungan dudy purwagandhi buka suara soal kehadiran taksi online asal vietnam..."
    ↓
[Stopword Removal]
Stopwords dihapus: "soal", "di", "yang", "ini", "dari", "untuk", ...
    ↓
After Stopword: "menteri perhubungan dudy purwagandhi buka suara kehadiran taksi online asal vietnam..."
    ↓
[Stemming Sastrawi]
- "menteri" → "menteri"
- "perhubungan" → "hubung"
- "buka" → "buka"
- "kehadiran" → "hadir"
- "taksi" → "taksi"
- "melakukan" → "laku"
    ↓
Processed Text: "menteri hubung dudy purwagandhi buka suara hadir taksi online asal vietnam..."
    ↓
[TF-IDF Vectorization]
Vocabulary: 3000 features
Text ini mengandung 62 unique terms dari vocabulary

TF-IDF Calculation:
- "taksi": TF=0.0058, IDF=2.15, TF-IDF=0.5174
- "dudy": TF=0.0058, IDF=3.91, TF-IDF=0.5187
- "vietnam": TF=0.0058, IDF=2.78, TF-IDF=0.2217
- "online": TF=0.0115, IDF=1.85, TF-IDF=0.2218
- ... (62 terms total, 2938 terms = 0)
    ↓
Vector (3000D sparse):
[0, 0, 0.5174, 0, 0, 0.2218, ..., 0, 0.5187, 0, ...]
Active: 62 features
Zero: 2938 features
    ↓
[SVM Classification]
Input: Sparse vector 3000D
Decision Function: w·x + b = 0.35
Probability: P(Finance) = 1/(1+exp(-0.35)) = 0.587 = 58.7%
             P(Sport) = 1 - 0.587 = 0.413 = 41.3%
    ↓
Output:
- Category: Finance
- Confidence: 58.7%
- Probabilities: {Finance: 58.7%, Sport: 41.3%}
- Top Keywords: [taksi: 0.5174, dudy: 0.5187, online: 0.2218, ...]
- Vector: [0, 0, 0.5174, ...]
```

## Fitur Aplikasi

### 1. Dual-Method Selection

User dapat memilih salah satu metode sebelum klasifikasi:

**Skip-Gram (Word2Vec) - Mean Vector:**
- Preprocessing: Hanya pembersihan noise
- Stopword removal: TIDAK digunakan
- Stemming: TIDAK digunakan
- Alasan: Word embedding butuh context penuh

**TF-IDF Vectorizer - Model TF-IDF:**
- Preprocessing: Pembersihan noise + Stopword Removal + Stemming Sastrawi
- Full NLP pipeline
- Alasan: TF-IDF berbasis frekuensi, stopwords harus dihapus

### 2. Input Flexibility

**Tab 1: Extract from URL**
- Paste URL artikel berita (Detikcom atau website lain)
- Tombol contoh: "Example: Sport Article", "Example: Finance Article"
- Otomatis scraping konten artikel
- Ekstrak metadata (title, author, date)

**Tab 2: Direct Text Input**
- Paste atau ketik teks artikel langsung
- Minimal 50 karakter
- Character counter real-time
- Tidak perlu scraping, langsung ke preprocessing

### 3. Classification Results

**Metric Cards:**
- Category: Sport atau Finance
- Confidence: Confidence score dalam persen
- Vocabulary Coverage (Skip-Gram): Persentase token yang match di vocabulary
- Active Features (TF-IDF): Jumlah features non-zero dari total vocabulary

**Probability Distribution Chart:**
- Horizontal bar chart interaktif (Plotly)
- Menampilkan probabilitas kedua kelas
- Ukuran bar sesuai persentase (FIXED)
- Warna: Orange (Sport), Blue (Finance)

### 4. Detailed Analysis Tabs

**Tab 1: Extracted Content**
- Article metadata lengkap (title, author, date, URL)
- Original content (scrollable, max height 300px)
- Tombol "Copy" dengan toast notification
- Text area enabled (bisa select dan copy dengan Ctrl+C)
- Statistics: Character count, word count

**Tab 2: Preprocessing Result**
- Method info: preprocessing yang digunakan
- Token statistics: total, matched/active, OOV/zero
- Processed text (scrollable, copyable)
- Sample matched tokens (untuk Skip-Gram)

**Tab 3: Feature Representation**
- Skip-Gram:
  - Dimension info (150D)
  - Representation method (Mean Word Vector)
  - Vector values sample (15 dimensions pertama)
  - Code block format (bisa copy)
  - Full vector dalam expander
- TF-IDF:
  - Dimension info (3000D, sparse)
  - Active features count
  - Top keywords dengan TF-IDF score (badges)
  - Sample TF-IDF values (15 non-zero pertama)
  - Full vector dalam expander

### 5. Progress Tracking

**4-Step Progress Bar:**
- Step 1: Extracting article content (scraping)
- Step 2: Preprocessing text (method-specific)
- Step 3: Classifying with [method name]
- Step 4: Complete

**Spinner dengan deskripsi:**
- "Scraping article..."
- "Cleaning and preprocessing..."
- "Running Skip-Gram embedding + SVM classification..."
- "Running TF-IDF Vectorizer classification..."

### 6. Model Information (Sidebar)

**Model Status:**
- Models Loaded Successfully (green box)

**Skip-Gram Model:**
- Vector Dimension: 150D
- Vocabulary Size: 4,015 words
- Window Size: 2
- Representation: Mean Word Vector (Rata-rata Vektor Kata)

**TF-IDF Model:**
- Vocabulary Size: 3,000 features
- Representation: TF-IDF Matrix (Term Frequency - Inverse Document Frequency)

**Training Dataset:**
- Total: 180 articles
- Sport: 90 articles
- Finance: 90 articles
- Split: 80% train, 20% test
- Bar chart distribusi dataset

### 7. Responsive Design

- Wide layout untuk maksimalkan space
- Sidebar collapsible
- Mobile-friendly (Streamlit responsive default)
- Professional blue/white/gray color scheme
- Clean dan minimal (tanpa clutter)

## Contoh Link Artikel untuk Testing

### Link Artikel Sport (10 contoh):

1. https://sport.detik.com/sepakbola/liga-indonesia/d-7128945/timnas-indonesia-u-23-vs-guinea-skor-akhir-3-0
2. https://sport.detik.com/sepakbola/liga-inggris/d-7605831/hasil-liga-inggris-tadi-malam-man-city-kalah-arsenal-menang
3. https://sport.detik.com/sepakbola/liga-spanyol/d-7604290/hasil-liga-spanyol-real-madrid-vs-barcelona-el-clasico-berakhir-imbang
4. https://sport.detik.com/basket/nba/d-7603125/hasil-nba-lakers-kalahkan-warriors-lebron-james-cetak-triple-double
5. https://sport.detik.com/raket/bulutangkis/d-7602456/indonesia-masters-2024-anthony-ginting-melaju-ke-semifinal
6. https://sport.detik.com/sepakbola/liga-italia/d-7601789/hasil-serie-a-inter-milan-pesta-gol-juventus-menang-tipis
7. https://sport.detik.com/moto-gp/d-7600234/motogp-2024-pecco-bagnaia-juara-dunia-untuk-kali-ketiga
8. https://sport.detik.com/sepakbola/piala-dunia/d-7599567/kualifikasi-piala-dunia-2026-indonesia-imbang-lawan-australia
9. https://sport.detik.com/tenis/d-7598890/atp-finals-2024-djokovic-kalah-alcaraz-melaju-ke-final
10. https://sport.detik.com/adv-sport-lain/d-7597123/formula-1-abu-dhabi-verstappen-juara-musim-ini

### Link Artikel Finance (10 contoh):

1. https://finance.detik.com/moneter/d-7128567/rupiah-menguat-ke-rp-15200-per-dolar-as-hari-ini
2. https://finance.detik.com/bursa-dan-valas/d-7605124/ihsg-ditutup-naik-09-persen-ke-level-7234
3. https://finance.detik.com/berita-ekonomi-bisnis/d-7604678/harga-emas-antam-hari-ini-naik-rp-10-ribu-per-gram
4. https://finance.detik.com/energi/d-7603901/harga-minyak-dunia-turun-di-tengah-kekhawatiran-ekonomi-global
5. https://finance.detik.com/moneter/d-7602345/bi-pertahankan-suku-bunga-acuan-di-level-6-persen
6. https://finance.detik.com/berita-ekonomi-bisnis/d-7601890/inflasi-oktober-2024-tercatat-1-55-persen-year-on-year
7. https://finance.detik.com/bursa-dan-valas/d-7600456/saham-bank-bri-naik-tajam-setelah-laba-kuartal-iii-melonjak
8. https://finance.detik.com/properti/d-7599123/penjualan-properti-residensial-tumbuh-positif-di-tahun-2024
9. https://finance.detik.com/industri/d-7598567/pt-telkom-indonesia-raih-laba-bersih-rp-25-triliun
10. https://finance.detik.com/moneter/d-7597234/pemerintah-terbitkan-obligasi-negara-senilai-rp-50-triliun

## Kebutuhan Sistem

### Development (Lokal)

**Operating System:**
- Windows 10/11
- macOS 11+
- Linux (Ubuntu 20.04+)

**Python:**
- Version: 3.11.10 (recommended)
- Installer: Miniconda atau Anaconda
- Virtual environment: conda environment "newsclassifier"

**Hardware:**
- RAM: Minimal 4 GB (recommended 8 GB)
- Storage: ~500 MB untuk environment dan models
- CPU: Multi-core recommended untuk training

**Internet:**
- Diperlukan untuk scraping URL
- Opsional untuk input text langsung

### Production (Streamlit Cloud)

**Python:**
- Version: 3.11.10 (otomatis dari .python-version)
- Runtime: Streamlit Cloud managed

**Resources:**
- RAM: 1 GB (free tier Streamlit Cloud)
- Storage: 100 MB limit untuk repository
- CPU: Shared (free tier)

**Build:**
- Build time: ~3-5 menit
- Auto-rebuild on git push

**URL:**
- Public URL: https://[username]-[repo].streamlit.app/
- Contoh: https://wahyu402191-news-classifier.streamlit.app/

## Instalasi dan Menjalankan Aplikasi

### Setup Environment

1. **Install Miniconda:**
   - Download dari: https://docs.conda.io/en/latest/miniconda.html
   - Install sesuai OS (Windows/Mac/Linux)

2. **Create Conda Environment:**
   ```bash
   conda create -n newsclassifier python=3.11.10
   conda activate newsclassifier
   ```

3. **Install Dependencies:**
   ```bash
   cd news-classifier-streamlit
   pip install -r requirements.txt
   ```

4. **Verify Installation:**
   ```bash
   python -c "import streamlit; import gensim; import sklearn; print('OK')"
   ```

### Menjalankan Aplikasi Lokal

**Windows:**
```bash
# Activate environment
conda activate newsclassifier

# Run aplikasi
streamlit run app.py

# Atau gunakan batch file
run_app.bat
```

**Mac/Linux:**
```bash
# Activate environment
conda activate newsclassifier

# Run aplikasi
streamlit run app.py
```

**Akses:**
- URL: http://localhost:8501
- Jika port 8501 sudah dipakai, Streamlit otomatis gunakan port lain (8502, 8503)
- Browser akan otomatis terbuka

**Stop Aplikasi:**
- Tekan Ctrl+C di terminal
- Atau tutup terminal

### Training Model (Opsional)

Jika ingin re-train model TF-IDF:

```bash
# Activate environment
conda activate newsclassifier

# Run training script
python train_tfidf_model.py

# Output:
# - models/tfidf_vectorizer.joblib
# - models/svm_tfidf_classifier.joblib
```

Model Skip-Gram sudah di-training sebelumnya (skipgram_model.model).

## Deployment ke Streamlit Cloud

### Persiapan

**Repository GitHub:**
- URL: https://github.com/Wahyu402191/news-classifier
- Branch: main
- File penting: app.py, requirements.txt, .python-version

**File Critical:**

1. **.python-version**
   ```
   3.11.10
   ```
   - Menentukan Python version untuk Streamlit Cloud
   - Python 3.12+ tidak support gensim 4.4.0

2. **requirements.txt**
   - Semua dependencies dengan version
   - Format: package>=version

3. **app.py**
   - Entry point aplikasi
   - Must be in root directory

### Langkah Deployment

1. **Login Streamlit Cloud:**
   - URL: https://share.streamlit.io/
   - Login dengan GitHub account

2. **Create New App:**
   - Click "New app"
   - Pilih repository: Wahyu402191/news-classifier
   - Branch: main
   - Main file path: app.py
   - (Python version otomatis detect dari .python-version)

3. **Deploy:**
   - Click "Deploy"
   - Tunggu build process (3-5 menit)
   - Monitor logs untuk cek progress

4. **Access App:**
   - URL: https://wahyu402191-news-classifier.streamlit.app/
   - Public accessible (siapa saja bisa akses)

### Update Deployment

**Automatic Update (Recommended):**

1. Push perubahan ke GitHub:
   ```bash
   git add .
   git commit -m "Update feature X"
   git push origin main
   ```

2. Streamlit Cloud otomatis detect perubahan (1-2 menit)

3. Auto-rebuild dan redeploy (2-3 menit)

4. Refresh browser untuk lihat perubahan

**Manual Reboot:**

1. Buka Streamlit Cloud dashboard
2. Pilih app "news-classifier"
3. Click menu (3 dots)
4. Click "Reboot app"
5. Tunggu rebuild selesai

### Monitor Deployment

**Build Logs:**
- Klik "Manage app" di dashboard
- Tab "Logs" untuk lihat build process
- Cek error jika build failed

**Common Issues:**

1. **Dependency Error:**
   - Cek requirements.txt version compatibility
   - Cek .python-version

2. **Model Loading Error:**
   - Pastikan model files ada di repository
   - Cek size limit (max 100 MB per file)

3. **Memory Error:**
   - Free tier Streamlit Cloud: 1 GB RAM
   - Optimize model size jika perlu

## Troubleshooting

### Error: Port 8501 already in use

**Penyebab:** Ada instance Streamlit lain yang sedang running

**Solusi 1 (Kill process):**
```bash
# Windows
taskkill /F /IM streamlit.exe

# Mac/Linux
pkill -f streamlit
```

**Solusi 2 (Use different port):**
```bash
streamlit run app.py --server.port 8502
```

### Error: Model file not found

**Penyebab:** Model file tidak ada di folder models/

**Solusi:**
```bash
# Cek apakah file ada
ls models/

# Expected files:
# - skipgram_model.model
# - svm_classifier.joblib
# - tfidf_vectorizer.joblib
# - svm_tfidf_classifier.joblib

# Jika TF-IDF model tidak ada, run training:
python train_tfidf_model.py
```

### Error: Scraping failed

**Penyebab:** Website punya anti-scraping protection atau koneksi internet bermasalah

**Solusi:**
- Cek koneksi internet
- Coba URL berbeda
- Gunakan "Direct Text Input" sebagai alternatif

### Error: ModuleNotFoundError (gensim, sklearn, etc)

**Penyebab:** Dependencies tidak terinstall

**Solusi:**
```bash
# Activate environment
conda activate newsclassifier

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "import gensim; import sklearn; print('OK')"
```

### Error: gensim build failed (Streamlit Cloud)

**Penyebab:** Python version terlalu baru (3.12+)

**Solusi:**
- Pastikan .python-version berisi 3.11.10
- Commit dan push ke GitHub
- Reboot app di Streamlit Cloud

### Bar chart probabilitas sama panjang

**Penyebab:** Bug di visualizer (nilai dikali 100 dua kali)

**Solusi:** Sudah diperbaiki di visualizer.py line 24

### Text area tidak bisa di-copy

**Penyebab:** Text area disabled=True

**Solusi:** Sudah diperbaiki, disabled=False di app.py

## Informasi Pengembang

**Developer:** Wahyu Pratama  
**GitHub:** https://github.com/Wahyu402191  
**Repository:** https://github.com/Wahyu402191/news-classifier  
**Year:** 2026  
**License:** MIT

## Credits

Dataset dikumpulkan dari detik.com (Sport dan Finance section) untuk keperluan edukasi dan penelitian akademik.

Libraries:
- Streamlit - Streamlit Inc.
- Gensim - RaRe Technologies
- scikit-learn - scikit-learn developers
- PySastrawi - har07
- trafilatura - Adrien Barbaresi
- Plotly - Plotly Technologies Inc.
