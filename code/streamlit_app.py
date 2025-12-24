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
# --- 3. UI: SETUP PAGE ---
def show_setup_page():
    # Inject CSS
    st.markdown(SETUP_CSS, unsafe_allow_html=True)
    
    # Background Elements
    st.markdown("""
        <div class="stars"></div>
        <div class="aurora-secondary"></div>
        <div class="aurora-container"></div>
        <div class="beam"></div>
        <div class="beam beam-2"></div>
    """, unsafe_allow_html=True)
    
    # Centered Cointainer
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # Logo Section
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem; margin-top: 5vh;">
                <div>
                     <span style="font-family: 'Inter', sans-serif; font-weight: 800; font-size: 3.5rem; color: #ffffff; letter-spacing: -0.03em; text-shadow: 0 0 20px rgba(255,255,255,0.3);">CA</span>
                     <span style="font-family: 'Playfair Display', serif; font-style: italic; font-weight: 600; font-size: 3.5rem; color: #7dd3fc; margin-left: 0.2rem; position: relative;">
                        Scribe <span style="position: absolute; top: 0; right: -25px; font-size: 1.5rem; color: #38bdf8;">✦</span>
                     </span>
                </div>
                <div style="font-family: 'Inter', sans-serif; font-weight: 500; color: #94a3b8; letter-spacing: 0.05em; text-transform: uppercase; font-size: 0.75rem; margin-top: -0.5rem;">
                    AI-Powered Competency Mapper
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("setup_form"):
            # Gemini Input
            st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Connect Gemini</span>
                        <span style="font-size: 0.6rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 2px 6px; border-radius: 99px; border: 1px solid rgba(56, 189, 248, 0.2);">RECOMMENDED</span>
                    </div>
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" style="font-size: 0.7rem; color: #38bdf8; text-decoration: none; font-weight: 600;">Get Free Key ↗</a>
                </div>
            """, unsafe_allow_html=True)
            g_key = st.text_input("Gemini Key", type="password", placeholder="Paste Google API Key (AIza...)", label_visibility="collapsed")
            
            # Groq Input
            st.markdown("""
                <div style="margin-top: 15px; margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Or Groq</span>
                    <a href="https://console.groq.com/keys" target="_blank" style="font-size: 0.7rem; color: #94a3b8; text-decoration: none; font-weight: 600; hover:color: #38bdf8;">Get Free Key ↗</a>
                </div>
            """, unsafe_allow_html=True)
            q_key = st.text_input("Groq Key", type="password", placeholder="Paste Groq API Key (gsk_...)", label_visibility="collapsed")
            
            # GitHub Input
            st.markdown("""
                <div style="margin-top: 15px; margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Or GitHub Models</span>
                    <a href="https://github.com/marketplace/models" target="_blank" style="font-size: 0.7rem; color: #94a3b8; text-decoration: none; font-weight: 600;">Get Token ↗</a>
                </div>
            """, unsafe_allow_html=True)
            gh_key = st.text_input("GitHub Token", type="password", placeholder="Personal Access Token", label_visibility="collapsed")
            
            submitted = st.form_submit_button("Initialize CA Scribe →")
            
            if submitted:
                if not (g_key or q_key or gh_key):
                    st.error("Please enter at least one API key.")
                else:
                    if g_key: st.session_state["GOOGLE_API_KEY"] = g_key
                    if q_key: st.session_state["GROQ_API_KEY"] = q_key
                    if gh_key: st.session_state["GITHUB_TOKEN"] = gh_key
                    
                    # Persist to local secrets
                    try:
                        secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
                        os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
                        with open(secrets_path, "w") as f:
                            f.write(f'GOOGLE_API_KEY = "{g_key}"\n')
                            f.write(f'GROQ_API_KEY = "{q_key}"\n')
                            f.write(f'GITHUB_TOKEN = "{gh_key}"\n')
                    except Exception:
                        pass 
                        
                    st.rerun()

        # Helper / Documentation Expander
        with st.expander("📘 Need Help? View API Key Guide"):
            st.markdown("""
            ### 🔑 How to get your keys
            
            **✨ Google Gemini (Recommended)**
            1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
            2. Click **"Create API key"**.
            3. Copy the key starting with `AIza...`.
            
            **⚡ Groq (Fastest)**
            1. Go to [Groq Console](https://console.groq.com/keys).
            2. Click **"Create API Key"**.
            3. Copy the key starting with `gsk_...`.
            
            **🐙 GitHub Models (OpenAI)**
            1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens).
            2. Generate a **Personal Access Token (classic)**.
            3. No special scopes needed. Copy the token starting with `ghp_...`.
            """)

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
