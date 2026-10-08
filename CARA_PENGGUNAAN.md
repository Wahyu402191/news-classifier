# 🚀 CARA PENGGUNAAN APLIKASI

## ✅ STATUS: APLIKASI SUDAH SIAP DIGUNAKAN!

Aplikasi **Detik News Classifier** sudah berhasil dibuat dan sedang berjalan!

---

## 🌐 AKSES APLIKASI (LOKAL)

Aplikasi sedang berjalan di:

- **Local URL**: http://localhost:8501
- **Network URL**: http://192.168.1.17:8501
- **External URL**: http://182.8.68.246:8501

**Cara Mengakses:**
1. Buka browser (Chrome, Firefox, Edge)
2. Ketik: `http://localhost:8501`
3. Tekan Enter

---

## 📱 CARA MENGGUNAKAN APLIKASI

### Mode 1: Klasifikasi dari URL

1. Pilih tab **"URL Input"**
2. Paste URL berita Detikcom (contoh: `https://sport.detik.com/...`)
3. Atau klik tombol **"Load Sport Example"** atau **"Load Finance Example"**
4. Klik tombol **"Classify Article"**
5. Tunggu proses (2-3 detik):
   - Step 1: Scraping artikel
   - Step 2: Preprocessing teks
   - Step 3: Klasifikasi
   - Step 4: Selesai
6. Lihat hasil klasifikasi:
   - **Category**: Sport atau Finance
   - **Confidence**: Persentase keyakinan model
   - **Vocabulary Coverage**: Persentase kata yang dikenali

### Mode 2: Klasifikasi dari Teks Langsung

1. Pilih tab **"Text Input"**
2. Ketik atau paste teks berita (minimal 50 karakter)
3. Klik tombol **"Classify Text"**
4. Tunggu proses (1-2 detik)
5. Lihat hasil klasifikasi

### Fitur Detail Results

Setelah klasifikasi, kamu bisa lihat detail di 4 tab:

**Tab 1: Article Metadata**
- Judul, penulis, tanggal
- Statistik: jumlah karakter, kata, kalimat

**Tab 2: Content Preview**
- Preview konten artikel asli (1000 karakter pertama)

**Tab 3: Preprocessing Results**
- Teks setelah dibersihkan dan di-preprocessing
- Perbandingan jumlah kata: before vs after

**Tab 4: Token Analysis**
- Total tokens, matched, out-of-vocabulary
- Visualization token coverage (pie chart)
- Sample tokens (50 pertama)

### Sidebar Information

Di sidebar (kiri), kamu bisa lihat:
- **Model Status**: Status loading model
- **Vector Dimension**: 150D
- **Vocabulary Size**: Jumlah kata yang dikenali
- **Context Window**: 3
- **Training Dataset**: 180 artikel (90 Sport + 90 Finance)
- **Dataset Distribution Chart**: Visualisasi balanced dataset
- **About**: Informasi aplikasi

---

## 🎨 DESAIN & UI

### Karakteristik Desain:
- ✅ **Professional & Clean**: Tidak ada emoji berlebihan
- ✅ **Color Scheme**: Blue, white, gray (berbeda dari Ivan)
- ✅ **Typography**: Segoe UI, Arial (readable)
- ✅ **Minimal**: Fokus pada konten dan data
- ✅ **Interactive Charts**: Plotly (hover untuk detail)
- ✅ **Progress Indicators**: User tahu proses sedang berjalan
- ✅ **Responsive**: Fit di layar desktop dan tablet

### Perbedaan dari Aplikasi Ivan:
| Aspek | Ivan | Aplikasi Kamu |
|-------|------|---------------|
| Framework | FastAPI + HTML/CSS/JS | Streamlit |
| Warna | Purple gradient | Blue professional |
| Emoji | Beberapa | Minimal |
| Dataset | 100+100 = 200 | 90+90 = 180 |
| Model | Dim 200, Win 2 | Dim 150, Win 3 |
| Deploy | VPS (bayar) | Streamlit Cloud (gratis) |

---

## ⚙️ INFORMASI TEKNIS

### File Structure:
```
news-classifier-streamlit/
├── app.py                    # Main application (14KB)
├── config.py                 # Configuration
├── utils/
│   ├── scraper.py           # Web scraping
│   ├── preprocessor.py      # NLP processing
│   ├── model_handler.py     # ML models
│   └── visualizer.py        # Plotly charts
├── models/
│   ├── skipgram_model.model # Word2Vec (6.2 MB)
│   └── svm_classifier.joblib # SVM (74 KB)
├── data/
│   ├── detik_sport_90.csv   # Training data
│   └── detik_finance_90.csv # Training data
└── requirements.txt          # Dependencies
```

### Model Information:
- **Word Embedding**: Skip-Gram Word2Vec
- **Vector Dimension**: 150
- **Context Window**: 3
- **Vocabulary Size**: ~7,000 kata
- **Classifier**: Linear SVM (Support Vector Machine)
- **Akurasi**: ~97% (pada test set)

### Processing Pipeline:
1. **Scraping** → trafilatura (ekstrak konten utama)
2. **Noise Removal** → Hapus HTML, special chars, angka
3. **Stopword Removal** → Sastrawi (750+ stopwords ID)
4. **Stemming** → Sastrawi (imbuhan Bahasa Indonesia)
5. **Word Embedding** → Skip-Gram (kata → vektor 150D)
6. **Classification** → SVM (vektor → kategori)

---

## 🛑 CARA MENGHENTIKAN APLIKASI

Jika ingin stop server:
1. Kembali ke terminal/command prompt
2. Tekan `Ctrl + C`
3. Atau tutup terminal

---

## 🚀 CARA MENJALANKAN LAGI

Jika sudah di-stop, untuk menjalankan lagi:

```bash
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"
streamlit run app.py
```

Aplikasi akan buka otomatis di browser.

---

## ☁️ DEPLOYMENT KE STREAMLIT CLOUD (GRATIS)

### Langkah Deploy Online:

#### 1. Push ke GitHub

```bash
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

# Initialize git (jika belum)
git init

# Add semua file
git add .

# Commit
git commit -m "Initial commit: Detik News Classifier"

# Connect ke GitHub (ganti USERNAME dengan username GitHub kamu)
git remote add origin https://github.com/USERNAME/news-classifier.git

# Push
git push -u origin main
```

#### 2. Deploy di Streamlit Cloud

1. Buka https://share.streamlit.io
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih:
   - **Repository**: `USERNAME/news-classifier`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Klik **"Deploy!"**
6. Tunggu 3-5 menit
7. Aplikasi akan online di: `https://USERNAME-news-classifier.streamlit.app`

#### 3. Share Link

Setelah deploy, kamu bisa share link ke teman/dosen:
```
https://USERNAME-news-classifier.streamlit.app
```

**Streamlit Cloud = 100% GRATIS SELAMANYA!**

---

## 📊 CONTOH PENGGUNAAN

### Contoh URL yang Bisa Dicoba:

**Sport:**
- https://sport.detik.com/sepakbola/liga-indonesia/...
- https://sport.detik.com/raket/...
- https://sport.detik.com/basket/...

**Finance:**
- https://finance.detik.com/moneter/...
- https://finance.detik.com/bursa-dan-valas/...
- https://finance.detik.com/fintech/...

### Contoh Teks yang Bisa Dicoba:

**Sport:**
```
Timnas Indonesia berhasil meraih kemenangan gemilang dengan skor 3-1 
melawan Thailand pada laga persahabatan. Pemain bintang Egy Maulana 
Vikri mencetak dua gol cantik di babak kedua. Pelatih Shin Tae-yong 
sangat puas dengan performa anak asuhnya.
```

**Finance:**
```
Nilai tukar rupiah terhadap dolar AS menguat ke level Rp 15.200 per 
dolar pada perdagangan hari ini. Penguatan rupiah didorong oleh sentimen 
positif dari rilis data inflasi yang terkendali. Bank Indonesia memproyeksikan 
rupiah akan stabil di kisaran Rp 15.000-15.500.
```

---

## ❓ TROUBLESHOOTING

### Problem: "ModuleNotFoundError"
**Solusi:**
```bash
pip install -r requirements.txt
```

### Problem: "Model file not found"
**Solusi:**
```bash
python setup_data.py
```

### Problem: "Port 8501 already in use"
**Solusi:**
```bash
streamlit run app.py --server.port 8502
```

### Problem: Browser tidak terbuka otomatis
**Solusi:**
Buka manual: http://localhost:8501

---

## 📞 SUPPORT

File dokumentasi lengkap ada di:
- `DOKUMENTASI.md` → Dokumentasi teknis lengkap
- `README.md` → Project overview
- `CARA_PENGGUNAAN.md` → File ini (user guide)

---

## ✅ CHECKLIST

- [x] Setup data & models berhasil
- [x] Dependencies terinstall
- [x] Aplikasi berjalan di localhost
- [ ] Push ke GitHub (optional)
- [ ] Deploy ke Streamlit Cloud (optional)
- [ ] Share link ke teman/dosen (optional)

---

**Selamat menggunakan aplikasi! 🎉**

Aplikasi kamu berbeda dari Ivan, lebih simple, clean, dan profesional!

**Developer:** Wahyu Pratama  
**Date:** October 7, 2026  
**Framework:** Streamlit (Python)
