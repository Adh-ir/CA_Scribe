import streamlit as st
import os
import sys
import time
import requests
# Deploy Trigger: V3.3 - Force Trigger
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

# Force global styles immediately
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
    """Checks for API keys in Streamlit secrets or OS environ."""
    # Priority: Session > Secrets > OS > Input
    # Safely get from secrets (may not exist on first run)
    def safe_secrets_get(key):
        try:
            return st.secrets.get(key)
        except:
            return None
    
    keys = {
        "GOOGLE_API_KEY": st.session_state.get("GOOGLE_API_KEY") or safe_secrets_get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY"),
        "GROQ_API_KEY": st.session_state.get("GROQ_API_KEY") or safe_secrets_get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY"),
        "GITHUB_TOKEN": st.session_state.get("GITHUB_TOKEN") or safe_secrets_get("GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN"),
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
        # Enhanced Logo Section - Moved UP by ~50px (10vh -> 5vh)
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2.5rem; margin-top: 2vh;">
                <div style="display: flex; align-items: baseline; justify-content: center; gap: 0.25rem; margin-bottom: 0.5rem;">
                     <span class="logo-main" style="font-size: 4rem;">CA</span>
                     <span class="logo-scribe" style="font-size: 4rem; position: relative;">
                        Scribe 
                        <span style="position: absolute; top: -8px; right: -28px; font-size: 1.75rem; color: #0ea5e9;">✦</span>
                     </span>
                </div>
                <div style="font-family: 'Inter', sans-serif; font-weight: 600; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; font-size: 0.85rem; margin-top: -0.25rem;">
                    AI-Powered Competency Mapper
                </div>
                <div style="font-family: 'Inter', sans-serif; font-weight: 500; color: #1e3a8a; font-size: 0.95rem; margin-top: 2rem; line-height: 1.6; max-width: 400px; margin-left: auto; margin-right: auto; text-shadow: none;">
                    Please retrieve and install one or all of the API keys below to get access to each model
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
                        Keys are stored locally in .streamlit/secrets.toml
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

            # Helper Link
            st.markdown("""
                <div style="text-align: center; margin-top: 0.5rem; margin-bottom: 0.5rem;">
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
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 1rem; margin-bottom: 2rem;">
            <div>
                <div style="display: flex; align-items: baseline; gap: 0.25rem;">
                    <span class="logo-main" style="font-size: 2.75rem;">CA</span>
                    <span class="logo-scribe" style="font-size: 2.75rem; position: relative;">
                        Scribe 
                        <span style="font-size: 1.25rem; color: #0ea5e9; position: absolute; top: -6px; right: -20px;">✦</span>
                    </span>
                </div>
                <div style="font-size: 1rem; color: #64748b; font-weight: 500; margin-top: -10px; letter-spacing: 0.025em; padding-left: 0.25rem;">AI-Powered Competency Mapper</div>
            </div>
            <div>
                <button style="
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
                ">
                    <span style="display: inline-block; width: 8px; height: 8px; background: #4ade80; border-radius: 50%;"></span>
                    Settings
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Main Content (The Glass Card) ---
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
        
        if st.button("✨ Target Competency                                                              +", use_container_width=True, type="secondary"):
            st.session_state.activity_input = "COMPETENCY: [Insert Name] EVIDENCE: "
        
        st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
        
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
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
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
        st.markdown(f'<h3 style="color: #1e3a8a; font-family: \'Inter\', sans-serif; margin-top: 0; margin-bottom: 1rem;">Analysis Report</h3>', unsafe_allow_html=True)
        
        # Check if analysis was triggered
        if st.session_state.get("run_analysis", False):
            # Clear the flag
            st.session_state.run_analysis = False
            
            # Show modern loading animation in placeholder area
            loading_placeholder = st.empty()
            loading_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@800&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
                    <style>
                        body { margin: 0; padding: 0; background: transparent; }
                        @keyframes dots {
                            0%, 20% { content: '.'; }
                            40% { content: '..'; }
                            60%, 100% { content: '...'; }
                        }
                        .loading-container {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            height: 350px;
                            background: transparent;
                        }
                        #text-canvas {
                            width: 800px;
                            height: 200px;
                        }
                        .loading-text {
                            margin-top: 20px;
                            font-weight: 600;
                            font-size: 1rem;
                            color: #0369a1;
                            font-family: 'Inter', sans-serif;
                        }
                        .loading-dots::after {
                            content: '';
                            animation: dots 1.5s steps(1, end) infinite;
                        }
                        .loading-subtext {
                            margin-top: 6px;
                            font-size: 0.85rem;
                            color: #94a3b8;
                            font-family: 'Inter', sans-serif;
                        }
                    </style>
                </head>
                <body>
                    <div class="loading-container">
                        <canvas id="text-canvas" width="800" height="200"></canvas>
                        <p class="loading-text">Analyzing with AI<span class="loading-dots"></span></p>
                        <p class="loading-subtext">Mapping competencies from your activity</p>
                    </div>
                    <script>
                        document.fonts.ready.then(() => {
                            const canvas = document.getElementById('text-canvas');
                            if (!canvas) return;
                            const ctx = canvas.getContext('2d');
                            const w = canvas.width;
                            const h = canvas.height;
                            
                            const colors = {
                                ca: '#003B5C',
                                scribe: '#005F88', 
                                star: '#0ea5e9'
                            };
                            
                            // Draw text to get pixel positions
                            const tempCanvas = document.createElement('canvas');
                            tempCanvas.width = w;
                            tempCanvas.height = h;
                            const tempCtx = tempCanvas.getContext('2d');
                            
                            const fontSize = 100;
                            const baseY = h / 2 + fontSize / 3;
                            
                            // Measure total width first for centering
                            tempCtx.font = `800 ${fontSize}px Inter`;
                            const caWidth = tempCtx.measureText('CA').width;
                            tempCtx.font = `italic 600 ${fontSize}px 'Playfair Display'`;
                            const scribeWidth = tempCtx.measureText('Scribe').width;
                            const starSize = fontSize * 0.35;
                            const spacing = 8;
                            const totalWidth = caWidth + spacing + scribeWidth + spacing + starSize * 2;
                            const startX = (w - totalWidth) / 2;
                            
                            // Draw CA
                            tempCtx.font = `800 ${fontSize}px Inter`;
                            tempCtx.fillStyle = colors.ca;
                            tempCtx.fillText('CA', startX, baseY);
                            
                            // Draw Scribe
                            tempCtx.font = `italic 600 ${fontSize}px 'Playfair Display'`;
                            tempCtx.fillStyle = colors.scribe;
                            tempCtx.fillText('Scribe', startX + caWidth + spacing, baseY);
                            
                            // Draw star
                            const starX = startX + caWidth + spacing + scribeWidth + spacing + starSize;
                            const starY = baseY - fontSize * 0.6;
                            tempCtx.fillStyle = colors.star;
                            tempCtx.beginPath();
                            const sx = starX, sy = starY;
                            tempCtx.moveTo(sx, sy - starSize);
                            tempCtx.lineTo(sx + starSize * 0.35, sy - starSize * 0.35);
                            tempCtx.lineTo(sx + starSize, sy);
                            tempCtx.lineTo(sx + starSize * 0.35, sy + starSize * 0.35);
                            tempCtx.lineTo(sx, sy + starSize);
                            tempCtx.lineTo(sx - starSize * 0.35, sy + starSize * 0.35);
                            tempCtx.lineTo(sx - starSize, sy);
                            tempCtx.lineTo(sx - starSize * 0.35, sy - starSize * 0.35);
                            tempCtx.closePath();
                            tempCtx.fill();
                            
                            // Sample pixels
                            const imageData = tempCtx.getImageData(0, 0, w, h).data;
                            const particles = [];
                            const step = 2;
                            
                            for (let y = 0; y < h; y += step) {
                                for (let x = 0; x < w; x += step) {
                                    const i = (y * w + x) * 4;
                                    if (imageData[i + 3] > 128) {
                                        const r = imageData[i], g = imageData[i + 1], b = imageData[i + 2];
                                        const color = `rgb(${r},${g},${b})`;
                                        const size = 0.6;
                                        // Random movement properties for each particle
                                        const speedX = (Math.random() - 0.5) * 0.8;
                                        const speedY = (Math.random() - 0.5) * 0.8;
                                        const phaseX = Math.random() * Math.PI * 2;
                                        const phaseY = Math.random() * Math.PI * 2;
                                        const amp = 6 + Math.random() * 6;
                                        particles.push({ 
                                            ox: x, oy: y, // original position
                                            x, y, 
                                            color, size, 
                                            speedX, speedY, phaseX, phaseY, amp
                                        });
                                    }
                                }
                            }
                            
                            let time = 0;
                            const cx = w / 2;
                            const cy = h / 2;
                            
                            // Pre-calculate each particle's direction from center
                            particles.forEach(p => {
                                const dx = p.ox - cx;
                                const dy = p.oy - cy;
                                const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                                p.nx = dx / dist; // normalized direction x
                                p.ny = dy / dist; // normalized direction y
                                p.dist = dist;    // distance from center
                            });
                            
                            function animate() {
                                ctx.clearRect(0, 0, w, h);
                                time += 0.04;
                                
                                // Global breathing wave
                                const breathe = Math.sin(time * 0.8);
                                
                                particles.forEach(p => {
                                    // Movement amount based on distance from center with variable speed
                                    // Outer particles breathe faster (higher frequency)
                                    // Inner particles breathe slower (lower frequency)
                                    // Base speed 0.8, increases with distance
                                    const particleSpeed = 0.8 + (p.dist / 150);
                                    const particleBreathe = Math.sin(time * particleSpeed);
                                    
                                    const moveAmount = particleBreathe * (p.dist / 80) * 8;
                                    
                                    // Move along the direction from center
                                    const px = p.ox + p.nx * moveAmount;
                                    const py = p.oy + p.ny * moveAmount;
                                    
                                    ctx.beginPath();
                                    ctx.arc(px, py, p.size, 0, Math.PI * 2);
                                    ctx.fillStyle = p.color;
                                    ctx.globalAlpha = 0.9;
                                    ctx.fill();
                                });
                                ctx.globalAlpha = 1;
                                
                                requestAnimationFrame(animate);
                            }
                            animate();
                        });
                    </script>
                </body>
                </html>
            """
            # Run analysis
            try:
                current_activity = st.session_state.get("activity_input", "")
                current_provider = st.session_state.get("selected_provider", "gemini")
                results = map_activity_to_competency(current_activity, st.session_state.framework_data, provider=current_provider)
                st.session_state.markdown_report = generate_markdown_content(results)
                loading_placeholder.empty()  # Clear loading animation
            except Exception as e:
                loading_placeholder.empty()
                st.error(f"Analysis failed: {e}")
        
        # Display results or placeholder
        if st.session_state.markdown_report:
            st.markdown(st.session_state.markdown_report)
        elif not st.session_state.get("run_analysis", False):
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

    # Footer
    # Footer
    # Footer
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
        components.html(html_content, height=1200, scrolling=True)
        
    except Exception as e:
        st.error(f"Could not load guide: {e}")
        st.info("Ensure 'code/templates/guide.html' exists in the repository.")

# --- 6. APP CONTROLLER ---
if __name__ == "__main__":
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
    elif has_access:
        show_main_page()
    else:
        show_setup_page()
