# 📝 CARA INSTALL MANUAL (STEP-BY-STEP)

Ikuti langkah ini **satu per satu** di Command Prompt atau Anaconda Prompt.

---

## 🚀 LANGKAH 1: Buka Command Prompt / Anaconda Prompt

**Cara 1:** Tekan `Win + R`, ketik `cmd`, Enter

**Cara 2:** Cari di Start Menu: "Command Prompt" atau "Anaconda Prompt"

---

## 🐍 LANGKAH 2: Activate Conda Environment

Copy-paste command ini, tekan Enter:

```bash
C:\Users\LAPTOP\miniconda3\Scripts\activate.bat newsclassifier
```

**Hasil yang benar:**
- Prompt berubah jadi: `(newsclassifier) C:\...>`
- Atau muncul tulisan environment aktif

---

## 📦 LANGKAH 3: Install Streamlit

```bash
pip install streamlit
```

**Tunggu:** ~2-3 menit (download ~50 MB)

**Hasil yang benar:**
```
Successfully installed streamlit-1.x.x
```

---

## 📦 LANGKAH 4: Install PySastrawi

```bash
pip install PySastrawi
```

**Tunggu:** ~30 detik

**Hasil yang benar:**
```
Successfully installed PySastrawi-1.2.1
```

---

## 📦 LANGKAH 5: Install Trafilatura

```bash
pip install trafilatura
```

**Tunggu:** ~30 detik

**Hasil yang benar:**
```
Requirement already satisfied: trafilatura
ATAU
Successfully installed trafilatura-2.x.x
```

---

## 📦 LANGKAH 6: Install Plotly

```bash
pip install plotly
```

**Tunggu:** ~1 menit

**Hasil yang benar:**
```
Successfully installed plotly-5.x.x
```

---

## ✅ LANGKAH 7: Verifikasi Instalasi

Test apakah semua library terinstall dengan baik:

### Test 1: Gensim
```bash
python -c "from gensim.models import Word2Vec; print('✓ Gensim OK')"
```

### Test 2: Streamlit
```bash
python -c "import streamlit; print('✓ Streamlit OK')"
```

### Test 3: PySastrawi
```bash
python -c "from Sastrawi.Stemmer.StemmerFactory import StemmerFactory; print('✓ PySastrawi OK')"
```

### Test 4: Trafilatura
```bash
python -c "import trafilatura; print('✓ Trafilatura OK')"
```

### Test 5: Scikit-learn
```bash
python -c "import sklearn; print('✓ Scikit-learn OK')"
```

### Test 6: Pandas
```bash
python -c "import pandas; print('✓ Pandas OK')"
```

**Kalau semua muncul "✓ ... OK" → BERHASIL!** ✅

---

## 🚀 LANGKAH 8: Jalankan Aplikasi

```bash
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"
streamlit run app.py
```

**Hasil yang benar:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

**Buka browser, ketik:** `http://localhost:8501`

---

## ❓ TROUBLESHOOTING

### Problem 1: "conda is not recognized"
**Solusi:**
```bash
# Gunakan full path
C:\Users\LAPTOP\miniconda3\Scripts\conda.exe activate newsclassifier
```

### Problem 2: "pip is not recognized"
**Solusi:**
```bash
# Gunakan full path
C:\Users\LAPTOP\miniconda3\envs\newsclassifier\Scripts\pip.exe install streamlit
```

### Problem 3: CMD keluar tiba-tiba
**Penyebab:** Script .bat error atau environment belum aktif
**Solusi:** Pakai cara manual ini, step by step

### Problem 4: Install lama banget
**Normal!** Streamlit ukuran besar (~50 MB), tunggu aja 2-5 menit

### Problem 5: "ModuleNotFoundError" saat run app
**Solusi:** Pastikan environment aktif sebelum run:
```bash
conda activate newsclassifier
streamlit run app.py
```

---

## 📊 CHECKLIST

Centang kalau sudah selesai:

- [ ] Miniconda terinstall
- [ ] Environment `newsclassifier` dibuat (Python 3.11)
- [ ] Gensim terinstall (via conda)
- [ ] Scikit-learn terinstall (via conda)
- [ ] Pandas terinstall (via conda)
- [ ] Numpy terinstall (via conda)
- [ ] Streamlit terinstall (via pip)
- [ ] PySastrawi terinstall (via pip)
- [ ] Trafilatura terinstall (via pip)
- [ ] Plotly terinstall (via pip)
- [ ] Semua test verifikasi OK
- [ ] App berhasil jalan di browser

---

## 🎯 RINGKASAN COMMAND

Kalau mau cepat, copy-paste semua ini **satu per satu**:

```bash
# 1. Activate environment
C:\Users\LAPTOP\miniconda3\Scripts\activate.bat newsclassifier

# 2. Install packages
pip install streamlit
pip install PySastrawi
pip install trafilatura
pip install plotly

# 3. Verifikasi
python -c "from gensim.models import Word2Vec; print('✓ Gensim OK')"
python -c "import streamlit; print('✓ Streamlit OK')"
python -c "from Sastrawi.Stemmer.StemmerFactory import StemmerFactory; print('✓ PySastrawi OK')"
python -c "import trafilatura; print('✓ Trafilatura OK')"
python -c "import sklearn; print('✓ Scikit-learn OK')"
python -c "import pandas; print('✓ Pandas OK')"

# 4. Run app
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"
streamlit run app.py
```

---

**Good luck! 🚀**
