@echo off
echo ========================================
echo PUSH TO GITHUB - Wahyu402191
echo ========================================
echo.

cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

echo Repository URL: https://github.com/Wahyu402191/news-classifier-streamlit
echo.
echo Pushing 24 files to GitHub...
echo.
echo IMPORTANT: Login window akan muncul!
echo - Sign in with your browser ATAU
echo - Masukkan username: Wahyu402191
echo - Masukkan password/token GitHub kamu
echo.
pause

git push -u origin main

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Files pushed to GitHub
    echo.
    echo Next step:
    echo 1. Buka: https://github.com/Wahyu402191/news-classifier-streamlit
    echo 2. Verifikasi files sudah ter-upload
    echo 3. Deploy di: https://share.streamlit.io
) else (
    echo FAILED! Check error message above
    echo.
    echo Common issues:
    echo - Wrong username/password
    echo - Repository not created yet
    echo - Network problem
)
echo ========================================
echo.
pause
