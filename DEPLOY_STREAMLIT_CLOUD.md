# 🚀 CARA DEPLOY KE STREAMLIT CLOUD (GRATIS SELAMANYA!)

## 📋 OVERVIEW

Streamlit Cloud adalah hosting gratis untuk aplikasi Streamlit. Kamu bisa deploy aplikasi ini secara gratis dan bisa diakses dari mana saja!

**Fitur Gratis:**
- ✅ Hosting gratis selamanya
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Custom domain (username.streamlit.app)
- ✅ Auto-deploy dari GitHub
- ✅ HTTPS otomatis

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### STEP 1: Buat Akun GitHub (Kalau Belum Punya)

1. Buka https://github.com
2. Klik **"Sign up"**
3. Isi email, password, username
4. Verifikasi email
5. Login ke GitHub

---

### STEP 2: Install Git di Komputer (Kalau Belum Ada)

1. Download Git: https://git-scm.com/download/win
2. Install dengan setting default (Next, Next, Finish)
3. Restart Command Prompt

**Test apakah Git sudah terinstall:**
```bash
git --version
```

Output: `git version 2.x.x` ✅

---

### STEP 3: Setup Git Config (Sekali Aja)

Buka Command Prompt, ketik:

```bash
git config --global user.name "Nama Kamu"
git config --global user.email "email@example.com"
```

Ganti dengan nama dan email GitHub kamu!

---

### STEP 4: Inisialisasi Git di Folder Aplikasi

Buka Command Prompt, navigate ke folder aplikasi:

```bash
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"
```

Inisialisasi Git:

```bash
git init
```

---

### STEP 5: Buat File .gitignore (Penting!)

Buat file `.gitignore` untuk exclude file yang tidak perlu di-upload:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Streamlit
.streamlit/secrets.toml

# Data (optional - kalau file data besar)
# data/*.csv

# Temporary
*.log
*.tmp
```

**Cara buat:** Buka Notepad, paste isi di atas, Save As → `.gitignore` (pilih "All Files", bukan "Text Document")

---

### STEP 6: Add & Commit Files

Di Command Prompt:

```bash
# Add semua file
git add .

# Commit
git commit -m "Initial commit: Detik News Classifier"
```

---

### STEP 7: Buat Repository di GitHub

1. Buka https://github.com
2. Login
3. Klik tombol **"+" (pojok kanan atas)** → **"New repository"**
4. Isi:
   - **Repository name**: `news-classifier` (atau nama lain)
   - **Description**: "Detik News Classifier using Streamlit"
   - **Public** (pilih ini - wajib untuk free Streamlit Cloud)
   - ❌ JANGAN centang "Add README"
5. Klik **"Create repository"**

---

### STEP 8: Push ke GitHub

GitHub akan kasih instruksi, copy command yang mirip ini:

```bash
git remote add origin https://github.com/USERNAME/news-classifier.git
git branch -M main
git push -u origin main
```

**Ganti `USERNAME` dengan username GitHub kamu!**

Paste ke Command Prompt, Enter.

**Nanti akan minta login GitHub:**
- Masukkan username GitHub
- Masukkan password (atau Personal Access Token kalau diminta)

**Output berhasil:**
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
...
To https://github.com/USERNAME/news-classifier.git
 * [new branch]      main -> main
```

---

### STEP 9: Verifikasi di GitHub

1. Refresh halaman repository di GitHub
2. Kamu akan lihat semua file aplikasi sudah ada:
   - `app.py`
   - `config.py`
   - `utils/`
   - `models/`
   - `requirements.txt`
   - dll.

✅ **Kalau semua file sudah muncul, BERHASIL!**

---

### STEP 10: Deploy di Streamlit Cloud

1. Buka https://share.streamlit.io
2. Klik **"Sign in"** → **"Continue with GitHub"**
3. Authorize Streamlit (klik "Authorize streamlit")
4. Klik **"New app"**
5. Isi form:
   - **Repository**: Pilih `USERNAME/news-classifier`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Ganti jadi nama custom, misalnya `detik-classifier`
6. Klik **"Deploy!"**

---

### STEP 11: Tunggu Deployment (3-5 Menit)

Streamlit akan:
1. ✅ Clone repository
2. ✅ Install dependencies dari `requirements.txt`
3. ✅ Run aplikasi
4. ✅ Generate URL

**Status yang muncul:**
```
🎈 Deploying your app...
Installing dependencies...
Building app...
✅ Your app is live!
```

---

### STEP 12: APLIKASI SUDAH ONLINE! 🎉

URL aplikasi kamu:
```
https://USERNAME-news-classifier.streamlit.app
```

Atau kalau pakai custom name:
```
https://detik-classifier.streamlit.app
```

**Aplikasi bisa diakses dari mana saja!**

---

## ⚠️ TROUBLESHOOTING DEPLOYMENT

### Problem 1: "Python version not found"

**Penyebab:** requirements.txt tidak specify Python version

**Solusi:** Buat file `.python-version` di root folder:

```
3.11
```

Atau tambahkan di `requirements.txt`:
```
python>=3.11,<3.12
```

---

### Problem 2: "Module not found"

**Penyebab:** Dependency tidak ada di `requirements.txt`

**Solusi:** Pastikan `requirements.txt` lengkap:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
gensim>=4.3.0
joblib>=1.3.0
PySastrawi>=1.2.0
trafilatura>=1.6.0
plotly>=5.17.0
```

Commit dan push lagi:
```bash
git add requirements.txt
git commit -m "Update requirements"
git push
```

Streamlit akan auto-redeploy!

---

### Problem 3: "Out of memory"

**Penyebab:** Model terlalu besar (>1 GB)

**Solusi:** 
- Compress model
- Atau pakai model yang lebih kecil
- Atau upgrade ke Streamlit Cloud Pro ($7/bulan)

---

### Problem 4: "App not loading"

**Penyebab:** Error di kode

**Solusi:** 
1. Cek logs di Streamlit Cloud dashboard
2. Fix error di kode lokal
3. Commit & push lagi

---

## 🔄 CARA UPDATE APLIKASI (Setelah Deploy)

Kalau kamu ubah kode, caranya:

```bash
# 1. Add changes
git add .

# 2. Commit
git commit -m "Fix scraping bug"

# 3. Push
git push
```

**Streamlit Cloud akan AUTO-REDEPLOY!** (dalam 1-2 menit)

---

## 📊 MONITORING APLIKASI

Di Streamlit Cloud dashboard (https://share.streamlit.io):

- ✅ Lihat status aplikasi (Running/Stopped/Error)
- ✅ Lihat logs real-time
- ✅ Lihat metrics (CPU, RAM usage)
- ✅ Restart aplikasi kalau error
- ✅ Delete aplikasi kalau tidak perlu

---

## 🎯 TIPS & BEST PRACTICES

### 1. **Gunakan secrets.toml untuk API keys** (kalau ada)

Buat file `.streamlit/secrets.toml` (lokal only, jangan push):
```toml
API_KEY = "your-secret-key"
```

Di Streamlit Cloud, add secrets via dashboard:
Settings → Secrets → Paste secrets

### 2. **Optimize model size**

Kalau model terlalu besar, compress atau pakai format yang lebih efisien

### 3. **Add caching**

Streamlit sudah pakai `@st.cache_resource` di kode, jadi model cuma load sekali

### 4. **Monitor performance**

Check dashboard regularly untuk lihat RAM usage

### 5. **Add README.md**

Buat README di GitHub untuk dokumentasi

---

## 📝 CHECKLIST DEPLOYMENT

- [ ] Git terinstall di komputer
- [ ] Akun GitHub sudah dibuat
- [ ] Repository GitHub sudah dibuat
- [ ] File `.gitignore` sudah ada
- [ ] `requirements.txt` lengkap
- [ ] Model files sudah di-commit (cek size <1 GB)
- [ ] Code sudah di-push ke GitHub
- [ ] Streamlit Cloud account sudah dibuat
- [ ] App sudah di-deploy
- [ ] App bisa diakses via URL
- [ ] Test semua fitur di production
- [ ] Share link ke teman/dosen!

---

## 🎉 LINK APLIKASI ONLINE

Setelah deploy, share link ini:

```
https://USERNAME-news-classifier.streamlit.app
```

**GRATIS SELAMANYA!** 🚀

---

## 📞 SUPPORT

**Dokumentasi Streamlit Cloud:**
https://docs.streamlit.io/streamlit-community-cloud

**GitHub Help:**
https://docs.github.com

**Git Tutorial:**
https://git-scm.com/doc

---

**Good luck deployment! 🚀**

Last updated: October 8, 2026
