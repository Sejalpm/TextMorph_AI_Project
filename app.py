import streamlit as st
import sys
from pathlib import Path

# Add src folder to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Now import from src folder
from src.combinedPipeline import SummarizationPipeline
import os
from dotenv import load_dotenv

# Load environment variables from src folder
env_path = src_path / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize session state for text area
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""
if 'output_type' not in st.session_state:
    st.session_state.output_type = ""

# Page config
st.set_page_config(
    page_title="Text Morph - AI Text Processing",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #ec4899;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Card styling */
    .stTextArea, .stButton, .stRadio, .stSelectSlider {
        background: white;
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #4a5568;
        font-size: 0.95rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Stats card */
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Output container */
    .output-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        min-height: 400px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# Function to save file to Downloads folder
def save_to_downloads(content, filename):
    """Save content to user's Downloads folder."""
    try:
        # Get Downloads folder path (works on Windows, Mac, Linux)
        downloads_path = Path.home() / "Downloads"
        
        # Create full file path
        file_path = downloads_path / filename
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path)
    except Exception as e:
        return None

# Get API key from environment
HF_API_KEY = os.getenv('HF_API_KEY')

if not HF_API_KEY:
    st.markdown("""
    <div class="info-box">
        <h2>⚠️ API Key Required</h2>
        <p>Please add your Hugging Face API key to the .env file in the src folder</p>
        <p>Get your key at: <a href="https://huggingface.co/settings/tokens" style="color: #ffd700;">https://huggingface.co/settings/tokens</a></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Initialize pipeline
@st.cache_resource
def load_pipeline():
    return SummarizationPipeline(HF_API_KEY)

try:
    pipeline = load_pipeline()
except Exception as e:
    st.error(f"❌ Failed to initialize pipeline: {str(e)}")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>🔮 Text Morph</h1>
    <p>AI-Powered Text Summarization & Paraphrasing Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    method = st.radio(
        "📊 Summarization Method",
        ["Extractive", "Abstractive"],
        help="Extractive: Selects key sentences from original text\nAbstractive: Generates new summary using AI"
    )
    
    length = st.select_slider(
        "📏 Summary Length",
        options=["Short", "Medium", "Long"],
        value="Medium",
        help="Choose the desired length of your summary"
    )
    
    st.markdown("---")
    
    # API Status
    st.markdown("### 🔐 API Status")
    if HF_API_KEY:
        st.success("✅ Connected to Hugging Face")
        st.caption("Inference API Active")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Models", "2+", delta="Active")
    with col_s2:
        st.metric("Speed", "Fast", delta="Cloud")
    
    st.markdown("---")
    
    # About section
    st.markdown("### 💡 About")
    st.markdown("""
    <div style='background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
        <p style='margin: 0; font-size: 0.9rem; color: #4a5568;'>
        <strong>Text Morph</strong> leverages state-of-the-art AI models via Hugging Face API to provide instant text summarization and paraphrasing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Creator info
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
        <p style='margin: 0; font-weight: 600;'>Created by Jeev</p>
        <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.9;'>Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
tab1, tab2, tab3 = st.tabs(["🚀 Process Text", "📚 Examples", "ℹ️ How It Works"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📝 Input")
        input_text = st.text_area(
            "Enter your text below",
            value=st.session_state.input_text,
            height=350,
            placeholder="Paste your text here for summarization or paraphrasing...\n\nExample: Long articles, research papers, essays, or any text content you want to process.",
            label_visibility="collapsed",
            key="text_input_area"
        )
        
        # Update session state
        st.session_state.input_text = input_text
        
        # Character count
        if input_text:
            char_count = len(input_text)
            word_count = len(input_text.split())
            st.caption(f"📊 Characters: {char_count} | Words: {word_count}")
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            summarize_btn = st.button("✨ Summarize", use_container_width=True, type="primary")
        
        with col_btn2:
            paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)
        
        with col_btn3:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)
            if clear_btn:
                st.session_state.input_text = ""
                st.rerun()
    
    with col2:
        st.markdown("### 📤 Output")
        
        if summarize_btn and input_text:
            with st.spinner("🔄 Processing with AI..."):
                try:
                    summary = pipeline.summarize(
                        input_text,
                        method=method.lower(),
                        length=length.lower()
                    )
                    
                    if summary.startswith("❌") or summary.startswith("⚠️"):
                        st.error(summary)
                    else:
                        st.session_state.output_text = summary
                        st.session_state.output_type = "summary"
                        
                        st.success("✅ Summary Generated Successfully!")
                        st.text_area("Your Summary", summary, height=300, label_visibility="collapsed", key="summary_output")
                        
                        # Stats
                        summary_words = len(summary.split())
                        original_words = len(input_text.split())
                        reduction = round((1 - summary_words/original_words) * 100, 1) if original_words > 0 else 0
                        
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        with col_stat1:
                            st.metric("Words", summary_words)
                        with col_stat2:
                            st.metric("Original", original_words)
                        with col_stat3:
                            st.metric("Reduced", f"{reduction}%")
                        
                        # Download button
                        if st.button("⬇️ Download Summary", use_container_width=True, key="download_summary_btn"):
                            filename = "text_morph_summary.txt"
                            file_path = save_to_downloads(summary, filename)
                            if file_path:
                                st.success(f"✅ File saved to: {file_path}")
                            else:
                                st.error("❌ Failed to save file")
                                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        elif paraphrase_btn and input_text:
            with st.spinner("🔄 Paraphrasing with AI..."):
                try:
                    paraphrased = pipeline.paraphrase(input_text)
                    
                    if paraphrased.startswith("❌") or paraphrased.startswith("⚠️"):
                        st.error(paraphrased)
                    else:
                        st.session_state.output_text = paraphrased
                        st.session_state.output_type = "paraphrase"
                        
                        st.success("✅ Text Paraphrased Successfully!")
                        st.text_area("Paraphrased Text", paraphrased, height=300, label_visibility="collapsed", key="paraphrase_output")
                        
                        # Stats
                        paraphrase_words = len(paraphrased.split())
                        original_words = len(input_text.split())
                        
                        col_stat1, col_stat2 = st.columns(2)
                        with col_stat1:
                            st.metric("Words", paraphrase_words)
                        with col_stat2:
                            st.metric("Original", original_words)
                        
                        # Download button
                        if st.button("⬇️ Download Paraphrase", use_container_width=True, key="download_paraphrase_btn"):
                            filename = "text_morph_paraphrase.txt"
                            file_path = save_to_downloads(paraphrased, filename)
                            if file_path:
                                st.success(f"✅ File saved to: {file_path}")
                            else:
                                st.error("❌ Failed to save file")
                                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Display previous output if exists
        elif st.session_state.output_text and not input_text:
            if st.session_state.output_type == "summary":
                st.success("✅ Summary (Previous Result)")
                st.text_area("Your Summary", st.session_state.output_text, height=300, label_visibility="collapsed", key="prev_summary")
            elif st.session_state.output_type == "paraphrase":
                st.success("✅ Paraphrase (Previous Result)")
                st.text_area("Paraphrased Text", st.session_state.output_text, height=300, label_visibility="collapsed", key="prev_paraphrase")
        
        elif not input_text and not st.session_state.output_text:
            st.markdown("""
            <div class='output-container'>
                <div style='text-align: center; padding-top: 60px;'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>📄</div>
                    <h3 style='color: #4a5568; margin-bottom: 0.5rem;'>Ready to Process</h3>
                    <p style='color: #718096;'>Enter text on the left and click a button to get started</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📚 Example Use Cases")
    
    col_ex1, col_ex2 = st.columns(2)
    
    with col_ex1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📰</div>
            <div class='feature-title'>News Articles</div>
            <div class='feature-desc'>Quickly summarize lengthy news articles to get key points and main ideas.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔬</div>
            <div class='feature-title'>Research Papers</div>
            <div class='feature-desc'>Extract essential findings and conclusions from academic papers.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📧</div>
            <div class='feature-title'>Email Content</div>
            <div class='feature-desc'>Paraphrase emails for different tones and contexts.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ex2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📖</div>
            <div class='feature-title'>Book Chapters</div>
            <div class='feature-desc'>Create concise summaries of book chapters for quick review.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>✍️</div>
            <div class='feature-title'>Essays & Reports</div>
            <div class='feature-desc'>Rephrase content to improve clarity and avoid redundancy.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💼</div>
            <div class='feature-title'>Business Documents</div>
            <div class='feature-desc'>Summarize reports, proposals, and meeting notes efficiently.</div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### ℹ️ How It Works")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        <div class='stats-card'>
            <h4 style='color: #667eea; margin-top: 0;'>🎯 Extractive Summarization</h4>
            <p style='color: #4a5568;'>
            Identifies and extracts the most important sentences from the original text. 
            This method preserves the exact wording while selecting key information.
            </p>
            <ul style='color: #4a5568; margin-bottom: 0;'>
                <li>Maintains original phrasing</li>
                <li>Fast processing</li>
                <li>High accuracy for factual content</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='stats-card'>
            <h4 style='color: #667eea; margin-top: 0;'>🔄 Paraphrasing</h4>
            <p style='color: #4a5568;'>
            Rewrites text in different words while preserving the original meaning. 
            Useful for avoiding plagiarism and improving clarity.
            </p>
            <ul style='color: #4a5568; margin-bottom: 0;'>
                <li>Natural language output</li>
                <li>Maintains context and meaning</li>
                <li>Multiple ways to express ideas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div class='stats-card'>
            <h4 style='color: #667eea; margin-top: 0;'>✨ Abstractive Summarization</h4>
            <p style='color: #4a5568;'>
            Uses AI to generate new sentences that capture the essence of the text. 
            Creates more human-like summaries with novel phrasing.
            </p>
            <ul style='color: #4a5568; margin-bottom: 0;'>
                <li>Human-like summaries</li>
                <li>Generates new sentences</li>
                <li>Better for creative content</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='stats-card'>
            <h4 style='color: #667eea; margin-top: 0;'>☁️ Cloud-Based Processing</h4>
            <p style='color: #4a5568;'>
            All processing happens via Hugging Face's Inference API. No local models 
            or downloads required - just instant results.
            </p>
            <ul style='color: #4a5568; margin-bottom: 0;'>
                <li>No installation needed</li>
                <li>Always up-to-date models</li>
                <li>Scalable infrastructure</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-top: 2rem;'>
    <p style='margin: 0; font-size: 1.1rem; font-weight: 600;'>Built with ❤️ using Streamlit</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;'>Powered by Hugging Face Inference API • No Local Models Required</p>
</div>
""", unsafe_allow_html=True)