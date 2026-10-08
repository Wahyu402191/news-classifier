"""
Detik News Classifier - Streamlit Application
Professional news classification using Skip-Gram Word2Vec + SVM
"""

import streamlit as st
import time
from pathlib import Path

# Import utilities
from utils.scraper import scrape_article, validate_url
from utils.preprocessor import preprocess_text, tokenize_text, get_text_statistics
from utils.model_handler import load_models, predict_category, get_model_info
from utils.visualizer import (
    plot_probability_distribution,
    plot_token_statistics,
    plot_dataset_distribution
)
from config import UI_CONFIG, COLOR_SCHEME


# Page configuration
st.set_page_config(
    page_title=UI_CONFIG['page_title'],
    page_icon=UI_CONFIG['page_icon'],
    layout=UI_CONFIG['layout'],
    initial_sidebar_state=UI_CONFIG['initial_sidebar_state']
)


# Custom CSS for professional styling (minimal, clean)
def load_custom_css():
    """Load custom CSS for professional styling"""
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


@st.cache_resource
def initialize_models():
    """Initialize and cache models"""
    with st.spinner('Loading ML models...'):
        models = load_models()
        info = get_model_info()
    return models, info


def render_sidebar():
    """Render sidebar with model information and settings"""
    with st.sidebar:
        st.title("System Information")
        
        # Model info
        st.subheader("Model Status")
        try:
            skipgram, svm = initialize_models()[0]
            info = get_model_info()
            
            st.success("Models Loaded Successfully")
            
            st.metric("Vector Dimension", f"{info['vector_size']}D")
            st.metric("Vocabulary Size", f"{info['vocab_size']:,} words")
            st.metric("Context Window", info['window'])
            
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
        News classification system using Skip-Gram Word2Vec 
        and Support Vector Machine for automatic categorization 
        of Detikcom articles.
        """)
        
        st.caption("© 2026 - Wahyu Pratama")


def render_url_input_tab():
    """Render URL input interface"""
    st.subheader("Extract from URL")
    st.caption("Paste a news article URL to automatically extract and classify content")
    
    # Initialize session state for URL
    if 'loaded_url' not in st.session_state:
        st.session_state['loaded_url'] = ""
    
    # Quick examples
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load Sport Example", use_container_width=True, type="secondary"):
            st.session_state['loaded_url'] = "https://sport.detik.com/sepakbola/liga-indonesia/d-7128945/timnas-indonesia-u-23-vs-guinea-skor-akhir-3-0"
    
    with col2:
        if st.button("Load Finance Example", use_container_width=True, type="secondary"):
            st.session_state['loaded_url'] = "https://finance.detik.com/moneter/d-7128567/rupiah-menguat-ke-rp-15200-per-dolar-as-hari-ini"
    
    # URL input (use session state value)
    url = st.text_input(
        "Article URL",
        value=st.session_state['loaded_url'],
        placeholder="https://sport.detik.com/...",
        key="url_input",
        help="Enter a valid news article URL (must start with http:// or https://)"
    )
    
    st.divider()
    
    # Classify button
    if st.button("Classify Article", type="primary", use_container_width=True):
        if not url:
            st.warning("Please enter a URL first")
            return
        
        if not validate_url(url):
            st.error("Invalid URL format. URL must start with http:// or https://")
            return
        
        # Process URL
        process_url_classification(url)


def render_text_input_tab():
    """Render direct text input interface"""
    st.subheader("Direct Text Input")
    st.caption("Paste or type article content directly for classification")
    
    # Text area
    text_input = st.text_area(
        "Article Content",
        height=250,
        placeholder="Paste news article text here (minimum 50 characters)...",
        help="Enter the full article content for classification"
    )
    
    # Character count
    if text_input:
        st.caption(f"Character count: {len(text_input)}")
    
    st.divider()
    
    # Classify button
    if st.button("Classify Text", type="primary", use_container_width=True):
        if not text_input or len(text_input) < 50:
            st.warning("Please enter at least 50 characters of text")
            return
        
        # Process text
        process_text_classification(text_input)


def process_url_classification(url: str):
    """Process URL classification workflow"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Scraping
    status_text.text("Step 1/4: Extracting article content...")
    progress_bar.progress(25)
    
    with st.spinner("Scraping article..."):
        result = scrape_article(url)
        time.sleep(0.5)  # Brief pause for UX
    
    if result.get('error'):
        st.error(f"Scraping failed: {result['error']}")
        progress_bar.empty()
        status_text.empty()
        return
    
    content = result['content']
    
    # Step 2: Preprocessing
    status_text.text("Step 2/4: Preprocessing text...")
    progress_bar.progress(50)
    
    with st.spinner("Cleaning and preprocessing..."):
        processed_text = preprocess_text(content)
        tokens = tokenize_text(processed_text)
        time.sleep(0.3)
    
    # Step 3: Classification
    status_text.text("Step 3/4: Classifying content...")
    progress_bar.progress(75)
    
    with st.spinner("Running classification model..."):
        prediction_result = predict_category(tokens)
        time.sleep(0.3)
    
    # Step 4: Complete
    status_text.text("Step 4/4: Complete!")
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    # Display results
    display_classification_results(
        prediction_result,
        result,
        content,
        processed_text,
        tokens
    )


def process_text_classification(text: str):
    """Process direct text classification workflow"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Preprocessing
    status_text.text("Step 1/2: Preprocessing text...")
    progress_bar.progress(50)
    
    with st.spinner("Processing..."):
        processed_text = preprocess_text(text)
        tokens = tokenize_text(processed_text)
        time.sleep(0.3)
    
    # Step 2: Classification
    status_text.text("Step 2/2: Classifying content...")
    progress_bar.progress(75)
    
    with st.spinner("Running classification..."):
        prediction_result = predict_category(tokens)
        time.sleep(0.3)
    
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    # Display results
    display_classification_results(
        prediction_result,
        {'title': 'Direct Input', 'author': 'User', 'date': 'Now', 'url': None},
        text,
        processed_text,
        tokens
    )


def display_classification_results(prediction, metadata, raw_text, processed_text, tokens):
    """Display classification results in a structured layout"""
    
    st.success("Classification Complete")
    
    # Main prediction result
    st.markdown("### Classification Result")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Category",
            prediction['prediction'],
            help="Predicted news category"
        )
    
    with col2:
        st.metric(
            "Confidence",
            f"{prediction['confidence']:.1f}%",
            help="Model confidence score"
        )
    
    with col3:
        coverage_pct = prediction['vocab_coverage']
        st.metric(
            "Vocabulary Coverage",
            f"{coverage_pct:.1f}%",
            help="Percentage of tokens found in model vocabulary"
        )
    
    # Probability visualization
    st.markdown("### Probability Distribution")
    if prediction['probabilities']:
        fig_prob = plot_probability_distribution(prediction['probabilities'])
        st.plotly_chart(fig_prob, use_container_width=True)
    
    st.divider()
    
    # Detailed information tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Article Metadata",
        "Content Preview",
        "Preprocessing Results",
        "Token Analysis"
    ])
    
    with tab1:
        st.markdown("#### Article Information")
        st.write(f"**Title**: {metadata.get('title', 'N/A')}")
        st.write(f"**Author**: {metadata.get('author', 'N/A')}")
        st.write(f"**Published**: {metadata.get('date', 'N/A')}")
        if metadata.get('url'):
            st.write(f"**URL**: [{metadata['url']}]({metadata['url']})")
        
        # Text statistics
        stats = get_text_statistics(raw_text)
        st.markdown("#### Content Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Characters", f"{stats['char_count']:,}")
        col2.metric("Words", stats['word_count'])
        col3.metric("Sentences", stats['sentence_count'])
        col4.metric("Avg Word Length", f"{stats['avg_word_length']:.1f}")
    
    with tab2:
        st.markdown("#### Original Content")
        st.caption("First 1000 characters of extracted content")
        st.text_area(
            "",
            raw_text[:1000] + ("..." if len(raw_text) > 1000 else ""),
            height=300,
            disabled=True
        )
    
    with tab3:
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
        st.markdown("#### Token Statistics")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tokens", prediction['total_tokens'])
        col2.metric("Matched", prediction['matched_tokens'])
        col3.metric("Out of Vocabulary", prediction['oov_tokens'])
        
        # Token coverage visualization
        if prediction['matched_tokens'] > 0:
            fig_tokens = plot_token_statistics(
                prediction['matched_tokens'],
                prediction['oov_tokens']
            )
            st.plotly_chart(fig_tokens, use_container_width=True)
        
        # Sample tokens
        with st.expander("View Sample Tokens (first 50)"):
            sample_tokens = tokens[:50]
            st.write(", ".join(sample_tokens))


def main():
    """Main application entry point"""
    
    # Load custom CSS
    load_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.title("Detik News Classifier")
    st.caption("Automated classification of news articles using Machine Learning")
    
    st.markdown("""
    This application uses **Skip-Gram Word2Vec** for word embedding and 
    **Support Vector Machine (SVM)** for classification of news articles 
    into **Sport** or **Finance** categories.
    """)
    
    st.divider()
    
    # Input mode tabs
    tab1, tab2 = st.tabs(["URL Input", "Text Input"])
    
    with tab1:
        render_url_input_tab()
    
    with tab2:
        render_text_input_tab()


if __name__ == "__main__":
    main()
