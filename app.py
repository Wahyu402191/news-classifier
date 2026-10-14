"""
Detik News Classifier - Streamlit Application
Professional news classification using Skip-Gram Word2Vec + SVM
"""

import streamlit as st
import time
from pathlib import Path

# Import utilities - modul untuk scraping, preprocessing, model, dan visualisasi
from utils.scraper import scrape_article, validate_url
from utils.preprocessor import preprocess_text, tokenize_text, get_text_statistics
from utils.model_handler import load_models, predict_category, get_model_info
from utils.visualizer import (
    plot_probability_distribution,
    plot_token_statistics,
    plot_dataset_distribution
)
from config import UI_CONFIG, COLOR_SCHEME


# Konfigurasi halaman Streamlit (title, icon, layout)
st.set_page_config(
    page_title=UI_CONFIG['page_title'],
    page_icon=UI_CONFIG['page_icon'],
    layout=UI_CONFIG['layout'],
    initial_sidebar_state=UI_CONFIG['initial_sidebar_state']
)


# CSS kustom untuk styling profesional (warna biru, putih, abu-abu)
def load_custom_css():
    """Load custom CSS untuk styling aplikasi"""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #ffffff;
    }
    
    /* Headers */
    h1 {
        color: #2c3e50;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 600;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0;
    }
    
    h2, h3 {
        color: #34495e;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
    }
    
    /* Success/Error boxes */
    .element-container div[data-baseweb="notification"] {
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f8f9fa;
        border-radius: 6px;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #f5f5f5;
        border-radius: 6px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 6px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource  # Cache agar model tidak di-load berulang kali
def initialize_models():
    """Inisialisasi model Skip-Gram dan SVM (hanya load sekali)"""
    with st.spinner('Loading ML models...'):
        models = load_models()  # Load Skip-Gram dan SVM
        info = get_model_info()  # Ambil info model (dimensi, vocab, dll)
    return models, info


def render_sidebar():
    """Tampilkan sidebar dengan informasi model dan dataset"""
    with st.sidebar:
        st.title("System Information")
        
        # Informasi model yang sedang digunakan
        st.subheader("Model Status")
        try:
            # Load model Skip-Gram dan SVM
            skipgram, svm = initialize_models()[0]
            info = get_model_info()
            
            st.success("Models Loaded Successfully")
            
            # Tampilkan spesifikasi model
            st.markdown("**Skip-Gram Model:**")
            st.metric("Vector Dimension", f"{info['vector_size']}D")  # Dimensi vektor word embedding
            st.metric("Vocabulary Size", f"{info['vocab_size']:,} words")  # Jumlah kata dalam vocabulary
            st.metric("Context Window", info['window'])  # Window size Skip-Gram
            
            st.markdown("**SVM Classifier:**")
            st.caption("Linear kernel with probability estimation")
            
        except Exception as e:
            st.error(f"Model Loading Error: {str(e)}")
            st.stop()
        
        st.divider()
        
        # Informasi dataset training
        st.subheader("Training Dataset")
        st.info("""
        **Total**: 180 articles  
        **Sport**: 90 articles  
        **Finance**: 90 articles  
        **Split**: 80% train, 20% test
        """)
        
        # Visualisasi distribusi dataset (pie chart)
        fig_dataset = plot_dataset_distribution(90, 90)
        st.plotly_chart(fig_dataset, use_container_width=True)
        
        st.divider()
        
        # About
        st.subheader("About")
        st.caption("""
        News classification system using Skip-Gram Word2Vec 
        and Support Vector Machine for automatic categorization 
        of Detikcom articles.
        """)
        
        st.caption("© 2026 - Wahyu Pratama")


def render_url_input_tab():
    """Tampilkan tab input URL untuk scraping artikel"""
    st.subheader("Extract from URL")
    st.caption("Paste a news article URL to automatically extract and classify content")
    
    # Session state untuk menyimpan URL (agar tidak hilang saat refresh)
    if 'loaded_url' not in st.session_state:
        st.session_state['loaded_url'] = ""
    
    # Tombol contoh URL (Sport dan Finance)
    col1, col2 = st.columns(2)
    with col1:
        # Tombol load contoh artikel Sport
        if st.button("Load Sport Example", use_container_width=True, type="secondary", key="btn_sport"):
            st.session_state['loaded_url'] = "https://sport.detik.com/sepakbola/liga-indonesia/d-7128945/timnas-indonesia-u-23-vs-guinea-skor-akhir-3-0"
            st.rerun()
    
    with col2:
        # Tombol load contoh artikel Finance
        if st.button("Load Finance Example", use_container_width=True, type="secondary", key="btn_finance"):
            st.session_state['loaded_url'] = "https://finance.detik.com/moneter/d-7128567/rupiah-menguat-ke-rp-15200-per-dolar-as-hari-ini"
            st.rerun()
    
    # Input URL dari user
    url = st.text_input(
        "Article URL",
        value=st.session_state['loaded_url'],
        placeholder="https://sport.detik.com/...",
        help="Enter a valid news article URL (must start with http:// or https://)"
    )
    
    # Update session state jika user ketik manual
    if url != st.session_state['loaded_url']:
        st.session_state['loaded_url'] = url
    
    st.divider()
    
    # Tombol untuk mulai klasifikasi
    if st.button("Classify Article", type="primary", use_container_width=True):
        # Validasi URL tidak kosong
        if not url:
            st.warning("Please enter a URL first")
            return
        
        # Validasi format URL
        if not validate_url(url):
            st.error("Invalid URL format. URL must start with http:// or https://")
            return
        
        # Proses klasifikasi dari URL
        process_url_classification(url)


def render_text_input_tab():
    """Tampilkan tab input teks langsung (tanpa scraping)"""
    st.subheader("Direct Text Input")
    st.caption("Paste or type article content directly for classification")
    
    # Area input teks
    text_input = st.text_area(
        "Article Content",
        height=250,
        placeholder="Paste news article text here (minimum 50 characters)...",
        help="Enter the full article content for classification"
    )
    
    # Hitung jumlah karakter
    if text_input:
        st.caption(f"Character count: {len(text_input)}")
    
    st.divider()
    
    # Tombol untuk mulai klasifikasi
    if st.button("Classify Text", type="primary", use_container_width=True):
        # Validasi minimal 50 karakter
        if not text_input or len(text_input) < 50:
            st.warning("Please enter at least 50 characters of text")
            return
        
        # Proses klasifikasi dari teks langsung
        process_text_classification(text_input)


def process_url_classification(url: str):
    """Proses klasifikasi dari URL (scraping -> preprocessing -> prediksi)"""
    
    # Progress bar untuk tracking proses
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Scraping artikel dari URL
    status_text.text("Step 1/4: Extracting article content...")
    progress_bar.progress(25)
    
    with st.spinner("Scraping article..."):
        result = scrape_article(url)  # Ekstrak konten artikel
        time.sleep(0.5)  # Pause singkat untuk UX
    
    # Cek jika scraping gagal
    if result.get('error'):
        st.error(f"Scraping failed: {result['error']}")
        progress_bar.empty()
        status_text.empty()
        return
    
    content = result['content']
    
    # Step 2: Preprocessing (noise removal, stopwords, stemming)
    status_text.text("Step 2/4: Preprocessing text...")
    progress_bar.progress(50)
    
    with st.spinner("Cleaning and preprocessing..."):
        processed_text = preprocess_text(content)  # Bersihkan teks
        tokens = tokenize_text(processed_text)  # Tokenisasi ke list kata
        time.sleep(0.3)
    
    # Step 3: Klasifikasi dengan Skip-Gram + SVM
    status_text.text("Step 3/4: Classifying content...")
    progress_bar.progress(75)
    
    with st.spinner("Running Skip-Gram embedding + SVM classification..."):
        prediction_result = predict_category(tokens)  # Prediksi kategori
        time.sleep(0.3)
    
    # Step 4: Selesai
    status_text.text("Step 4/4: Complete!")
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    # Tampilkan hasil klasifikasi
    display_classification_results(
        prediction_result,
        result,
        content,
        processed_text,
        tokens
    )


def process_text_classification(text: str):
    """Proses klasifikasi dari teks langsung (preprocessing -> prediksi)"""
    
    # Progress bar untuk tracking proses
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Preprocessing (noise removal, stopwords, stemming)
    status_text.text("Step 1/2: Preprocessing text...")
    progress_bar.progress(50)
    
    with st.spinner("Processing..."):
        processed_text = preprocess_text(text)  # Bersihkan teks
        tokens = tokenize_text(processed_text)  # Tokenisasi
        time.sleep(0.3)
    
    # Step 2: Klasifikasi dengan Skip-Gram + SVM
    status_text.text("Step 2/2: Classifying content...")
    progress_bar.progress(75)
    
    with st.spinner("Running Skip-Gram embedding + SVM classification..."):
        prediction_result = predict_category(tokens)  # Prediksi kategori
        time.sleep(0.3)
    
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    # Tampilkan hasil klasifikasi
    display_classification_results(
        prediction_result,
        {'title': 'Direct Input', 'author': 'User', 'date': 'Now', 'url': None},
        text,
        processed_text,
        tokens
    )


def display_classification_results(prediction, metadata, raw_text, processed_text, tokens):
    """Tampilkan hasil klasifikasi dalam layout terstruktur"""
    
    st.success("Classification Complete")
    
    # Hasil prediksi utama
    st.markdown("### Classification Result")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Kategori hasil prediksi (Sport/Finance)
        st.metric(
            "Category",
            prediction['prediction'],
            help="Predicted news category"
        )
    
    with col2:
        # Confidence score (persentase keyakinan model)
        st.metric(
            "Confidence",
            f"{prediction['confidence']:.1f}%",
            help="Model confidence score"
        )
    
    with col3:
        # Vocabulary coverage (berapa % kata yang dikenali model)
        coverage_pct = prediction['vocab_coverage']
        st.metric(
            "Vocabulary Coverage",
            f"{coverage_pct:.1f}%",
            help="Percentage of tokens found in Skip-Gram vocabulary"
        )
    
    # Visualisasi distribusi probabilitas (bar chart)
    st.markdown("### Probability Distribution")
    if prediction['probabilities']:
        fig_prob = plot_probability_distribution(prediction['probabilities'])
        st.plotly_chart(fig_prob, use_container_width=True)
    
    # Expander penjelasan Skip-Gram
    with st.expander("How does Skip-Gram classification work?"):
        st.markdown("""
        **Classification Pipeline:**
        
        1. **Preprocessing**: Clean text, remove stopwords, stemming
        2. **Tokenization**: Split into individual words
        3. **Skip-Gram Embedding**: Each word → 150D vector
           - Example: "sepakbola" → [0.23, -0.45, 0.67, ..., 0.12]
        4. **Mean Pooling**: Average all word vectors → document vector (150D)
        5. **SVM Classification**: Classify document vector → Sport or Finance
        6. **Confidence Score**: SVM decision function probability
        
        **Why Skip-Gram?**
        - Captures semantic meaning (similar words have similar vectors)
        - Better than TF-IDF for understanding context
        - Compact representation (150D vs thousands of dimensions)
        """)
    
    st.divider()
    
    # Tab detail informasi (metadata, konten, preprocessing, token)
    tab1, tab2, tab3, tab4 = st.tabs([
        "Article Metadata",
        "Content Preview",
        "Preprocessing Results",
        "Token Analysis"
    ])
    
    with tab1:
        # Metadata artikel (title, author, tanggal, URL)
        st.markdown("#### Article Information")
        st.write(f"**Title**: {metadata.get('title', 'N/A')}")
        st.write(f"**Author**: {metadata.get('author', 'N/A')}")
        st.write(f"**Published**: {metadata.get('date', 'N/A')}")
        if metadata.get('url'):
            st.write(f"**URL**: [{metadata['url']}]({metadata['url']})")
        
        # Statistik konten artikel
        stats = get_text_statistics(raw_text)
        st.markdown("#### Content Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Characters", f"{stats['char_count']:,}")
        col2.metric("Words", stats['word_count'])
        col3.metric("Sentences", stats['sentence_count'])
        col4.metric("Avg Word Length", f"{stats['avg_word_length']:.1f}")
    
    with tab2:
        # Preview konten asli (1000 karakter pertama)
        st.markdown("#### Original Content")
        st.caption("First 1000 characters of extracted content")
        st.text_area(
            "",
            raw_text[:1000] + ("..." if len(raw_text) > 1000 else ""),
            height=300,
            disabled=True
        )
    
    with tab3:
        # Hasil preprocessing (setelah noise removal, stopwords, stemming)
        st.markdown("#### Preprocessed Text")
        st.caption("After noise removal, stopword removal, and stemming (Sastrawi)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Words", len(raw_text.split()))
        with col2:
            st.metric("After Processing", len(tokens))
        
        st.text_area(
            "",
            processed_text[:1000] + ("..." if len(processed_text) > 1000 else ""),
            height=200,
            disabled=True
        )
    
    with tab4:
        # Analisis token (matched vs out-of-vocabulary)
        st.markdown("#### Token Statistics (Skip-Gram Vocabulary)")
        
        st.caption("""
        Tokens are converted to 150D vectors using Skip-Gram Word2Vec model. 
        Matched tokens have vector representation, OOV tokens are ignored.
        """)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tokens", prediction['total_tokens'])
        col2.metric("Matched", prediction['matched_tokens'])  # Kata yang ada di vocabulary
        col3.metric("Out of Vocabulary", prediction['oov_tokens'])  # Kata yang tidak dikenali
        
        # Visualisasi coverage token (pie chart)
        if prediction['matched_tokens'] > 0:
            fig_tokens = plot_token_statistics(
                prediction['matched_tokens'],
                prediction['oov_tokens']
            )
            st.plotly_chart(fig_tokens, use_container_width=True)
        
        # Sample 50 token pertama
        with st.expander("View Sample Tokens (first 50)"):
            sample_tokens = tokens[:50]
            st.write(", ".join(sample_tokens))


def main():
    """Fungsi utama aplikasi - entry point"""
    
    # Load CSS kustom
    load_custom_css()
    
    # Tampilkan sidebar (model info, dataset info)
    render_sidebar()
    
    # Konten utama
    st.title("Detik News Classifier")
    st.caption("Automated classification of news articles using Machine Learning")
    
    st.markdown("""
    This application uses **Skip-Gram Word2Vec** for word embedding and 
    **Support Vector Machine (SVM)** for classification of news articles 
    into **Sport** or **Finance** categories.
    """)
    
    # Info box tentang metode
    st.info("""
    **Machine Learning Pipeline:**
    1. Skip-Gram Word2Vec (150D vectors) - Word embedding
    2. Mean Pooling - Document vector representation  
    3. SVM Classifier (Linear kernel) - Binary classification
    """)
    
    st.divider()
    
    # Tab input (URL atau Text langsung)
    tab1, tab2 = st.tabs(["URL Input", "Text Input"])
    
    with tab1:
        render_url_input_tab()  # Tab scraping dari URL
    
    with tab2:
        render_text_input_tab()  # Tab input teks langsung


# Entry point aplikasi
if __name__ == "__main__":
    main()
