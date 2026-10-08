@echo off
echo ========================================
echo RUNNING NEWS CLASSIFIER APP
echo ========================================
echo.

REM Activate conda environment
call C:\Users\LAPTOP\miniconda3\Scripts\activate.bat newsclassifier

REM Navigate to app directory
cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"

REM Install trafilatura if not installed
echo Checking dependencies...
pip install trafilatura --quiet

REM Kill any existing Streamlit process
echo Stopping any existing Streamlit servers...
taskkill /F /IM streamlit.exe 2>nul

REM Run Streamlit app
echo.
echo Starting Streamlit app...
echo Browser will open automatically at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause
