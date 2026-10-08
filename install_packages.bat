@echo off
echo ========================================
echo INSTALLING PACKAGES FOR NEWS CLASSIFIER
echo ========================================
echo.

REM Activate conda environment
call C:\Users\LAPTOP\miniconda3\Scripts\activate.bat newsclassifier

echo Step 1/3: Installing core ML packages (gensim, scikit-learn, numpy, pandas)...
echo This will take 5-10 minutes (downloading ~188 MB)...
conda install -c conda-forge gensim scikit-learn pandas numpy -y

echo.
echo Step 2/3: Installing Streamlit and other packages...
pip install streamlit PySastrawi trafilatura plotly joblib

echo.
echo Step 3/3: Verifying installation...
python -c "from gensim.models import Word2Vec; print('✓ Gensim OK')"
python -c "import streamlit; print('✓ Streamlit OK')"
python -c "from Sastrawi.Stemmer.StemmerFactory import StemmerFactory; print('✓ PySastrawi OK')"
python -c "import trafilatura; print('✓ Trafilatura OK')"
python -c "import sklearn; print('✓ Scikit-learn OK')"
python -c "import pandas; print('✓ Pandas OK')"

echo.
echo ========================================
echo INSTALLATION COMPLETE!
echo ========================================
echo.
echo To run the app:
echo   1. cd "c:\Users\LAPTOP\OneDrive\Dokumen\PPW\news-classifier-streamlit"
echo   2. streamlit run app.py
echo.
pause
