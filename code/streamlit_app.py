import streamlit as st
import os
import sys
import time
import streamlit.components.v1 as components
from PIL import Image

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.streamlit_styles import SETUP_CSS, MAIN_CSS, FONT_LINKS
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
st.markdown("""
    <style>
    /* Force Transparent Background for App */
    .stApp, [data-testid="stAppViewContainer"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Hide Streamlit Header/Toolbar */
    header, [data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Custom Semi-Wide Layout (User Requested "Halfway" Width) */
    .block-container {
        max-width: 1200px !important;
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-top: -40px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOADING ANIMATION (Local & Cloud Compatible) ---
if "loading_complete" not in st.session_state:
    st.session_state.loading_complete = False

if not st.session_state.loading_complete:
    # Fullscreen iframe hack & PADDING OVERRIDE
    st.markdown("""
        <style>
        /* Override the global 1200px limit during loading */
        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Match Background to Blue Gradient (Hides white bars) */
        .stApp, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #7dd3fc 0%, #bae6fd 100%) !important;
        }
        
        iframe[title="streamlit.components.v1.html"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 999999;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)
LOADING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
  <style>
    body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: linear-gradient(135deg, #7dd3fc 0%, #bae6fd 100%); font-family: 'Inter', sans-serif; }
    #container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
    #introCanvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; transition: opacity 1.5s ease-out; }
    #precise-text { position: relative; z-index: 2; opacity: 0; transition: opacity 1.5s ease-out; display: flex; flex-direction: column; align-items: center; justify-content: center; -webkit-font-smoothing: antialiased; top: -70px; }
    #loading-label { 
        position: absolute; 
        top: calc(50% - 70px); 
        left: 50%; 
        transform: translate(-50%, -50%); 
        font-family: 'Inter', sans-serif; 
        font-weight: 300; 
        font-size: 24px; 
        letter-spacing: 0.2em;
        color: #003B5C; 
        opacity: 1; 
        transition: opacity 1.0s ease-out;
        z-index: 2;
    }
    .brand-row { display: flex; align-items: center; line-height: 1; }
    .brand-ca { font-family: 'Inter', sans-serif; font-weight: 800; color: #003B5C; }
    .brand-scribe { font-family: 'Playfair Display', serif; font-weight: 600; font-style: italic; color: #005F88; margin-left: 0.15em; }
    .brand-star { color: #0ea5e9; margin-left: 0.15em; margin-bottom: 0.4em; }
    .brand-subtitle { font-family: 'Inter', sans-serif; font-weight: 600; color: #334155; margin-top: 15px; letter-spacing: 0.02em; }
    .cross-fade #introCanvas { opacity: 0; }
    .cross-fade #precise-text { opacity: 1; }
    .cross-fade #loading-label { opacity: 0; }
  </style>
</head>
<body>
  <div id="container">
    <canvas id="introCanvas"></canvas>
    <div id="loading-label">LOADING...</div>
    <div id="precise-text">
       <div class="brand-row">
          <span class="brand-ca" id="dom-ca">CA</span>
          <span class="brand-scribe" id="dom-scribe">Scribe</span>
          <svg class="brand-star" id="dom-star" width="0" height="0" viewBox="0 0 24 24" fill="currentColor">
             <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z" />
          </svg>
       </div>
       <div class="brand-subtitle" id="dom-sub">AI-Powered Competency Mapper</div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('introCanvas');
    const ctx = canvas.getContext('2d');
    const elCA = document.getElementById('dom-ca');
    const elScribe = document.getElementById('dom-scribe');
    const elStar = document.getElementById('dom-star');
    const elSub = document.getElementById('dom-sub');

    const CONFIG = {
      formationDuration: 8000, 
      densityStep: 1, 
      colors: { ca: '#003B5C', scribe: '#005F88', star: '#0ea5e9', subtitle: '#334155' },
      offsetX: 2, 
      offsetY: 6
    };

    let width, height;
    let particles = [];
    
    // STATE MACHINE
    const STATE = { WAITING: 0, FORMING: 1, DONE: 2 };
    
    // START IMMEDIATELY
    let currentState = STATE.FORMING;
    let formationStartTime = null;

    document.fonts.ready.then(() => { setTimeout(init, 100); });

    function resize() {
      const dpr = window.devicePixelRatio || 1;
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      ctx.scale(dpr, dpr);
      
      const mainSize = Math.min(width / 6, 120);
      elCA.style.fontSize = mainSize + 'px';
      elScribe.style.fontSize = mainSize + 'px';
      const starSize = mainSize * 0.4;
      elStar.setAttribute('width', starSize);
      elStar.setAttribute('height', starSize);
      elStar.style.width = starSize + 'px';
      elStar.style.height = starSize + 'px';
      elSub.style.fontSize = (mainSize * 0.22) + 'px';
    }

    window.addEventListener('resize', () => { resize(); init(); });

    function getTargetsFromDOM() {
       const targets = [];
       const dpr = window.devicePixelRatio || 1;
       function scanElement(el, color) {
          const rect = el.getBoundingClientRect();
          const style = window.getComputedStyle(el);
          const tmp = document.createElement('canvas');
          tmp.width = width * dpr;
          tmp.height = height * dpr;
          const tCtx = tmp.getContext('2d');
          tCtx.scale(dpr, dpr);
          tCtx.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
          tCtx.textBaseline = 'top'; 
          tCtx.fillStyle = color;
          tCtx.fillText(el.innerText, rect.left + CONFIG.offsetX, rect.top + CONFIG.offsetY); 
          const imgData = tCtx.getImageData(0, 0, width * dpr, height * dpr).data;
          const step = CONFIG.densityStep * dpr;
          const sY = Math.max(0, Math.floor((rect.top+CONFIG.offsetY-20)*dpr));
          const eY = Math.min(height*dpr, Math.floor((rect.bottom+CONFIG.offsetY+20)*dpr));
          const sX = Math.max(0, Math.floor((rect.left+CONFIG.offsetX-20)*dpr));
          const eX = Math.min(width*dpr, Math.floor((rect.right+CONFIG.offsetX+20)*dpr));

           for (let y = sY; y < eY; y += step) { 
             for (let x = sX; x < eX; x += step) {
               if (imgData[(y * width * dpr + x) * 4 + 3] > 200) {
                 targets.push({ x: x / dpr, y: y / dpr, color: color });
               }
             }
           }
       }
       scanElement(elCA, CONFIG.colors.ca);
       scanElement(elScribe, CONFIG.colors.scribe);
       scanElement(elSub, CONFIG.colors.subtitle);

       const sRect = elStar.getBoundingClientRect();
       const sTmp = document.createElement('canvas');
       sTmp.width = width * dpr;
       sTmp.height = height * dpr;
       const sCTX = sTmp.getContext('2d');
       sCTX.scale(dpr, dpr);
       sCTX.fillStyle = CONFIG.colors.star;
       
       const scaleX = sRect.width / 24;
       const scaleY = sRect.height / 24;
       sCTX.translate(sRect.left + CONFIG.offsetX, sRect.top + CONFIG.offsetY);
       sCTX.scale(scaleX, scaleY);
       sCTX.beginPath();
       sCTX.moveTo(12, 0); sCTX.lineTo(14.59, 9.41); sCTX.lineTo(24, 12); sCTX.lineTo(14.59, 14.59);
       sCTX.lineTo(12, 24); sCTX.lineTo(9.41, 14.59); sCTX.lineTo(0, 12); sCTX.lineTo(9.41, 9.41); sCTX.lineTo(12, 0);
       sCTX.fill();
       
       const sData = sCTX.getImageData(0,0,width*dpr, height*dpr).data;
       const sStep = CONFIG.densityStep * dpr;
       const syS = Math.floor((sRect.top+CONFIG.offsetY)*dpr);
       const syE = Math.floor((sRect.bottom+CONFIG.offsetY)*dpr);
       const sxS = Math.floor((sRect.left+CONFIG.offsetX)*dpr);
       const sxE = Math.floor((sRect.right+CONFIG.offsetX)*dpr);

       for(let sy=syS; sy<syE; sy+=sStep){
          for(let sx=sxS; sx<sxE; sx+=sStep){
             if(sData[(sy * width * dpr + sx) * 4 + 3]>200) {
                targets.push({x: sx/dpr, y: sy/dpr, color: CONFIG.colors.star});
             }
          }
       }
       return targets;
    }

    class Particle {
      constructor(target, w, h) {
        this.tx = target.x;
        this.ty = target.y;
        this.color = target.color;
        
        const r = Math.random();
        if (r < 0.49) this.formationSize = 0.5;
        else if (r < 0.74) this.formationSize = 0.5 + Math.random() * 0.5;
        else if (r < 0.93) this.formationSize = 1.0 + Math.random() * 1.0;
        else if (r < 0.99) this.formationSize = 2.0 + Math.random() * 1.0;
        else this.formationSize = 3.0 + Math.random() * 1.0;
        
        this.driftSize = this.formationSize; 
        
        if (this.formationSize === 0.5) {
             const r2 = Math.random();
             if (r2 < 0.10) { 
                 this.driftSize = 3.0 + Math.random() * 1.0; 
             } else if (r2 < 0.20) {
                 this.driftSize = 4.0 + Math.random() * 1.0;
             }
        }
        
        this.currentSize = this.driftSize;
        this.x = Math.random() * w; 
        this.y = Math.random() * h;
        this.driftVx = -(0.5 + Math.random() * 0.5); 
        this.phase = Math.random() * Math.PI * 2;
        this.swirlRange = 15 + Math.random() * 30; 
        
        const nx = this.tx / w; 
        this.arrivalDuration = 1500 + (nx * 1000); 
      }

      update(time, elapsedFormation) {
        let targetSize = this.driftSize;
        
        if (currentState === STATE.WAITING) {
             // Not used here, we jump to Forming
        } else if (currentState === STATE.FORMING) {
            targetSize = this.formationSize; 
            const crystallizeStart = 5000; 
            
            if (elapsedFormation < this.arrivalDuration) {
               const dx = this.tx - this.x;
               const dy = this.ty - this.y;
               this.x += dx * 0.04; 
               this.y += dy * 0.04;
               this.y += Math.sin(this.x * 0.01 + time * 0.002) * 2;
               
            } else if (elapsedFormation < crystallizeStart) {
               const swirlX = Math.cos(time * 0.0015 + this.phase) * this.swirlRange;
               const swirlY = Math.sin(time * 0.0010 + this.phase) * this.swirlRange; 
               const dx = this.tx - this.x;
               const dy = this.ty - this.y;
               this.x += dx * 0.1;
               this.y += dy * 0.1;
               this.x += swirlX * 0.05;
               this.y += swirlY * 0.05;
               
            } else {
               const p = (elapsedFormation - crystallizeStart) / (8000 - crystallizeStart);
               const clampedP = Math.max(0, Math.min(1, p));
               const ease = clampedP < 0.5 ? 2 * clampedP * clampedP : 1 - Math.pow(-2 * clampedP + 2, 2) / 2;
               const currentSwirlRange = this.swirlRange * (1 - ease);
               const swirlX = Math.cos(time * 0.0015 + this.phase) * currentSwirlRange;
               const swirlY = Math.sin(time * 0.0010 + this.phase) * currentSwirlRange;
               const targetX = this.tx + swirlX; 
               const targetY = this.ty + swirlY;
               this.x += (targetX - this.x) * 0.2;
               this.y += (targetY - this.y) * 0.2;
            }
        }
        this.currentSize += (targetSize - this.currentSize) * 0.05;
      }

      draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.currentSize, 0, Math.PI*2);
        ctx.fill();
      }
    }

    function init() {
      resize();
      const targets = getTargetsFromDOM();
      particles = targets.map(t => new Particle(t, width, height));
      requestAnimationFrame(animate);
      
      const lbl = document.getElementById('loading-label');
      if(lbl) {
        // Fade out label quickly as we start forming
        setTimeout(() => lbl.style.opacity = '0', 500);
      }
    }

    function animate(timestamp) {
      if (!formationStartTime) formationStartTime = timestamp;
      const elapsedFormation = timestamp - formationStartTime;
      
      ctx.clearRect(0, 0, width, height);
      if (particles.length > 0) {
        for (let i = 0; i < particles.length; i++) {
          particles[i].update(timestamp, elapsedFormation);
          particles[i].draw(ctx);
        }
      }
      
      if (elapsedFormation > 7000) {
         document.body.classList.add('cross-fade');
      }
      
      requestAnimationFrame(animate);
    }
  </script>
</body>
</html>
"""

if not st.session_state.loading_complete:
    # Fullscreen iframe hack
    st.markdown("""
        <style>
        iframe[title="streamlit.components.v1.html"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 999999;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
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
    # Inject CSS
    st.markdown(FONT_LINKS, unsafe_allow_html=True)
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
                <div style="font-size: 1rem; color: #64748b; font-weight: 500; margin-top: 5px; letter-spacing: 0.025em; padding-left: 0.25rem;">AI-Powered Competency Mapper</div>
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
        # Helper Prompt
        if st.button("✨ Target Competency Template", help="Click to pre-fill a template"):
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
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        if st.button("Generate Analysis 🚀", use_container_width=True, type="primary"):
            if not activity.strip():
                st.warning("Please describe your activity first.")
            else:
                with st.spinner("Analyzing with AI..."):
                    try:
                        results = map_activity_to_competency(activity, st.session_state.framework_data, provider=provider)
                        st.session_state.markdown_report = generate_markdown_content(results)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

    # --- RIGHT PANEL (Report) ---
    with main_col2:
        st.markdown("### Analysis Report")
        if st.session_state.markdown_report:
            st.markdown(st.session_state.markdown_report)
        else:
            st.markdown("""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; color: #94a3b8; opacity: 0.7;">
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
                
        # st.markdown('</div>', unsafe_allow_html=True) # Removed invalid wrapper

    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; color: #64748b; font-size: 0.8rem; border-top: 1px solid #e2e8f0; padding-top: 20px;">
            Made by <strong style="color: #0369a1;">Adhir Singh</strong>
             &nbsp;&bull;&nbsp; <a href="https://github.com/Adh-ir" target="_blank" style="color: #64748b; text-decoration: none;">GitHub</a>
             &nbsp;&bull;&nbsp; <a href="https://linkedin.com/in/adhirs" target="_blank" style="color: #64748b; text-decoration: none;">LinkedIn</a>
        </div>
    """, unsafe_allow_html=True)

# --- 5. APP CONTROLLER ---
if has_access:
    show_main_page()
else:
    show_setup_page()
