# 📤 CARA PUSH KE GITHUB

## ✅ STATUS SEKARANG:

- ✅ Git repository sudah di-init
- ✅ 24 files sudah di-commit
- ✅ Siap untuk di-push ke GitHub!

---

## 🚀 LANGKAH PUSH KE GITHUB:

### STEP 1: Buat Repository di GitHub

1. Buka https://github.com
2. Login dengan akun GitHub kamu
3. Klik tombol **"+"** (pojok kanan atas) → **"New repository"**
4. Isi form:
   - **Repository name**: `news-classifier-streamlit` (atau nama lain)
   - **Description**: `Detik News Classifier using Skip-Gram Word2Vec and SVM`
   - **Visibility**: **Public** (wajib untuk Streamlit Cloud gratis)
   - ❌ **JANGAN centang** "Add a README file"
   - ❌ **JANGAN centang** "Add .gitignore"
   - ❌ **JANGAN centang** "Choose a license"
5. Klik **"Create repository"**

---

### STEP 2: Push dari Komputer ke GitHub

Setelah buat repository, GitHub akan kasih instruksi. Copy dan jalankan command ini di Command Prompt atau PowerShell:

**GANTI `YOUR_USERNAME` dengan username GitHub kamu!**

```bash
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

git remote add origin https://github.com/YOUR_USERNAME/news-classifier-streamlit.git

git branch -M main

git push -u origin main
```

---

### STEP 3: Login (Kalau Diminta)

Nanti akan muncul window login GitHub:
- Pilih **"Sign in with your browser"**
- Atau masukkan **Personal Access Token** kalau sudah punya

**Cara buat Personal Access Token (kalau belum punya):**

1. GitHub → Settings (profile pojok kanan atas)
2. Scroll ke bawah → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Isi:
   - **Note**: `Streamlit App Deploy`
   - **Expiration**: `90 days` (atau custom)
   - **Select scopes**: ✅ Centang **`repo`** (full control of private repositories)
6. Klik **Generate token**
7. **COPY TOKEN** (hanya muncul sekali!)
8. Paste token sebagai password saat git push

---

### STEP 4: Verifikasi

Setelah push berhasil, refresh halaman repository di GitHub. Kamu akan lihat:

```
✅ .gitignore
✅ .python-version
✅ .streamlit/config.toml
✅ app.py
✅ config.py
✅ requirements.txt
✅ models/skipgram_model.model (6.2 MB)
✅ models/svm_classifier.joblib (74 KB)
✅ data/detik_sport_90.csv
✅ data/detik_finance_90.csv
✅ utils/ (4 files)
✅ DOKUMENTASI.md
✅ CARA_PENGGUNAAN.md
✅ DEPLOY_STREAMLIT_CLOUD.md
✅ README.md
✅ Dan semua file lainnya
```

Total: **24 files**

---

## 🎯 SETELAH PUSH BERHASIL:

### Deploy ke Streamlit Cloud:

1. Buka https://share.streamlit.io
2. **Sign in** → **Continue with GitHub**
3. Klik **"New app"**
4. Isi:
   - **Repository**: `YOUR_USERNAME/news-classifier-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (custom): `detik-classifier` (atau terserah)
5. Klik **"Deploy!"**
6. Tunggu 3-5 menit
7. ✅ **Aplikasi online!**

URL: `https://detik-classifier.streamlit.app`

---

## ⚠️ TROUBLESHOOTING:

### Problem: "Permission denied (publickey)"

**Solusi:** Pakai HTTPS (bukan SSH) untuk remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/news-classifier-streamlit.git
```

### Problem: "Authentication failed"

**Solusi:** Pakai Personal Access Token sebagai password

### Problem: "File size too large"

**Solusi:** Model file (6.2 MB) masih OK untuk GitHub. Tapi kalau ada file >100 MB, pakai Git LFS:
```bash
git lfs install
git lfs track "*.model"
```

---

## 📝 COMMAND LENGKAP (COPY-PASTE INI):

```bash
# 1. Navigate ke folder
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

# 2. Add remote (GANTI YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/news-classifier-streamlit.git

# 3. Rename branch ke main
git branch -M main

# 4. Push ke GitHub
git push -u origin main
```

**GANTI `YOUR_USERNAME` dengan username GitHub kamu!**

Contoh:
- Kalau username GitHub: `johndoe`
- Maka: `https://github.com/johndoe/news-classifier-streamlit.git`

---

## ✅ CHECKLIST:

- [ ] Buka https://github.com
- [ ] Login ke GitHub
- [ ] Buat repository baru (public, no README)
- [ ] Copy repository URL
- [ ] Buka Command Prompt/PowerShell
- [ ] Run command `git remote add origin ...`
- [ ] Run command `git push -u origin main`
- [ ] Login GitHub (kalau diminta)
- [ ] Refresh repository page
- [ ] Verifikasi 24 files sudah ter-upload
- [ ] Deploy di https://share.streamlit.io
- [ ] Share link aplikasi!

---

**Selamat! Aplikasi kamu akan segera online! 🚀**

Last updated: October 8, 2026
