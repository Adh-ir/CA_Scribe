import streamlit as st
import os
import sys
import time

# Deploy Trigger: V5.1 - Session-only persistence (localStorage blocked on Streamlit Cloud)
import streamlit.components.v1 as components
from PIL import Image

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.streamlit_styles import (
    SETUP_CSS, 
    MAIN_CSS, 
    FONT_LINKS, 
    GLOBAL_HACKS_CSS, 
    FOCUS_FIX_JS,
    LOADING_MODE_CSS
)
from utils.html_templates import LOADING_HTML
from ingestion.framework_loader import load_competency_framework
from analysis.mapper import map_activity_to_competency
from reporting.generator import generate_markdown_content

# --- 1. CONFIG & STATE ---
try:
    favicon = Image.open(os.path.join(os.path.dirname(__file__), "static", "favicon.png"))
except Exception:
    favicon = "static/favicon.png" # Fallback

st.set_page_config(
    page_title="CA Scribe",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INITIALIZE SESSION STATE ---
if "framework_data" not in st.session_state:
    st.session_state.framework_data = None
    
if "markdown_report" not in st.session_state:
    st.session_state.markdown_report = ""

if "keys_loaded_from_storage" not in st.session_state:
    st.session_state.keys_loaded_from_storage = False

# --- API KEY PERSISTENCE ---
# Note: Browser localStorage is not supported on Streamlit Cloud due to iframe
# sandbox restrictions. Keys persist in session state during the browser session.
# For production, use st.secrets for server-side key management.

# Force global styles immediately
st.markdown(GLOBAL_HACKS_CSS, unsafe_allow_html=True)
st.markdown(FOCUS_FIX_JS, unsafe_allow_html=True)

# --- LOADING ANIMATION (Local & Cloud Compatible) ---
if "loading_complete" not in st.session_state:
    # Check if we should skip loading (e.g. for guide page)
    should_skip = False
    try:
        if st.query_params.get("page") == "guide":
            should_skip = True
    except:
        pass
    st.session_state.loading_complete = should_skip




if not st.session_state.loading_complete:
    # Fullscreen iframe hack & PADDING OVERRIDE
    st.markdown(LOADING_MODE_CSS, unsafe_allow_html=True)
    
    # Render Animation
    components.html(LOADING_HTML, height=800)
    
    # --- BACKGROUND LOADING START ---
    t_start = time.time()
    
    # Perform expensive loading HERE while animation is running on frontend
    if st.session_state.framework_data is None:
        try:
            st.session_state.framework_data = load_competency_framework()
        except Exception as e:
            print(f"Background Loading Failed: {e}")
            # Ensure we don't crash, let the app proceed (it might handle None later or retry)
            st.session_state.framework_data = None
        
    # Wait remaining time (Total 8.5s)
    elapsed = time.time() - t_start
    remaining = 8.5 - elapsed
    if remaining > 0:
        time.sleep(remaining)
    # --- BACKGROUND LOADING END ---
    
    st.session_state.loading_complete = True
    st.rerun()

# --- APP START ---

# --- 2. AUTHENTICATION ---
def get_api_keys():
    """Gets API keys from session state ONLY (user must enter their own keys).
    
    SECURITY: We intentionally DO NOT read from st.secrets or os.environ on Streamlit Cloud
    to prevent the app owner's API keys from being used by all visitors.
    Each user must provide their own API keys.
    """
    keys = {
        "GOOGLE_API_KEY": st.session_state.get("GOOGLE_API_KEY"),
        "GROQ_API_KEY": st.session_state.get("GROQ_API_KEY"),
        "GITHUB_TOKEN": st.session_state.get("GITHUB_TOKEN"),
    }
    # Filter out None and empty strings
    return {k: v for k, v in keys.items() if v}

keys = get_api_keys()
has_access = bool(keys)

# Propagate to OS for mapper.py
for k, v in keys.items():
    os.environ[k] = v

# --- 3. UI: SETUP PAGE ---
def show_setup_page():
    # Inject CSS
    st.markdown(FONT_LINKS, unsafe_allow_html=True)
    st.markdown(SETUP_CSS, unsafe_allow_html=True)
    
    # Particle Wave Background Elements
    st.markdown("""
        <div class="fluid-bg">
            <div class="dot-grid"></div>
            <div class="wave-layer"></div>
            <div class="wave-layer-2"></div>
            <div class="fluid-shape shape-1"></div>
            <div class="fluid-shape shape-2"></div>
            <div class="fluid-shape shape-3"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Centered Container
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # CSS-based star using ::after pseudo-element (bypasses HTML sanitization)
        st.markdown("""
            <style>
            .logo-star-setup::after {
                content: '';
                position: absolute;
                top: -5px;
                right: -30px;
                width: 28px;
                height: 28px;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cg transform='rotate(28 12 12)'%3E%3Cpath d='M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z' fill='%230ea5e9'/%3E%3C/g%3E%3C/svg%3E");
                background-size: contain;
                background-repeat: no-repeat;
            }
            </style>
            <div style="text-align: center; margin-bottom: 2.5rem; margin-top: 2vh;">
                <div style="display: flex; align-items: baseline; justify-content: center; gap: 0.25rem; margin-bottom: 0.5rem;">
                     <span class="logo-main" style="font-size: 4rem;">CA</span>
                     <span class="logo-scribe logo-star-setup" style="font-size: 4rem; position: relative;">
                        Scribe
                     </span>
                </div>
                <div style="font-family: 'Inter', sans-serif; font-weight: 600; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; font-size: 0.85rem; margin-top: -0.25rem;">
                    AI-Powered Competency Mapper
                </div>
                <div style="font-family: 'Inter', sans-serif; font-weight: 500; color: #1e3a8a; font-size: 0.95rem; margin-top: 2rem; line-height: 1.6; max-width: 400px; margin-left: auto; margin-right: auto; text-shadow: none;">
                    Please retrieve and install one or all of the API keys below to get access to each model
                </div>
                <div style="background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 8px; padding: 10px 16px; margin-top: 1.5rem; max-width: 400px; margin-left: auto; margin-right: auto;">
                    <p style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #92400e; margin: 0; line-height: 1.4;">
                        ⚠️ <strong>Note:</strong> Please do not input confidential or sensitive information into this application.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("setup_form"):
            # Gemini Input Section
            st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; margin-top: 10px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">✨ Google Gemini</span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: #0ea5e9; background: rgba(14, 165, 233, 0.1); padding: 3px 8px; border-radius: 99px; border: 1px solid rgba(14, 165, 233, 0.25);">RECOMMENDED</span>
                    </div>
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" style="font-size: 0.75rem; color: #0ea5e9; text-decoration: none; font-weight: 600; transition: color 0.2s;">Get Free Key ↗</a>
                </div>
            """, unsafe_allow_html=True)
            g_key = st.text_input("Gemini Key", type="password", placeholder="Paste Google API Key (AIza...)", label_visibility="collapsed")
            
            # Groq Input Section
            st.markdown("""
                <div style="margin-top: 20px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">⚡ Groq</span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: #f97316; background: rgba(249, 115, 22, 0.1); padding: 3px 8px; border-radius: 99px; border: 1px solid rgba(249, 115, 22, 0.25);">FASTEST</span>
                    </div>
                    <a href="https://console.groq.com/keys" target="_blank" style="font-size: 0.75rem; color: #0ea5e9; text-decoration: none; font-weight: 600; transition: color 0.2s;">Get Free Key ↗</a>
                </div>
            """, unsafe_allow_html=True)
            q_key = st.text_input("Groq Key", type="password", placeholder="Paste Groq API Key (gsk_...)", label_visibility="collapsed")
            
            # GitHub Input Section
            st.markdown("""
                <div style="margin-top: 20px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">🐙 GitHub Models</span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: #64748b; background: rgba(100, 116, 139, 0.1); padding: 3px 8px; border-radius: 99px; border: 1px solid rgba(100, 116, 139, 0.25);">OPENAI GPT-4o</span>
                    </div>
                    <a href="https://github.com/settings/tokens" target="_blank" style="font-size: 0.75rem; color: #0ea5e9; text-decoration: none; font-weight: 600; transition: color 0.2s;">Get Token ↗</a>
                </div>
            """, unsafe_allow_html=True)
            gh_key = st.text_input("GitHub Token", type="password", placeholder="Personal Access Token (ghp_...)", label_visibility="collapsed")
            
            # Info note
            st.markdown("""
                <div style="text-align: center; margin: 0.5rem 0 0.5rem 0;">
                    <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 500;">
                        Keys are stored in your browser for 7 days
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Initialize CA Scribe →", use_container_width=True)
            
            if submitted:
                if not (g_key or q_key or gh_key):
                    st.error("⚠️ Please enter at least one API key to continue.")
                else:
                    if g_key: st.session_state["GOOGLE_API_KEY"] = g_key
                    if q_key: st.session_state["GROQ_API_KEY"] = q_key
                    if gh_key: st.session_state["GITHUB_TOKEN"] = gh_key
                    st.rerun()

            # Helper Link
            st.markdown("""
                <div style="text-align: center; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                    <a href="/?page=guide" target="_blank" style="color: #64748b; font-size: 0.8rem; text-decoration: none; font-weight: 500; transition: color 0.2s;">
                        Need help getting keys? View Full Guide ↗
                    </a>
                </div>
            """, unsafe_allow_html=True)




# --- 3.5. UI: SETTINGS PAGE ---
def render_settings_page():
    st.markdown(FONT_LINKS, unsafe_allow_html=True)
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="fluid-bg"><div class="fluid-shape shape-1"></div><div class="fluid-shape shape-2"></div><div class="fluid-shape shape-3"></div></div>', unsafe_allow_html=True)

    # Inject CSS to style the form itself as the Glass Card
    st.markdown("""
        <style>
        /* Target the specific form used for settings */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.95); 
            backdrop-filter: blur(20px); 
            padding: 3rem 3rem 1.2rem 3rem; 
            border-radius: 24px; 
            box-shadow: 0 20px 40px -10px rgba(14, 165, 233, 0.15); 
            border: 0.5px solid rgba(200, 230, 255, 0.5); 
            max-width: 500px; 
            margin: 0 auto;
            margin-top: calc(5vh - 50px);
            text-align: center;
        }
        /* Ensure buttons don't wrap */
        [data-testid="stForm"] button {
            white-space: nowrap !important;
        }
        /* Make button columns wider */
        [data-testid="stForm"] [data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.form("settings_form"):
        # 1. Logo & Header (Inside the form now)
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="display: flex; justify-content: center; align-items: baseline; gap: 0.25rem; margin-bottom: 0.5rem;">
                     <span class="logo-main" style="font-size: 2.4rem;">CA</span>
                     <span class="logo-scribe" style="font-size: 2.4rem; position: relative;">
                        Scribe 
                        <span style="position: absolute; top: -5px; right: -26px;"><img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgdHJhbnNmb3JtPSJyb3RhdGUoMjggMTIgMTIpIj4KPHBhdGggZD0iTTEyIDBMMTQuNTkgOS40MUwyNCAxMkwxNC41OSAxNC41OUwxMiAyNEw5LjQxIDE0LjU5TDAgMTJMOS40MSA5LjQxTDEyIDBaIiBmaWxsPSIjMGVhNWU5Ii8+CjwvZz4KPC9zdmc+" style="width: 24px; height: 24px;" alt="star"></span>
                     </span>
                </div>
                <h2 style="font-family: 'Inter', sans-serif; color: #1e293b; font-size: 1.25rem;">API Configuration</h2>
                <p style="color: #64748b; font-size: 0.9rem;">Update your API keys below</p>
            </div>
        """, unsafe_allow_html=True)

        # Gemini Input Section
        st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; margin-top: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">✨ Google Gemini</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: #0ea5e9; background: rgba(14, 165, 233, 0.1); padding: 3px 8px; border-radius: 99px; border: 1px solid rgba(14, 165, 233, 0.25);">RECOMMENDED</span>
                </div>
                <a href="https://aistudio.google.com/app/apikey" target="_blank" style="font-size: 0.75rem; color: #0ea5e9; text-decoration: none; font-weight: 600; transition: color 0.2s;">Get Free Key ↗</a>
            </div>
        """, unsafe_allow_html=True)
        g_key_val = st.session_state.get("GOOGLE_API_KEY", "")
        g_key = st.text_input("Gemini Key", value=g_key_val, type="password", placeholder="Paste Google API Key (AIza...)", label_visibility="collapsed")
        
        # Groq Input Section
        st.markdown("""
            <div style="margin-top: 20px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">⚡ Groq</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: #f97316; background: rgba(249, 115, 22, 0.1); padding: 3px 8px; border-radius: 99px; border: 1px solid rgba(249, 115, 22, 0.25);">FASTEST</span>
                </div>
                <a href="https://console.groq.com/keys" target="_blank" style="font-size: 0.75rem; color: #0ea5e9; text-decoration: none; font-weight: 600; transition: color 0.2s;">Get Free Key ↗</a>
            </div>
        """, unsafe_allow_html=True)
        q_key_val = st.session_state.get("GROQ_API_KEY", "")
        q_key = st.text_input("Groq Key", value=q_key_val, type="password", placeholder="Paste Groq API Key (gsk_...)", label_visibility="collapsed")
        
        # GitHub Input Section
        st.markdown("""
            <div style="margin-top: 20px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">🐙 GitHub Models</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: #64748b; background: rgba(100, 116, 139, 0.1); padding: 3px 8px; border-radius: 99px; border: 1px solid rgba(100, 116, 139, 0.25);">OPENAI GPT-4o</span>
                </div>
                <a href="https://github.com/settings/tokens" target="_blank" style="font-size: 0.75rem; color: #0ea5e9; text-decoration: none; font-weight: 600; transition: color 0.2s;">Get Token ↗</a>
            </div>
        """, unsafe_allow_html=True)
        gh_key_val = st.session_state.get("GITHUB_TOKEN", "")
        gh_key = st.text_input("GitHub Token", value=gh_key_val, type="password", placeholder="Personal Access Token (ghp_...)", label_visibility="collapsed")
        
        # Add spacing before buttons (increased to 60px)
        st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            if st.form_submit_button("Cancel", type="secondary", use_container_width=True):
                st.session_state.view_mode = "main"
                try: st.query_params.clear() 
                except: pass
                st.rerun()
        with col2:
            if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                if g_key: st.session_state["GOOGLE_API_KEY"] = g_key
                if q_key: st.session_state["GROQ_API_KEY"] = q_key
                if gh_key: st.session_state["GITHUB_TOKEN"] = gh_key
                
                st.session_state.view_mode = "main"
                try: st.query_params.clear() 
                except: pass
                st.rerun()

        # Helper Link
        st.markdown("""
            <div style="text-align: center; margin-top: 1rem; margin-bottom: 0.5rem;">
                <a href="/?page=guide" target="_blank" style="color: #64748b; font-size: 0.8rem; text-decoration: none; font-weight: 500; transition: color 0.2s;">
                    Need help getting keys? View Full Guide ↗
                </a>
            </div>
        """, unsafe_allow_html=True)


# --- 4. UI: MAIN PAGE ---
def show_main_page():

    # Inject Styles & Background
    st.markdown(FONT_LINKS, unsafe_allow_html=True)
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="fluid-bg"><div class="fluid-shape shape-1"></div><div class="fluid-shape shape-2"></div><div class="fluid-shape shape-3"></div></div>', unsafe_allow_html=True)
    
    # Lazy Load Framework (Fallback if background loading failed)
    if st.session_state.framework_data is None:
        with st.spinner("Finalizing setup..."):
            try:
                st.session_state.framework_data = load_competency_framework()
            except Exception:
                st.error("Failed to load competency framework. Please check logs.")
    
    # --- HEADER (Outside Card) ---
    st.markdown("""
        <style>
        /* Stronger Glo Effect */
        a.settings-link:hover {
            box-shadow: 0 0 25px rgba(14, 165, 233, 0.6) !important;
            border-color: #0ea5e9 !important;
            background: rgba(255, 255, 255, 1.0) !important;
            transform: translateY(-1px);
        }
        </style>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 1rem; margin-bottom: 2rem;">
            <div>
                <div style="display: flex; align-items: baseline; gap: 0.25rem;">
                    <span class="logo-main" style="font-size: 2.75rem;">CA</span>
                    <span class="logo-scribe" style="font-size: 2.75rem; position: relative;">
                        Scribe 
                        <span style="position: absolute; top: -5px; right: -28px;">
                            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgdHJhbnNmb3JtPSJyb3RhdGUoMjggMTIgMTIpIj4KPHBhdGggZD0iTTEyIDBMMTQuNTkgOS40MUwyNCAxMkwxNC41OSAxNC41OUwxMiAyNEw5LjQxIDE0LjU5TDAgMTJMOS40MSA5LjQxTDEyIDBaIiBmaWxsPSIjMGVhNWU5Ii8+CjwvZz4KPC9zdmc+" style="width: 22px; height: 22px;" alt="star">
                        </span>
                    </span>
                </div>
                <div style="font-size: 1rem; color: #64748b; font-weight: 500; margin-top: -10px; letter-spacing: 0.025em; padding-left: 0.25rem;">AI-Powered Competency Mapper</div>
            </div>
            <div>
                <a href="/?page=settings" target="_blank" class="settings-link" style="
                    background: rgba(255, 255, 255, 0.8); 
                    backdrop-filter: blur(10px);
                    border: 1px solid #7dd3fc; 
                    border-radius: 8px; 
                    padding: 8px 16px; 
                    color: #0369a1; 
                    font-weight: 600; 
                    font-size: 0.8rem; 
                    cursor: pointer; 
                    display: flex; 
                    align-items: center; 
                    gap: 6px;
                    text-decoration: none;
                    transition: all 0.3s ease;
                ">
                    <span style="display: inline-block; width: 8px; height: 8px; background: #4ade80; border-radius: 50%;"></span>
                    Settings
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Main Content (The Glass Card) ---
    # 2. COLUMNS (Inputs & Report)
    main_col1, main_col2 = st.columns([4, 6], gap="large")

    # --- LEFT PANEL (Input) ---
    with main_col1:
        # Inject CSS to make Streamlit secondary button look like custom design
        # Force redeploy - v2
        st.markdown("""
            <style>
            /* Force secondary button to match custom design */
            div.stButton > button[kind="secondary"] {
                width: 100% !important;
                padding: 0.85rem 1.5rem !important;
                background: #ffffff !important;
                border: 1px solid #e0f2fe !important;
                border-radius: 0.75rem !important;
                color: #0369a1 !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                text-align: left !important;
                font-family: 'Inter', sans-serif !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                justify-content: flex-start !important;
            }
            div.stButton > button[kind="secondary"]:hover {
                background: #f0f9ff !important;
                border-color: #7dd3fc !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.15) !important;
                color: #0284c7 !important;
            }
            div.stButton > button[kind="secondary"]:active {
                transform: translateY(0) !important;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.05) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Button to pre-fill competency template
        if st.button("✨ Target Competency                                                              +", use_container_width=True, type="secondary", help="Autofill template below"):
            st.session_state.activity_input = "COMPETENCY: [Insert Name] EVIDENCE: "
        
        activity_val = st.session_state.get("activity_input", "")
        activity = st.text_area(
            "Activity Description", 
            value=activity_val,
            height=350, 
            placeholder="Describe your activity... e.g. 'I managed the inventory count for the client...'",
            label_visibility="visible"
        )
        # Update state on change
        st.session_state.activity_input = activity 
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        provider = st.selectbox(
            "AI Model", 
            ["gemini", "groq", "github_mini", "github_4o"], 
            format_func=lambda x: {
                "gemini": "✨ Gemini 2.0 Flash Exp",
                "groq": "⚡ Groq (Llama 3)",
                "github_mini": "🐙 GitHub - GPT-4o Mini",
                "github_4o": "🐙 GitHub - GPT-4o"
            }.get(x, x)
        )
        
        # --- Generate Analysis Button ---
        # Store provider in session state
        st.session_state.selected_provider = provider
        
        if st.button("Generate Analysis 🚀", use_container_width=True, type="primary"):
            # Get current values from session state
            current_activity = st.session_state.get("activity_input", "")
            
            # Check if activity is empty or just the template
            is_empty = not current_activity.strip()
            is_template_only = current_activity.strip() == "COMPETENCY: [Insert Name] EVIDENCE:"
            has_no_evidence = "EVIDENCE:" in current_activity and current_activity.split("EVIDENCE:", 1)[1].strip() == ""
            
            if is_empty or is_template_only or has_no_evidence:
                st.warning("Please describe your activity first. Fill in the template with your actual work details.")
            else:
                # Set flag to trigger analysis in right panel
                st.session_state.run_analysis = True
                st.rerun()

    # --- RIGHT PANEL (Report) ---
    with main_col2:
        # Static Header (Only show if no report generated AND not currently running)
        if not st.session_state.get("markdown_report") and not st.session_state.get("run_analysis", False):
            st.markdown(f'<h3 style="color: #1e3a8a; font-family: \'Inter\', sans-serif; margin-top: 0; margin-bottom: 1rem;">Analysis Report</h3>', unsafe_allow_html=True)
        
        # Create a SINGLE placeholder for all content (loading, report, or empty state)
        content_area = st.empty()
        
        # Check if analysis was triggered
        if st.session_state.get("run_analysis", False):
            
            # Wrapper for the animation to allow mode switching
            def get_loading_html(mode="ENTRY"):
                # mode: "ENTRY" (Assemble + Breathe loop) or "EXIT" (Instant Explode)
                
                # JS Logic Configuration
                js_config = f"""
                    const MODE = "{mode}"; 
                """
                
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@800&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
                    <style>
                        body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
                        @keyframes fadeOut {{
                            0% {{ opacity: 1; }}
                            70% {{ opacity: 1; }}
                            100% {{ opacity: 0; }}
                        }}
                        .loading-container {{
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            height: 350px;
                            background: transparent;
                            position: relative;
                            { 'animation: fadeOut 1.2s ease-out forwards;' if mode == 'EXIT' else '' }
                        }}
                        #text-canvas {{
                            width: 800px;
                            height: 200px;
                            z-index: 2;
                        }}
                        .loading-text {{
                            margin-top: 10px;
                            font-weight: 600;
                            font-size: 1rem;
                            color: #0369a1;
                            font-family: 'Inter', sans-serif;
                            z-index: 2;
                            opacity: 1;
                        }}
                        .loading-subtext {{
                            margin-top: 4px;
                            font-size: 0.85rem;
                            color: #94a3b8;
                            font-family: 'Inter', sans-serif;
                            z-index: 2;
                            opacity: 1;
                        }}
                    </style>
                </head>
                <body>
                    <div class="loading-container">
                        <canvas id="text-canvas" width="800" height="200"></canvas>
                        <p class="loading-text">Analyzing with AI...</p>
                        <p class="loading-subtext">Mapping competencies</p>
                    </div>
                    <script>
                        {js_config}
                        
                        (function() {{
                            const canvas = document.getElementById('text-canvas');
                            if (!canvas) return;
                            
                            const ctx = canvas.getContext('2d');
                            const dpr = window.devicePixelRatio || 1;
                            
                            canvas.width = 800 * dpr;
                            canvas.height = 200 * dpr;
                            ctx.scale(dpr, dpr);
                            
                            canvas.style.width = '800px';
                            canvas.style.height = '200px';
                            
                            const w = 800; 
                            const h = 200; 
                            
                            const colors = {{ 
                                ca: '#003B5C', 
                                scribe: '#005F88', 
                                star: '#0ea5e9' 
                            }};

                            // Path: M12 0L14.59 9.41L24 12... (Native 24x24)
                            function drawTargetStar(ctx, x, y, size) {{
                                ctx.save();
                                ctx.translate(x, y);
                                
                                // ROTATION: 28 degrees = ~0.488 radians
                                ctx.rotate(28 * Math.PI / 180);
                                
                                const scale = size / 24;
                                ctx.scale(scale, scale);
                                ctx.translate(-12, -12);
                                
                                ctx.beginPath();
                                ctx.moveTo(12, 0);
                                ctx.lineTo(14.59, 9.41);
                                ctx.lineTo(24, 12);
                                ctx.lineTo(14.59, 14.59);
                                ctx.lineTo(12, 24);
                                ctx.lineTo(9.41, 14.59);
                                ctx.lineTo(0, 12);
                                ctx.lineTo(9.41, 9.41);
                                ctx.lineTo(12, 0);
                                ctx.closePath();
                                ctx.fillStyle = colors.star;
                                ctx.fill();
                                ctx.restore();
                            }}

                            function createParticleGroups() {{
                                const tempCanvas = document.createElement('canvas');
                                tempCanvas.width = w;
                                tempCanvas.height = h;
                                const tempCtx = tempCanvas.getContext('2d');
                                
                                // Layout
                                const fontSize = 70;
                                const baseY = h / 2 + fontSize / 3;
                                tempCtx.font = `800 ${{fontSize}}px "Inter", sans-serif`;
                                const caWidth = tempCtx.measureText('CA').width;
                                tempCtx.font = `italic 600 ${{fontSize}}px "Playfair Display", serif`;
                                const scribeWidth = tempCtx.measureText('Scribe').width;
                                
                                const spacing = 12;
                                const starSize = 40; 
                                
                                const totalWidth = caWidth + spacing + scribeWidth + spacing + starSize;
                                const startX = (w - totalWidth) / 2;
                                
                                // 1. Draw CA
                                tempCtx.clearRect(0,0,w,h);
                                tempCtx.font = `800 ${{fontSize}}px "Inter", sans-serif`;
                                tempCtx.fillStyle = '#FFFFFF'; 
                                tempCtx.fillText('CA', startX, baseY);
                                const caData = tempCtx.getImageData(0,0,w,h).data;
                                
                                // 2. Draw Scribe
                                tempCtx.clearRect(0,0,w,h);
                                tempCtx.font = `italic 600 ${{fontSize}}px "Playfair Display", serif`;
                                tempCtx.fillStyle = '#FFFFFF';
                                tempCtx.fillText('Scribe', startX + caWidth + spacing, baseY);
                                const scribeData = tempCtx.getImageData(0,0,w,h).data;
                                
                                // 3. Draw Star (ROTATED)
                                tempCtx.clearRect(0,0,w,h);
                                const starCenterX = startX + caWidth + spacing + scribeWidth + spacing + (starSize/2);
                                const starCenterY = baseY - (fontSize / 4); 
                                tempCtx.fillStyle = '#FFFFFF';
                                drawTargetStar(tempCtx, starCenterX, starCenterY, starSize);
                                const starData = tempCtx.getImageData(0,0,w,h).data;
                                
                                // Generate Particles
                                const groupCA = [];
                                const groupScribe = [];
                                const groupStar = [];
                                
                                const step = 2; 
                                
                                for (let y = 0; y < h; y += step) {{
                                    for (let x = 0; x < w; x += step) {{
                                        const i = (y * w + x) * 4;
                                        
                                        if (starData[i+3] > 128) {{
                                             groupStar.push({{
                                                ox: x, oy: y,
                                                x: (MODE === "EXIT") ? x : Math.random() * w,
                                                y: (MODE === "EXIT") ? y : Math.random() * h,
                                                size: 1.5, 
                                                phase: Math.random() * Math.PI * 2,
                                                vx: (Math.random() - 0.5) * 4,
                                                vy: (Math.random() - 0.5) * 4    
                                            }});
                                        }}
                                        else if (scribeData[i+3] > 128) {{
                                            groupScribe.push({{
                                                ox: x, oy: y,
                                                x: (MODE === "EXIT") ? x : Math.random() * w,
                                                y: (MODE === "EXIT") ? y : Math.random() * h,
                                                size: 1.5,
                                                phase: Math.random() * Math.PI * 2,
                                                vx: (Math.random() - 0.5) * 4,
                                                vy: (Math.random() - 0.5) * 4    
                                            }});
                                        }}
                                        else if (caData[i+3] > 128) {{
                                            groupCA.push({{
                                                ox: x, oy: y,
                                                x: (MODE === "EXIT") ? x : Math.random() * w,
                                                y: (MODE === "EXIT") ? y : Math.random() * h,
                                                size: 1.5,
                                                phase: Math.random() * Math.PI * 2,
                                                vx: (Math.random() - 0.5) * 4,
                                                vy: (Math.random() - 0.5) * 4    
                                            }});
                                        }}
                                    }}
                                }}
                                return {{ groupCA, groupScribe, groupStar }};
                            }}
                            
                            // Animation Loop
                            document.fonts.ready.then(() => {{
                                const groups = createParticleGroups();
                                
                                let time = 0;
                                const cx = w / 2;
                                const cy = h / 2;
                                let phase = "ASSEMBLE"; 
                                if (MODE === "EXIT") phase = "BREATHE"; 
                                
                                function updateAndDrawGroup(particles, colorStr) {{
                                    ctx.fillStyle = colorStr;
                                    ctx.beginPath();
                                    
                                    const breatheScale = 1 + Math.sin(time * 2) * 0.02;
                                    
                                    for (let i = 0; i < particles.length; i++) {{
                                        const p = particles[i];
                                        
                                        // Update Logic
                                        if (phase === "ASSEMBLE") {{
                                            p.x += (p.ox - p.x) * 0.08;
                                            p.y += (p.oy - p.y) * 0.08;
                                        }} else if (phase === "BREATHE") {{
                                            const dx = p.ox - cx;
                                            const dy = p.oy - cy;
                                            const bx = cx + dx * breatheScale;
                                            const by = cy + dy * breatheScale;
                                            const driftX = Math.sin(time + p.phase) * 1.5;
                                            const driftY = Math.cos(time + p.phase * 0.7) * 1.5;
                                            p.x += (bx + driftX - p.x) * 0.1;
                                            p.y += (by + driftY - p.y) * 0.1;
                                        }} else if (phase === "EXPLODE") {{
                                            p.x += p.vx;
                                            p.y += p.vy;
                                            p.vx *= 1.05; 
                                            p.vy *= 1.05;
                                        }}
                                        
                                        // Render
                                        ctx.rect(p.x, p.y, p.size, p.size);
                                    }}
                                    ctx.fill();
                                }}

                                function animate() {{
                                    ctx.clearRect(0, 0, w, h);
                                    time += 0.02;
                                    
                                    if (MODE === "ENTRY") {{
                                        if (time < 2.5) phase = "ASSEMBLE";
                                        else phase = "BREATHE";
                                    }}
                                    else if (MODE === "EXIT") {{
                                        if (time < 0.5) phase = "BREATHE";
                                        else phase = "EXPLODE";
                                    }}
                                    
                                    updateAndDrawGroup(groups.groupCA, colors.ca);
                                    updateAndDrawGroup(groups.groupScribe, colors.scribe);
                                    updateAndDrawGroup(groups.groupStar, colors.star);

                                    requestAnimationFrame(animate);
                                }}
                                animate();
                            }});
                        }})();
                    </script>
                </body>
                </html>
                """

            # 1. ENTRY PHASE: Show            # 1. Display ENTRY Animation IMMEDIATELY
            with content_area.container():
                components.html(get_loading_html("ENTRY"), height=370)
            
            # Yield to UI for render
            time.sleep(0.5) 
            
            try:
                # Do Work
                current_activity = st.session_state.get("activity_input", "")
                current_provider = st.session_state.get("selected_provider", "gemini")
                results = map_activity_to_competency(current_activity, st.session_state.framework_data, provider=current_provider)
                st.session_state.markdown_report = generate_markdown_content(results)
                st.session_state.run_analysis = False
                
                # 2. EXIT PHASE: Explode
                with content_area.container():
                    components.html(get_loading_html("EXIT"), height=370)
                
                time.sleep(1.3) # Match the 1.2s fade-out animation
                
                content_area.empty()  # Remove
                st.rerun()
                
            except Exception as e:
                content_area.empty()
                st.error(f"Analysis failed: {e}")
        
        # Display results or placeholder
        if st.session_state.markdown_report:
            with content_area.container():
                st.markdown(st.session_state.markdown_report)
                # AI Disclaimer
                st.markdown("""
                    <p style="text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 1.5rem; font-weight: 400;">
                        AI models can make mistakes. Please review information generated.
                    </p>
                """, unsafe_allow_html=True)
        elif not st.session_state.get("run_analysis", False):
            with content_area.container():
                st.markdown("""
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; color: #94a3b8; opacity: 0.7;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                        <p style="margin-top: 20px; font-weight: 500;">Detailed mapping will appear here</p>
                    </div>
                """, unsafe_allow_html=True)
            # AI Disclaimer
            st.markdown("""
                <p style="text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 1rem; font-weight: 400;">
                    AI models can make mistakes. Please review information generated.
                </p>
            """, unsafe_allow_html=True)

    # Footer
    footer_html = """
    <div class="footer-container">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <p style="margin-bottom: 10px; font-size: 1.1rem; color: #0284c7;">Made by <strong style="color: #075985;">Adhir Singh</strong></p>
            <div style="display: flex; justify-content: center; align-items: center; gap: 20px; transform: translateY(-5px);">
                <a href="https://github.com/Adh-ir/SAICA_Scribe/issues" target="_blank" style="text-decoration: none; color: #0284c7; display: flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="opacity: 0.9;"><path fill-rule="evenodd" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" clip-rule="evenodd" /></svg>
                    <span style="font-size: 0.9rem; font-weight: 600;">Report Issue</span>
                </a>
                <a href="https://github.com/Adh-ir" target="_blank" style="text-decoration: none; color: #0284c7; display: flex; align-items: center; transition: all 0.2s;" title="GitHub">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="opacity: 0.9;"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.48 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" /></svg>
                </a>
                <a href="https://linkedin.com/in/adhirs" target="_blank" style="text-decoration: none; color: #0284c7; display: flex; align-items: center; transition: all 0.2s;" title="LinkedIn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="opacity: 0.9;"><path fill-rule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clip-rule="evenodd" /></svg>
                </a>
            </div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- 5. GUIDE PAGE ---
def show_guide_page():
    try:
        template_path = os.path.join(os.path.dirname(__file__), "templates", "guide.html")
        with open(template_path, "r") as f:
            html_content = f.read()
        
        # Fix Frame Navigation: Ensure "Back" link breaks out of iframe
        # html_content = html_content.replace('<a href="/"', '<a href="/" target="_top"') -> Button removed
        
        # Render in Iframe to support full HTML/CSS/Tailwind without Markdown interference
        #components.html(html_content, height=1200, scrolling=True)
        components.html(html_content, height=1200, scrolling=True)
        
    except Exception as e:
        st.error(f"Could not load guide: {e}")
        st.info("Ensure 'code/templates/guide.html' exists in the repository.")

# --- 6. APP CONTROLLER ---
if __name__ == "__main__":
    # Initialize view_mode
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "main"

    # Check query params for routing
    try:
        # Streamlit 1.30+
        query_params = st.query_params
        page = query_params.get("page")
    except:
        # Fallback
        page = None

    if page == "guide":
        show_guide_page()
    elif page == "settings":
        render_settings_page()
    elif has_access:
        # Also check session state in case we want to support internal state switching too (optional)
        if st.session_state.get("view_mode") == "settings":
            render_settings_page()
        else:
            show_main_page()
    else:
        show_setup_page()
# Force update

