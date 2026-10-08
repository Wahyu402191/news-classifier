# 🔧 CARA INSTALL GENSIM DI PYTHON 3.14

## ⚠️ MASALAH

Gensim versi 4.3.0+ belum tersedia dalam bentuk pre-compiled (wheel) untuk Python 3.14.4. Saat install, pip mencoba compile dari source code yang membutuhkan Microsoft Visual C++ 14.0 compiler.

**Error yang muncul:**
```
error: Microsoft Visual C++ 14.0 or greater is required.
ModuleNotFoundError: No module named 'trafilatura'
```

---

## ✅ SOLUSI 1: INSTALL MICROSOFT VISUAL C++ BUILD TOOLS (RECOMMENDED)

### Langkah-langkah:

1. **Download Visual Studio Build Tools**
   - Buka: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Download "Build Tools for Visual Studio 2022"
   - Ukuran installer: ~3 MB, size full install: ~6 GB

2. **Install Visual C++ Build Tools**
   - Jalankan installer
   - Pilih **"Desktop development with C++"**
   - Checklist:
     - [x] MSVC v143 - VS 2022 C++ x64/x86 build tools
     - [x] Windows 11 SDK (atau Windows 10 SDK)
   - Klik "Install"
   - Tunggu ~30-60 menit (download + install)

3. **Restart Computer** (important!)

4. **Install Gensim**
   ```bash
   pip install gensim==4.3.0
   ```

5. **Verifikasi**
   ```bash
   python -c "from gensim.models import Word2Vec; print('Gensim OK!')"
   ```

**Keuntungan:**
- ✅ Install gensim versi terbaru (4.3.0+)
- ✅ Bisa compile library Python lain yang butuh C++
- ✅ Solusi permanen

**Kekurangan:**
- ❌ Butuh download 6 GB
- ❌ Install lama (30-60 menit)
- ❌ Butuh restart computer

---

## ✅ SOLUSI 2: DOWNGRADE PYTHON KE VERSI 3.11 (ALTERNATIF)

Gensim punya pre-compiled wheel untuk Python 3.8 - 3.11, jadi tidak perlu compiler.

### Langkah-langkah:

1. **Download Python 3.11**
   - Buka: https://www.python.org/downloads/
   - Download Python 3.11.x (latest stable)
   - Install ke lokasi berbeda (misalnya: C:\Python311\)

2. **Buat Virtual Environment dengan Python 3.11**
   ```bash
   C:\Python311\python.exe -m venv venv311
   venv311\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Aplikasi**
   ```bash
   streamlit run app.py
   ```

**Keuntungan:**
- ✅ No compiler needed
- ✅ Install cepat (< 10 menit)
- ✅ Gensim langsung kerja

**Kekurangan:**
- ❌ Harus maintain 2 versi Python
- ❌ Python 3.11 lebih lama dari 3.14

---

## ✅ SOLUSI 3: GUNAKAN CONDA/MINICONDA (EASIEST!)

Conda/Miniconda punya pre-compiled gensim untuk semua platform.

### Langkah-langkah:

1. **Download Miniconda**
   - Buka: https://docs.conda.io/en/latest/miniconda.html
   - Download Windows 64-bit installer
   - Install (ukuran: ~400 MB)

2. **Buat Conda Environment**
   ```bash
   conda create -n newsclassifier python=3.11 -y
   conda activate newsclassifier
   ```

3. **Install Dependencies**
   ```bash
   conda install -c conda-forge gensim scikit-learn pandas numpy -y
   pip install streamlit PySastrawi trafilatura plotly joblib
   ```

4. **Run Aplikasi**
   ```bash
   streamlit run app.py
   ```

**Keuntungan:**
- ✅ No compiler needed
- ✅ Semua library science/ML pre-compiled
- ✅ Easy package management
- ✅ Industry standard untuk data science

**Kekurangan:**
- ❌ Butuh install Miniconda (~400 MB)
- ❌ Environment terpisah dari system Python

---

## 🚀 QUICK FIX: MODE DEMO (TEMPORARY)

Jika kamu mau lihat UI dulu tanpa prediksi aktual, saya bisa modifikasi kode untuk pakai **mock predictions** (prediksi palsu untuk testing).

Mode demo akan:
- ✅ Tampilkan full UI
- ✅ Scraping tetap jalan
- ✅ Preprocessing tetap jalan
- ✅ Prediksi pakai random (Sport/Finance 50/50)
- ✅ Visualisasi tetap jalan

Untuk enable mode demo, buat file `.env`:
```
DEMO_MODE=True
```

---

## 📋 REKOMENDASI

**Untuk Belajar/Development:**
→ **SOLUSI 3 (Conda/Miniconda)** - Paling mudah dan cepat

**Untuk Production/Deploy:**
→ **SOLUSI 1 (Visual C++ Build Tools)** - Paling proper

**Untuk Quick Test:**
→ **QUICK FIX (Mode Demo)** - Lihat UI dulu

---

## ❓ FAQ

### Q: Kenapa Python 3.14 tidak support?
A: Python 3.14 baru release, banyak library science/ML belum compile wheel-nya. Python 3.11 lebih stabil untuk data science.

### Q: Apakah harus install Visual Studio penuh?
A: TIDAK. Cukup "Build Tools for Visual Studio" (6 GB), tidak perlu Visual Studio IDE penuh (30+ GB).

### Q: Apakah Streamlit Cloud support Python 3.14?
A: Belum. Streamlit Cloud support Python 3.8 - 3.11. Jadi untuk deploy, harus pakai Python 3.11 max.

### Q: Bagaimana jika saya sudah punya VS Code?
A: VS Code ≠ Visual C++ compiler. Tetap harus install "Build Tools for Visual Studio".

---

## 📞 BANTUAN

Jika masih error, cek:
1. `python --version` - Pastikan Python version
2. `pip list | findstr gensim` - Cek gensim terinstall atau tidak
3. Error message lengkap - Share ke saya

---

**Updated:** October 7, 2026
