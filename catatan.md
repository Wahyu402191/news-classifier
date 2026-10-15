# Notes untuk Presentasi ke Dosen

## Ringkasan Perubahan

### 1. Komentar Lengkap di Semua Code
Semua file Python sudah ditambahkan komentar Indonesia yang jelas:
- `app.py`: Setiap fungsi ada penjelasan (render sidebar, proses klasifikasi, display hasil)
- `utils/scraper.py`: Penjelasan scraping, validasi URL, cleaning HTML
- `utils/preprocessor.py`: Pipeline preprocessing (noise removal, stopwords, stemming)
- `utils/model_handler.py`: Load model, doc-to-vector, prediksi kategori
- `utils/visualizer.py`: Buat chart probabilitas, token coverage, dataset

### 2. README.md Lengkap dan Detail
Satu-satunya file dokumentasi, mencakup:
- Deskripsi aplikasi
- Teknologi dan framework
- Arsitektur (tidak bisa dipisah backend-frontend)
- Struktur folder lengkap
- Penjelasan setiap file
- Metode ML (Skip-Gram, TF-IDF, SVM)
- Fitur aplikasi
- Cara menjalankan
- Deployment
- Troubleshooting

### 3. File MD yang Dihapus
- CARA_PENGGUNAAN.md
- DEPLOY_STREAMLIT_CLOUD.md
- DOKUMENTASI.md
- INSTALL_GENSIM.md
- INSTALL_MANUAL.md
- LANGKAH_PUSH.md
- PUSH_TO_GITHUB.md
- READY_TO_PUSH.md

Sekarang hanya ada **1 file README.md** yang sangat detail.

## Jawaban untuk Pertanyaan Dosen

### Q: Aplikasi ini pakai framework apa?
**A**: Streamlit (all-in-one framework Python untuk web app)

### Q: Bisa dipisah backend dan frontend seperti teman kamu?
**A**: Tidak bisa. Ini perbedaan arsitektur:
- **Teman (Ivan)**: FastAPI (backend) + HTML/CSS/JS (frontend terpisah)
- **Saya**: Streamlit (full-stack, frontend-backend jadi satu)
- Streamlit otomatis generate UI dari Python code, tidak perlu HTML/CSS/JS manual

### Q: Skip-Gram itu apa?
**A**: Word embedding yang ubah kata jadi vektor numerik (150 dimensi)
- Input: 1 kata center
- Output: Prediksi kata di sekitarnya (context)
- Hasil: Kata serupa punya vektor mirip
- Contoh: vektor("sepakbola") ≈ vektor("bola")

### Q: TF-IDF itu apa? Kenapa tidak dipakai?
**A**: TF-IDF = metode lain untuk representasi teks (frekuensi × rareness)
- Aplikasi ini pakai Skip-Gram saja (lebih baik semantic meaning)
- TF-IDF hanya hitung frekuensi, tidak tangkap makna
- Skip-Gram lebih modern untuk klasifikasi teks

### Q: SVM itu apa fungsinya?
**A**: Classifier yang pisahkan Sport vs Finance
- Input: Vektor 150 dimensi dari Skip-Gram
- Cari hyperplane (garis pemisah) terbaik
- Output: Kategori + confidence score

### Q: Dataset apa yang kamu pakai?
**A**: 180 artikel dari detik.com
- Sport: 90 artikel
- Finance: 90 artikel
- Split: 80% training, 20% testing
- Balanced dataset

### Q: Jelaskan preprocessing pipeline
**A**: 
1. Noise Removal: Hapus [Gambas], watermark, special characters
2. Lowercase: Ubah semua huruf jadi kecil
3. Stopword Removal: Hapus 750+ kata umum Indonesia (Sastrawi)
4. Stemming: Ubah ke bentuk dasar (berlari → lari) (Sastrawi)
5. Tokenization: Split jadi list kata

### Q: Cara kerja klasifikasi dari URL?
**A**:
1. Scraping: Download HTML, ekstrak konten (trafilatura)
2. Preprocessing: Bersihkan teks (noise, stopwords, stemming)
3. Tokenization: Split jadi list kata
4. Skip-Gram: Ubah setiap kata jadi vektor 150D
5. Mean Pooling: Rata-rata semua vektor kata = document vector
6. SVM: Prediksi kategori dari document vector
7. Output: Sport/Finance + confidence + visualisasi

### Q: Aplikasi ini sudah deploy?
**A**: Ya, di Streamlit Cloud (gratis)
- URL: https://wahyu402191-news-classifier.streamlit.app/
- GitHub: https://github.com/Wahyu402191/news-classifier
- Otomatis update kalau push ke GitHub

### Q: Cara update deployment kalau ada perubahan?
**A**: 
```bash
git add .
git commit -m "Update aplikasi"
git push origin main
```
Streamlit Cloud otomatis detect dan rebuild.

### Q: Fitur apa saja yang ada?
**A**:
1. Input URL (scraping otomatis)
2. Input Text langsung
3. Preprocessing otomatis
4. Klasifikasi real-time
5. Confidence score
6. Vocabulary coverage
7. Visualisasi interaktif (Plotly)
8. Detail hasil (metadata, statistics, token analysis)

### Q: Kenapa pakai Python 3.11.10?
**A**: Kompatibilitas dengan gensim 4.4.0
- Python 3.12+ belum support gensim 4.4.0
- File `.python-version` penting untuk Streamlit Cloud

### Q: Apa kelebihan aplikasi kamu dibanding teman?
**A**:
1. **Simple deployment**: Streamlit Cloud gratis vs VPS berbayar
2. **Clean code**: Python only vs HTML/CSS/JS terpisah
3. **Professional UI**: Theme biru/putih minimal (tanpa emoji berlebihan)
4. **Interactive visualization**: Plotly charts
5. **Comprehensive documentation**: README detail, komentar lengkap

## Tips Presentasi

1. **Demo Live**: Buka aplikasi, coba scraping URL Sport dan Finance
2. **Tunjukkan Code**: Buka app.py, jelaskan fungsi utama dengan komentar
3. **Tunjukkan README**: Scroll section Skip-Gram vs TF-IDF
4. **Tunjukkan Hasil**: Confidence score, vocabulary coverage, visualisasi
5. **Jelaskan Pipeline**: URL → Scraping → Preprocessing → Skip-Gram → SVM → Hasil

## Contoh URL untuk Demo

**Sport:**
- https://sport.detik.com/sepakbola/liga-indonesia/d-7128945/timnas-indonesia-u-23-vs-guinea-skor-akhir-3-0

**Finance:**
- https://finance.detik.com/moneter/d-7128567/rupiah-menguat-ke-rp-15200-per-dolar-as-hari-ini

## Struktur Presentasi yang Disarankan

1. **Intro** (2 menit)
   - Nama aplikasi: Detik News Classifier
   - Tujuan: Klasifikasi otomatis artikel Sport/Finance
   - Framework: Streamlit + Skip-Gram + SVM

2. **Demo** (5 menit)
   - Buka aplikasi
   - Input URL Sport → Lihat hasil
   - Input URL Finance → Lihat hasil
   - Jelaskan confidence score dan visualisasi

3. **Teknologi** (5 menit)
   - Framework: Streamlit (all-in-one)
   - ML: Skip-Gram Word2Vec + SVM
   - NLP: Sastrawi (stopwords, stemming)
   - Visualization: Plotly

4. **Pipeline** (3 menit)
   - Scraping → Preprocessing → Tokenization
   - Skip-Gram embedding → Mean pooling
   - SVM classification → Output

5. **Code Walkthrough** (3 menit)
   - Buka app.py, jelaskan fungsi utama
   - Buka preprocessor.py, jelaskan pipeline
   - Buka model_handler.py, jelaskan prediksi

6. **Q&A** (2 menit)
   - Siap jawab pertanyaan dosen

Total: 20 menit

## Kesimpulan

- Aplikasi sudah lengkap dengan komentar detail
- README sangat comprehensive (tanpa emoji)
- Siap untuk presentasi dan deployment
- GitHub: https://github.com/Wahyu402191/news-classifier
