import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.streamlit_styles import SETUP_CSS, MAIN_CSS
from ingestion.framework_loader import load_competency_framework
from analysis.mapper import map_activity_to_competency
from reporting.generator import generate_markdown_content

# --- 1. CONFIG & STATE ---
st.set_page_config(
    page_title="CA Scribe",
    page_icon="static/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "framework_data" not in st.session_state:
    st.session_state.framework_data = None
if "markdown_report" not in st.session_state:
    st.session_state.markdown_report = ""

# --- 2. AUTHENTICATION ---
def get_api_keys():
    """Checks for API keys in Streamlit secrets or OS environ."""
    # Priority: Session > Secrets > OS > Input
    keys = {
        "GOOGLE_API_KEY": st.session_state.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY"),
        "GROQ_API_KEY": st.session_state.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY"),
        "GITHUB_TOKEN": st.session_state.get("GITHUB_TOKEN") or st.secrets.get("GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN"),
    }
    # Filter out empty strings
    return {k: v for k, v in keys.items() if v}

keys = get_api_keys()
has_access = bool(keys)

# Propagate to OS for mapper.py
for k, v in keys.items():
    os.environ[k] = v

# --- 3. UI: SETUP PAGE ---
def show_setup_page():
    st.markdown(SETUP_CSS, unsafe_allow_html=True)
    st.markdown('<div class="gradient-bg"></div>', unsafe_allow_html=True)
    
    # Centered Cointainer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)
        st.markdown("""
            <h1 style='text-align: center; color: #1e3a8a; margin-bottom: 0;'>Welcome to CA Scribe</h1>
            <p style='text-align: center; color: #64748b; margin-top: 0;'>AI-Powered Competency Documentation Assistant</p>
            <hr style='margin: 20px 0; border: 0; border-top: 1px solid #e2e8f0;'>
        """, unsafe_allow_html=True)

        st.info("💡 Connect your AI brains. Pick a favorite, or go wild and connect all 3!")

        with st.form("setup_form"):
            st.markdown("### ✨ Google Gemini (Recommended)")
            g_key = st.text_input("Gemini API Key", type="password", help="Starts with AIza...")
            
            st.markdown("### ⚡ Groq (Llama 3)")
            q_key = st.text_input("Groq API Key", type="password", help="Starts with gsk_...")
            
            st.markdown("### 🐙 GitHub Models (OpenAI)")
            gh_key = st.text_input("GitHub Token", type="password", help="Personal Access Token")
            
            submitted = st.form_submit_button("Connect & Launch 🚀")
            
            if submitted:
                if not (g_key or q_key or gh_key):
                    st.error("Please enter at least one API key.")
                else:
                    if g_key: st.session_state["GOOGLE_API_KEY"] = g_key
                    if q_key: st.session_state["GROQ_API_KEY"] = q_key
                    if gh_key: st.session_state["GITHUB_TOKEN"] = gh_key
                    
                    # Persist to local secrets if possible (Local Dev Only)
                    # We skip writing to file in Streamlit Cloud environment to avoid errors
                    try:
                        secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
                        os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
                        with open(secrets_path, "w") as f:
                            f.write(f'GOOGLE_API_KEY = "{g_key}"\n')
                            f.write(f'GROQ_API_KEY = "{q_key}"\n')
                            f.write(f'GITHUB_TOKEN = "{gh_key}"\n')
                    except Exception:
                        pass # Ignore file write errors on cloud
                        
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. UI: MAIN PAGE ---
def show_main_page():
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="fluid-bg"></div>', unsafe_allow_html=True)
    
    # Lazy Load Framework
    if st.session_state.framework_data is None:
        with st.spinner("Loading Competency Framework..."):
            st.session_state.framework_data = load_competency_framework()

    # Header
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 1rem 0;">
            <div>
                <span class="logo-main">CA</span>
                <span class="logo-scribe">Scribe <span style="font-size: 1rem; color: #0ea5e9; vertical-align: top;">✦</span></span>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #0ea5e9; font-family: monospace;">STATUS: CONNECTED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, spacer, col2 = st.columns([40, 5, 55])
    
    with col1:
        st.markdown("### Activity Input")
        activity = st.text_area(
            "Describe your activity...", 
            height=300, 
            placeholder="e.g. 'I managed the inventory count for the client...'"
        )
        
        provider = st.selectbox("AI Provider", ["gemini", "groq", "github_mini", "github_4o"])
        
        if st.button("Generate Analysis 🚀", use_container_width=True):
            if not activity.strip():
                st.warning("Please describe your activity first.")
            else:
                with st.spinner("Analyzing with AI..."):
                    try:
                        # Map
                        results = map_activity_to_competency(
                            activity, 
                            st.session_state.framework_data, 
                            provider=provider
                        )
                        # Report
                        st.session_state.markdown_report = generate_markdown_content(results)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

    with col2:
        st.markdown("### Analysis Report")
        if st.session_state.markdown_report:
            st.markdown(st.session_state.markdown_report)
        else:
            st.info("Detailed mapping will appear here after analysis.")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #64748b; font-size: 0.8rem;">
            Made by <strong>Adhir Singh</strong>
        </div>
    """, unsafe_allow_html=True)

# --- 5. APP CONTROLLER ---
if has_access:
    show_main_page()
else:
    show_setup_page()
