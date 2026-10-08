# 🚀 LANGKAH PUSH KE GITHUB - MUDAH!

## ✅ STATUS:
- ✅ 27 files sudah di-commit
- ✅ Remote URL sudah dikonfigurasi
- ⚠️ Repository GitHub **BELUM DIBUAT**

---

## 📝 LANGKAH 1: BUAT REPOSITORY DI GITHUB (WAJIB!)

### Cara Cepat:
1. **Buka link ini:** https://github.com/new
   
2. **Isi form:**
   - **Repository name:** `news-classifier-streamlit` (HARUS SAMA!)
   - **Description:** `Detik News Classifier using Skip-Gram and SVM`
   - **Visibility:** Pilih **Public** ✅
   
3. **PENTING - Jangan centang apapun:**
   - ❌ Add a README file
   - ❌ Add .gitignore  
   - ❌ Choose a license
   
4. **Klik tombol hijau:** "Create repository"

5. **JANGAN IKUTI** instruksi di halaman berikutnya! Langsung ke langkah 2.

---

## 📤 LANGKAH 2: PUSH FILES

### Cara A: Pakai Script (TERMUDAH!)

**Double-click file ini:**
```
push_to_github.bat
```

Lokasi: Di folder `news-classifier-streamlit`

**Yang akan terjadi:**
1. CMD window muncul
2. Akan ada proses push
3. **Login window akan muncul** - pilih "Sign in with browser"
4. Browser buka → Login GitHub
5. Klik "Authorize"
6. Tunggu upload (27 files, ~10 MB)
7. ✅ Done!

---

### Cara B: Manual di Command Prompt

```cmd
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"
git push -u origin main
```

Login kalau diminta (cara sama seperti Cara A).

---

## 🔐 LOGIN GITHUB (Kalau Diminta)

Akan muncul window login. **PILIH SALAH SATU:**

### Opsi 1: Sign in with Browser (RECOMMENDED ✅)
1. Klik "Sign in with your browser"
2. Browser akan terbuka
3. Login dengan akun GitHub kamu
4. Klik "Authorize git-credential-manager"
5. Done!

### Opsi 2: Username + Personal Access Token
**Username:** `Wahyu402191`  
**Password:** Pakai **Personal Access Token** (bukan password biasa!)

**Cara buat token:**
1. GitHub → Settings (pojok kanan atas)
2. Scroll bawah → Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. Note: `Streamlit Deploy`
6. Expiration: `90 days`
7. Centang: ✅ `repo` (full control)
8. Generate token
9. **COPY token** (hanya muncul 1x!)
10. Paste sebagai password

---

## ✅ VERIFIKASI BERHASIL

Setelah push berhasil, di CMD akan muncul:

```
Enumerating objects: 35, done.
Counting objects: 100% (35/35), done.
Delta compression using up to 8 threads
Compressing objects: 100% (30/30), done.
Writing objects: 100% (35/35), 6.50 MiB | 2.15 MiB/s, done.
Total 35 (delta 2), reused 0 (delta 0), pack-reused 0
To https://github.com/Wahyu402191/news-classifier-streamlit.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**Cek di browser:**
```
https://github.com/Wahyu402191/news-classifier-streamlit
```

Kamu akan lihat:
- ✅ 27 files
- ✅ models/ folder (2 files)
- ✅ data/ folder (2 files)
- ✅ utils/ folder (4 files)
- ✅ Semua dokumentasi (.md files)
- ✅ README.md terbuka otomatis

---

## 🌐 LANGKAH 3: DEPLOY KE STREAMLIT CLOUD

Setelah push berhasil:

1. **Buka:** https://share.streamlit.io

2. **Sign in:** Klik "Continue with GitHub"

3. **New app:** Klik tombol "New app"

4. **Isi form:**
   - **Repository:** `Wahyu402191/news-classifier-streamlit`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** `wahyu-detik-classifier` (atau custom)

5. **Deploy!** Klik tombol "Deploy!"

6. **Tunggu 3-5 menit** - Streamlit akan:
   - Install dependencies dari requirements.txt
   - Setup Python 3.11
   - Load model files
   - Start aplikasi

7. ✅ **Aplikasi online!**

**URL Final:**
```
https://wahyu-detik-classifier.streamlit.app
```

**GRATIS SELAMANYA!** 🎉

---

## 📋 CHECKLIST LENGKAP:

- [ ] Buka https://github.com/new
- [ ] Buat repository `news-classifier-streamlit` (public, no README)
- [ ] Klik "Create repository"
- [ ] Double-click `push_to_github.bat`
- [ ] Login GitHub (sign in with browser)
- [ ] Tunggu upload selesai
- [ ] Buka https://github.com/Wahyu402191/news-classifier-streamlit
- [ ] Verifikasi 27 files ada semua
- [ ] Buka https://share.streamlit.io
- [ ] Sign in dengan GitHub
- [ ] Deploy aplikasi
- [ ] Tunggu 3-5 menit
- [ ] Test aplikasi online
- [ ] ✅ Share link ke dosen/teman!

---

## ❓ TROUBLESHOOTING

### "Repository not found"
✅ **Penyebab:** Repository belum dibuat di GitHub  
🔧 **Solusi:** Buat dulu di https://github.com/new (langkah 1)

### "Authentication failed"
✅ **Penyebab:** Belum login atau token salah  
🔧 **Solusi:** Login lagi, atau generate Personal Access Token baru

### "Permission denied"
✅ **Penyebab:** Repository dibuat dengan username berbeda  
🔧 **Solusi:** Pastikan repository dibuat dengan username `Wahyu402191`

### Push lambat/stuck
✅ **Penyebab:** Internet lambat, file besar (model 6 MB)  
🔧 **Solusi:** Tunggu aja, biasanya 2-5 menit

### "Large files detected"
✅ **Penyebab:** Model file 6.2 MB mendekati limit  
🔧 **Solusi:** Masih OK, GitHub limit 100 MB per file

---

## 📊 FILE YANG AKAN DI-UPLOAD:

Total: **27 files** (~10 MB)

### Core Files (3):
- app.py (14 KB)
- config.py (2 KB)
- requirements.txt (1 KB)

### Models (2):
- skipgram_model.model (6.2 MB) ⬅️ File terbesar
- svm_classifier.joblib (74 KB)

### Data (2):
- detik_sport_90.csv (90 articles)
- detik_finance_90.csv (89 articles)

### Utils (5):
- __init__.py
- scraper.py (4 KB)
- preprocessor.py (3 KB)
- model_handler.py (5 KB)
- visualizer.py (4 KB)

### Documentation (8):
- README.md (5 KB)
- DOKUMENTASI.md (12 KB)
- CARA_PENGGUNAAN.md (8 KB)
- DEPLOY_STREAMLIT_CLOUD.md (7 KB)
- INSTALL_MANUAL.md (6 KB)
- INSTALL_GENSIM.md (5 KB)
- PUSH_TO_GITHUB.md (4 KB)
- READY_TO_PUSH.md (3 KB)
- LANGKAH_PUSH.md (ini file)

### Config (3):
- .gitignore
- .python-version
- .streamlit/config.toml

### Helper Scripts (3):
- install_packages.bat
- run_app.bat
- push_to_github.bat
- setup_data.py

---

## 🎯 RINGKASAN:

**3 Langkah Mudah:**

1. **Buat repository** di GitHub (2 menit)
2. **Push files** dengan double-click `push_to_github.bat` (3-5 menit)
3. **Deploy** di Streamlit Cloud (3-5 menit)

**Total waktu: ~10 menit**

**Hasil:** Aplikasi online, bisa diakses dari mana aja! 🚀

---

**MULAI DARI LANGKAH 1 SEKARANG!**

Buka: https://github.com/new

Last updated: October 8, 2026
