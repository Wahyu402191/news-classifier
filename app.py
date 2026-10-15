"""
Detik News Classifier - Streamlit Application
Dual-method classification: Skip-Gram Word2Vec + TF-IDF
"""

import streamlit as st
import time
from pathlib import Path

# Import utilities
from utils.scraper import scrape_article, validate_url
from utils.preprocessor import preprocess_text, tokenize_text, get_text_statistics, clean_noise
from utils.dual_model_handler import load_dual_models, get_skipgram_info, get_tfidf_info, classify_with_method
from utils.visualizer import plot_probability_distribution, plot_dataset_distribution
from config import UI_CONFIG, COLOR_SCHEME


# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title=UI_CONFIG['page_title'],
    page_icon=UI_CONFIG['page_icon'],
    layout=UI_CONFIG['layout'],
    initial_sidebar_state=UI_CONFIG['initial_sidebar_state']
)


# CSS kustom untuk styling profesional
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
    
    /* Method selection card */
    .stRadio > label {
        font-weight: 600;
        font-size: 16px;
        color: #2c3e50;
    }
    
    /* Scrollable text area */
    .scrollable-text {
        max-height: 300px;
        overflow-y: auto;
        padding: 15px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Copy button */
    .copy-button {
        float: right;
        margin-bottom: 10px;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
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
    
    /* Vector display */
    .vector-box {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        overflow-x: auto;
        margin: 10px 0;
    }
    
    /* Feature badges */
    .feature-badge {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px;
        background-color: #e3f2fd;
        color: #1976d2;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def initialize_models():
    """Inisialisasi dan cache semua model (Skip-Gram dan TF-IDF)"""
    with st.spinner('Loading ML models...'):
        success = load_dual_models()
        skipgram_info = get_skipgram_info()
        tfidf_info = get_tfidf_info()
    return success, skipgram_info, tfidf_info


def render_sidebar():
    """Tampilkan sidebar dengan informasi model"""
    with st.sidebar:
        st.title("System Information")
        
        # Model status
        st.subheader("Model Status")
        try:
            success, skipgram_info, tfidf_info = initialize_models()
            
            if success:
                st.success("Models Loaded Successfully")
            
            # Skip-Gram Info
            if skipgram_info:
                st.markdown("**Skip-Gram Model:**")
                st.metric("Vector Dimension", f"{skipgram_info['vector_size']}D")
                st.metric("Vocabulary Size", f"{skipgram_info['vocab_size']:,} words")
                st.metric("Window Size", skipgram_info['window'])
                st.caption(skipgram_info['representation'])
            
            st.divider()
            
            # TF-IDF Info
            if tfidf_info:
                st.markdown("**TF-IDF Model:**")
                st.metric("Vocabulary Size", f"{tfidf_info['vocab_size']:,} features")
                st.caption(tfidf_info['representation'])
            
        except Exception as e:
            st.error(f"Model Loading Error: {str(e)}")
            st.stop()
        
        st.divider()
        
        # Dataset info
        st.subheader("Training Dataset")
        st.info("""
        **Total**: 180 articles  
        **Sport**: 90 articles  
        **Finance**: 90 articles  
        **Split**: 80% train, 20% test
        """)
        
        # Visualization
        fig_dataset = plot_dataset_distribution(90, 90)
        st.plotly_chart(fig_dataset, use_container_width=True)
        
        st.divider()
        
        # About
        st.subheader("About")
        st.caption("""
        News classification system with dual-method support:
        Skip-Gram Word2Vec and TF-IDF Vectorizer
        for automatic categorization of news articles.
        """)
        
        st.caption("© 2026 - Wahyu Pratama")


def render_method_selection():
    """Tampilkan pilihan metode klasifikasi"""
    st.subheader("Choose Classification Method")
    
    method = st.radio(
        "Select method:",
        options=["skipgram", "tfidf"],
        format_func=lambda x: "Skip-Gram (Word2Vec) - Mean Vector" if x == "skipgram" else "TF-IDF Vectorizer - Model TF-IDF",
        horizontal=False,
        key="classification_method"
    )
    
    # Info box untuk metode yang dipilih
    if method == "skipgram":
        st.info("""
        **Skip-Gram (Word2Vec)**  
        Preprocessing: Hanya pembersihan noise. Proses stopword removal & stemming TIDAK digunakan sesuai karakteristik word embedding.
        """)
    else:
        st.info("""
        **TF-IDF Vectorizer**  
        Preprocessing: Menggunakan Stopword Removal & Stemming Sastrawi lengkap dengan model klasifikasi TF-IDF khusus.
        """)
    
    return method


def render_input_section():
    """Tampilkan section input"""
    st.subheader("Input Article")
    
    # Tabs untuk URL atau Text
    tab1, tab2 = st.tabs(["Extract from URL", "Direct Text Input"])
    
    with tab1:
        # Session state untuk URL
        if 'loaded_url' not in st.session_state:
            st.session_state['loaded_url'] = ""
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Example: Sport Article", use_container_width=True, type="secondary", key="btn_sport"):
                st.session_state['loaded_url'] = "https://sport.detik.com/sepakbola/liga-indonesia/d-7128945/timnas-indonesia-u-23-vs-guinea-skor-akhir-3-0"
                st.rerun()
        
        with col2:
            if st.button("Example: Finance Article", use_container_width=True, type="secondary", key="btn_finance"):
                st.session_state['loaded_url'] = "https://finance.detik.com/moneter/d-7128567/rupiah-menguat-ke-rp-15200-per-dolar-as-hari-ini"
                st.rerun()
        
        url_input = st.text_input(
            "Article URL",
            value=st.session_state['loaded_url'],
            placeholder="https://sport.detik.com/... atau https://finance.detik.com/...",
            help="Paste URL artikel berita"
        )
        
        if url_input != st.session_state['loaded_url']:
            st.session_state['loaded_url'] = url_input
        
        return ('url', url_input)
    
    with tab2:
        text_input = st.text_area(
            "Article Content",
            height=250,
            placeholder="Paste full article text here (minimum 50 characters)...",
            help="Enter article content directly"
        )
        
        if text_input:
            st.caption(f"Character count: {len(text_input)}")
        
        return ('text', text_input)


def process_classification(input_type, input_data, method):
    """Proses klasifikasi berdasarkan input"""
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Extract content
    if input_type == 'url':
        status_text.text("Step 1/4: Extracting article content...")
        progress_bar.progress(25)
        
        if not validate_url(input_data):
            st.error("Invalid URL format. URL must start with http:// or https://")
            progress_bar.empty()
            status_text.empty()
            return
        
        with st.spinner("Scraping article..."):
            result = scrape_article(input_data)
            time.sleep(0.5)
        
        if result.get('error'):
            st.error(f"Scraping failed: {result['error']}")
            progress_bar.empty()
            status_text.empty()
            return
        
        raw_text = result['content']
        metadata = result
    else:
        if len(input_data) < 50:
            st.warning("Please enter at least 50 characters of text")
            return
        
        raw_text = input_data
        metadata = {'title': 'Direct Input', 'author': 'User', 'date': 'Now', 'url': None}
        progress_bar.progress(25)
    
    # Step 2: Preprocessing
    status_text.text("Step 2/4: Preprocessing text...")
    progress_bar.progress(50)
    
    with st.spinner("Cleaning and preprocessing..."):
        if method == 'skipgram':
            # Skip-Gram: Hanya noise removal (NO stopwords, NO stemming)
            cleaned_text = clean_noise(raw_text)
            tokens = tokenize_text(cleaned_text)
            processed_input = tokens  # Skip-Gram pakai token list
            processed_text = cleaned_text
        else:
            # TF-IDF: Full preprocessing (noise + stopwords + stemming)
            processed_text = preprocess_text(raw_text)
            tokens = tokenize_text(processed_text)
            processed_input = processed_text  # TF-IDF pakai string
        
        time.sleep(0.3)
    
    # Step 3: Classification
    method_label = "Skip-Gram Word2Vec" if method == 'skipgram' else "TF-IDF Vectorizer"
    status_text.text(f"Step 3/4: Classifying with {method_label}...")
    progress_bar.progress(75)
    
    with st.spinner(f"Running {method_label} classification..."):
        prediction_result = classify_with_method(processed_input, method)
        time.sleep(0.3)
    
    # Step 4: Complete
    status_text.text("Step 4/4: Complete!")
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    # Display results
    display_results(prediction_result, metadata, raw_text, processed_text, tokens, method)


def display_results(prediction, metadata, raw_text, processed_text, tokens, method):
    """Tampilkan hasil klasifikasi"""
    
    st.success("Classification Complete!")
    
    # Main result
    st.markdown("### Classification Result")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Category", prediction['prediction'])
    
    with col2:
        st.metric("Confidence", f"{prediction['confidence']:.1f}%")
    
    with col3:
        if method == 'skipgram':
            st.metric("Vocabulary Coverage", f"{prediction['vocab_coverage']:.1f}%")
        else:
            st.metric("Active Features", f"{prediction['active_features']}/{prediction['total_vocab']}")
    
    # Probability distribution
    st.markdown("### Probability Distribution")
    if prediction['probabilities']:
        fig_prob = plot_probability_distribution(prediction['probabilities'])
        st.plotly_chart(fig_prob, use_container_width=True)
    
    # Method info
    st.info(f"**Method Used**: {prediction['method_label']}")
    
    st.divider()
    
    # Tabs untuk detail
    tab1, tab2, tab3 = st.tabs([
        "Extracted Content",
        "Preprocessing Result",
        "Feature Representation"
    ])
    
    with tab1:
        st.markdown("#### Article Metadata")
        st.write(f"**Title**: {metadata.get('title', 'N/A')}")
        st.write(f"**Author**: {metadata.get('author', 'N/A')}")
        st.write(f"**Published**: {metadata.get('date', 'N/A')}")
        if metadata.get('url'):
            st.write(f"**URL**: [{metadata['url']}]({metadata['url']})")
        
        st.markdown("#### Original Content")
        st.caption(f"Total: {len(raw_text)} characters")
        
        # Tombol salin
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("📋 Copy", key="copy_original"):
                st.toast("Click the text area and Ctrl+C to copy", icon="ℹ️")
        
        # Text area dengan scroll (disabled=False agar bisa di-copy)
        st.text_area(
            "",
            raw_text,
            height=300,
            disabled=False,
            key="original_content",
            label_visibility="collapsed"
        )
    
    with tab2:
        preprocessing_label = "Noise Removal Only (No Stopwords, No Stemming)" if method == 'skipgram' else "Noise Removal + Stopword Removal + Stemming (Sastrawi)"
        
        st.markdown(f"#### Preprocessing: {preprocessing_label}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tokens", prediction['total_tokens'])
        
        if method == 'skipgram':
            col2.metric("Matched in Vocab", prediction['matched_tokens'])
            col3.metric("Out of Vocabulary", prediction['oov_tokens'])
        else:
            col2.metric("Active TF-IDF", prediction['active_features'])
            col3.metric("Zero Values", prediction['total_vocab'] - prediction['active_features'])
        
        st.markdown("#### Processed Text")
        
        # Tombol salin
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("📋 Copy", key="copy_processed"):
                st.toast("Click the text area and Ctrl+C to copy", icon="ℹ️")
        
        # Text area dengan scroll
        st.text_area(
            "",
            processed_text,
            height=250,
            disabled=False,
            key="processed_content",
            label_visibility="collapsed"
        )
        
        # Sample tokens
        if method == 'skipgram' and 'matched_sample' in prediction:
            with st.expander("Sample Matched Tokens (first 20)"):
                st.write(", ".join(prediction['matched_sample']))
    
    with tab3:
        st.markdown(f"#### {prediction['method_label']} - Feature Representation")
        
        if method == 'skipgram':
            st.markdown(f"**Dimension**: {prediction['vector_dimension']}D Vector")
            st.markdown(f"**Representation Method**: Mean Word Vector (Rata-rata Vektor Kata)")
            
            st.markdown("**Vector Values (First 15 dimensions):**")
            
            # Display vector sebagai code block yang bisa di-copy
            vector_str = str(prediction['vector_sample'])
            st.code(vector_str, language='python')
            
            # Full vector dalam expander
            with st.expander("View Full Vector (All Dimensions)"):
                full_vector_str = str(prediction['vector_full'])
                st.code(full_vector_str, language='python')
                st.caption(f"Total dimensions: {len(prediction['vector_full'])}")
        
        else:  # TF-IDF
            st.markdown(f"**Total Dimensions**: {prediction['vector_dimension']} Features (TF-IDF Matrix)")
            st.markdown(f"**Active Features**: {prediction['active_features']} (Non-zero values)")
            st.markdown(f"**Representation Method**: TF-IDF Matrix (Term Frequency - Inverse Document Frequency)")
            
            st.markdown("**Top Keywords by TF-IDF Score:**")
            
            # Display top features sebagai badges
            if 'top_features' in prediction and prediction['top_features']:
                html_badges = ""
                for feat in prediction['top_features']:
                    html_badges += f'<span class="feature-badge">{feat["word"]} <b>{feat["score"]}</b></span>'
                st.markdown(html_badges, unsafe_allow_html=True)
            
            st.markdown("**Sample TF-IDF Values (First 15 non-zero):**")
            
            # Display sample values
            if 'vector_sample' in prediction:
                sample_str = "[\n"
                for item in prediction['vector_sample']:
                    sample_str += f"  {item['feature']}: {item['value']}\n"
                sample_str += "]"
                st.code(sample_str, language='python')
            
            # Full vector dalam expander
            with st.expander("View Full TF-IDF Vector (All Features)"):
                full_vector_str = str(prediction['vector_full'])
                st.code(full_vector_str, language='python')
                st.caption(f"Total features: {len(prediction['vector_full'])}, Active: {prediction['active_features']}")


def main():
    """Fungsi utama aplikasi"""
    
    # Load custom CSS
    load_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.title("Detik News Classifier")
    st.caption("Dual-Method Classification System: Skip-Gram Word2Vec & TF-IDF Vectorizer")
    
    st.markdown("""
    Automated classification of news articles into **Sport** or **Finance** categories
    using two different machine learning approaches with different preprocessing strategies.
    """)
    
    st.divider()
    
    # Method selection
    method = render_method_selection()
    
    st.divider()
    
    # Input section
    input_type, input_data = render_input_section()
    
    st.divider()
    
    # Classify button
    if st.button("🚀 Classify Article", type="primary", use_container_width=True):
        if not input_data or (input_type == 'text' and len(input_data) < 50):
            st.warning("Please provide valid input (URL or text with at least 50 characters)")
            return
        
        process_classification(input_type, input_data, method)


if __name__ == "__main__":
    main()
