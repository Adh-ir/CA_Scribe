
# Common Fonts (Separate to avoid @import warnings)
FONT_LINKS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@1,600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
"""

SETUP_CSS = """
<style>
/* Font import handled via FONT_LINKS */

/* Force Font globally */
html {
    background: #e0f2fe; /* Base color to prevent white flash */
}

body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    color: #1e3a8a;
    animation: fadeIn 1.5s ease-in-out;
}

@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

/* Light Gradient Background for Setup */
.stApp {
    
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* --- DOT WAVE BACKGROUND ENGINE --- */
.fluid-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    overflow: hidden;
}

/* Base Dot Pattern */
.dot-grid {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(14, 165, 233, 0.3) 1px, transparent 1px);
    background-size: 30px 30px;
    mask-image: radial-gradient(circle at 50% 50%, black 40%, transparent 80%);
    opacity: 0.6;
}

/* Animated Wave Overlay */
.wave-layer {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background-image: radial-gradient(rgba(14, 165, 233, 0.4) 1.5px, transparent 1.5px);
    background-size: 40px 40px;
    opacity: 0.4;
    animation: waveFloat 20s infinite linear;
    transform: rotate(15deg);
}

.wave-layer-2 {
    background-image: radial-gradient(rgba(56, 189, 248, 0.5) 1.5px, transparent 1.5px);
    background-size: 45px 45px;
    animation-duration: 25s;
    animation-direction: reverse;
    opacity: 0.3;
    left: -20%;
}

@keyframes waveFloat {
    0% { transform: rotate(15deg) translateY(0); }
    50% { transform: rotate(15deg) translateY(-50px); }
    100% { transform: rotate(15deg) translateY(0); }
}

/* Keep original fluid shapes but make them very subtle for depth */
.fluid-shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(50px); /* Reduced for performance */
    opacity: 0.4; /* Reduced opacity */
    animation: fluid-move 14s infinite ease-in-out;
    will-change: transform;
    mix-blend-mode: multiply;
}

.shape-1 {
    background: #7dd3fc;
    width: 65vw;
    height: 65vw;
    top: -15%;
    left: -10%;
    animation-duration: 16s;
}

.shape-2 {
    background: #bae6fd;
    width: 70vw;
    height: 70vw;
    top: 25%;
    right: -25%;
    animation-duration: 20s;
    animation-delay: -4s;
}

.shape-3 {
    background: #a5f3fc;
    width: 55vw;
    height: 55vw;
    bottom: -15%;
    left: 15%;
    animation-duration: 14s;
    animation-delay: -8s;
}

@keyframes fluid-move {
    0% { transform: translate(0, 0) scale(1) rotate(0deg); }
    33% { transform: translate(45px, 65px) scale(1.1) rotate(8deg); }
    66% { transform: translate(-35px, 25px) scale(0.9) rotate(-6deg); }
    100% { transform: translate(0, 0) scale(1) rotate(0deg); }
}

/* --- GLASS CARD (Applied to Streamlit Form) --- */
[data-testid="stForm"] {
    position: relative;
    z-index: 10;
    background: #ffffff;
    /* backdrop-filter: blur(30px); Removed */
    border: 2px solid rgba(147, 197, 253, 0.5);
    box-shadow: 
        0 4px 6px -1px rgba(0, 0, 0, 0.05),
        0 20px 40px -12px rgba(14, 165, 233, 0.15);
    border-radius: 24px;
    padding: 2.5rem;
    animation: none !important;
    transition: all 0.3s ease !important;
}

[data-testid="stForm"]:focus-within {
    border-color: #1e3a8a !important;
    box-shadow: 0 0 25px rgba(2, 132, 199, 0.5), 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}

/* --- LOGO STYLES --- */
.logo-main {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #003B5C;
}

.logo-scribe {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 600;
    color: #005F88;
}

/* --- INPUT STYLES --- */
.stTextInput input {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1.5px solid #cbd5e1 !important;
    color: #1e293b !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus {
    border-color: #1e3a8a !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
    background: #ffffff !important;
}

.stTextInput input::placeholder {
    color: #94a3b8 !important;
}

/* --- LABELS --- */
label {
    color: #64748b !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
}

/* --- BUTTON STYLES --- */
.stButton button {
    background: linear-gradient(to right, #0ea5e9, #2563eb) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 1rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3) !important;
    font-size: 1rem !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 25px -5px rgba(14, 165, 233, 0.4) !important;
    opacity: 0.95 !important;
}

.stButton button:active {
    transform: translateY(0) !important;
}

/* --- EXPANDER STYLES --- */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid #e0f2fe !important;
    border-radius: 12px !important;
    color: #0369a1 !important;
    font-weight: 600 !important;
    padding: 0.75rem 1rem !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(255, 255, 255, 0.8) !important;
    border-color: #7dd3fc !important;
}

.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.5) !important;
    border: 1px solid #e0f2fe !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1rem !important;
}

/* --- MARKDOWN IN EXPANDER --- */
[data-testid="stExpander"] p, 
[data-testid="stExpander"] li {
    color: #475569 !important;
    line-height: 1.6 !important;
}

[data-testid="stExpander"] strong {
    color: #1e293b !important;
}

[data-testid="stExpander"] a {
    color: #0ea5e9 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
}

[data-testid="stExpander"] a:hover {
    text-decoration: underline !important;
}

[data-testid="stExpander"] code {
    background: rgba(148, 163, 184, 0.15) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    color: #0f172a !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* --- ERROR/SUCCESS MESSAGES --- */
.stAlert {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 12px !important;
    border-left-width: 4px !important;
}

</style>
"""


MAIN_CSS = """
<style>
/* Font import handled via FONT_LINKS */

/* Base Font */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1e3a8a;
}

/* Transparent Background for Streamlit Main Container */
.stApp {
    background-color: transparent !important;
}

/* --- FLUID BACKGROUND ENGINE --- */
.fluid-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    overflow: hidden;
}

.fluid-shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(50px);
    opacity: 0.9;
    animation: fluid-move 14s infinite ease-in-out;
    will-change: transform;
    mix-blend-mode: multiply;
}

.shape-1 {
    background: #7dd3fc;
    width: 65vw;
    height: 65vw;
    top: -15%;
    left: -10%;
    animation-duration: 16s;
}

.shape-2 {
    background: #bae6fd;
    width: 70vw;
    height: 70vw;
    top: 25%;
    right: -25%;
    animation-duration: 20s;
    animation-delay: -4s;
}

.shape-3 {
    background: #a5f3fc;
    width: 55vw;
    height: 55vw;
    bottom: -15%;
    left: 15%;
    animation-duration: 14s;
    animation-delay: -8s;
}

@keyframes fluid-move {
    0% { transform: translate(0, 0) scale(1) rotate(0deg); }
    33% { transform: translate(45px, 65px) scale(1.1) rotate(8deg); }
    66% { transform: translate(-35px, 25px) scale(0.9) rotate(-6deg); }
    100% { transform: translate(0, 0) scale(1) rotate(0deg); }
}

/* --- GLASS CARD WRAPPER (Applied to Streamlit Border Container) --- */
/* Target the new st.container(border=True) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    background-color: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: 0px none transparent !important;
    border-width: 0px !important;
    outline: none !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin-top: 1rem;
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    position: relative !important;
    z-index: 1 !important;
}

/* Hide the default tiny border Streamlit adds */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: none !important;
}

/* TARGETED FIX: Make the main columns container white */
/* Lift the entire app container (Header + Content) closer to top */
.block-container {
    padding-top: 15px !important;
    padding-bottom: 1rem !important;
}

/* Main Container (stHorizontalBlock) styling moved to GLOBAL_HACKS_CSS for flash fix */

/* --- LOGO STYLES (From Local Index.html) --- */
.logo-main {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #003B5C !important;
}

.logo-scribe {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 600;
    color: #005F88 !important;
}

/* Vertical Separator for the Report Column (Right Side) */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-of-type(2) {
    border-left: 2px solid rgba(147, 197, 253, 0.5) !important;
    padding-left: 2rem !important;
}

/* Report Column Main Container - Scrollable */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"] {
    max-height: 65vh !important;
    overflow-y: auto !important;
    padding-right: 10px !important;
}

/* Report Title Styling - Applies to h1 inside the scrollable column */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) h1,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child h1 {
    background: -webkit-linear-gradient(120deg, #1e3a8a, #0284c7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.5rem !important;
}

/* Report H2 Styling - Deep Blue (Consistent) */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) h2,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child h2 {
    color: #1e3a8a !important;
    font-weight: 700 !important;
    margin-top: 1.5rem !important;
}

/* Report H3 Styling - Deep Blue (Consistent) */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) h3,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child h3 {
    color: #1e3a8a !important;
    font-weight: 600 !important;
}

/* Report Body Text - Dark Blue (Fix for white text issue) */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) p,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) li,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) span,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child p,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child li,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child span {
    color: #1e293b !important;
}

/* --- UI ELEMENTS --- */

/* Text Area & Inputs (New Style) */
.stTextArea textarea, .stTextInput input {
    border: 1px solid #e0f2fe !important;
    background-color: #ffffff !important;
    border-radius: 0.75rem !important;
    color: #1e293b;
    transition: all 0.2s ease-in-out;
}

/* Specific Fix for Text Area Height */
.stTextArea textarea {
    resize: none !important;
    height: 350px !important;
    max-height: 350px !important;
}

/* Model Select Box (Reverted Style) */
.stSelectbox div[data-baseweb="select"] {
    border: 1px solid #cbd5e1 !important;
    background-color: #ffffff !important;
    border-radius: 1rem !important;
    color: #1e293b;
    transition: all 0.2s ease-in-out;
}

/* Remove default Streamlit outer border to prevent double-border */
[data-baseweb="textarea"], [data-baseweb="input"] {
    border: none !important;
    background: transparent !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border: 2px solid #38bdf8 !important;
    padding: calc(0.75rem - 1px) !important;
    box-shadow: 0 0 22px rgba(56, 189, 248, 0.6) !important;
    outline: none !important;
}

/* Custom Scrollbar for Report */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"]::-webkit-scrollbar {
    width: 8px;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-track,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-track {
    background: rgba(224, 242, 254, 0.3);
    border-radius: 4px;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb {
    background: rgba(147, 197, 253, 0.8);
    border-radius: 4px;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover {
    background: rgba(56, 189, 248, 1);
}

.stSelectbox div[data-baseweb="select"]:focus-within {
    border-color: #cbd5e1 !important;
    box-shadow: none !important;
    outline: none !important;
}


/* --- BUTTON STYLES (Recreated for Flash Removal) --- */

/* Primary Button - Strict Override */
div.stButton > button[kind="primary"] {
    background: linear-gradient(to right, #0ea5e9, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.5rem !important;
    transition: transform 0.1s !important;
    box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3) !important;
    outline: none !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    opacity: 0.95 !important;
    box-shadow: 0 15px 20px -3px rgba(14, 165, 233, 0.4) !important;
}

div.stButton > button[kind="primary"]:focus,
div.stButton > button[kind="primary"]:active,
div.stButton > button[kind="primary"]:focus-visible {
    outline: none !important;
    border: none !important;
    box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3) !important; /* Keep same shadow as normal */
    transform: translateY(0) !important;
}

/* Secondary Button - Target Competency Style */
div.stButton > button[kind="secondary"],
button[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-secondary"] {
    width: 100% !important;
    border: 1px solid #e0f2fe !important;
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #94a3b8 !important; /* Even dimmer text color */
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    text-align: left !important;
    border-radius: 0.75rem !important;
    padding: 0.85rem 1.5rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    outline: none !important;
    justify-content: flex-start !important;
}

div.stButton > button[kind="secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-secondary"]:hover {
    background: #f0f9ff !important;
    background-color: #f0f9ff !important;
    border-color: #38bdf8 !important; /* Sky 400 - Stronger Border */
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 20px -3px rgba(14, 165, 233, 0.4) !important; /* Stronger Glow matching Primary */
    color: #0284c7 !important;
}

div.stButton > button[kind="secondary"]:active,
button[data-testid="stBaseButton-secondary"]:active,
[data-testid="stBaseButton-secondary"]:active {
    transform: translateY(0) !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05) !important;
}

div.stButton > button[kind="secondary"]:focus,
div.stButton > button[kind="secondary"]:focus-visible,
button[data-testid="stBaseButton-secondary"]:focus,
[data-testid="stBaseButton-secondary"]:focus {
    outline: none !important;
    border: 1px solid #e0f2fe !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    background: white !important;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    color: #0f172a;
}

/* Labels Bold Override */
.stTextArea label, .stSelectbox label, .stTextArea label p, .stSelectbox label p {
    font-weight: 700 !important;
    color: #1e3a8a !important;
    font-size: 0.9rem !important;
}
/* --- FOOTER FULL WIDTH BREAKOUT --- */
.footer-container {
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    background: rgba(255, 255, 255, 0.20);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1px solid rgba(224, 242, 254, 0.8);
    text-align: center;
    padding: 2.5rem 0;
    margin-top: 3rem;
    box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.01);
}
</style>
"""

# --- GLOBAL HACKS & OVERRIDES (Focus & Layout) ---
GLOBAL_HACKS_CSS = """
<style>
/* Prevent horizontal scroll from breakout */
body {
    overflow-x: hidden;
}
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
    margin-top: -60px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Remove blue flash/focus ring from entire container */
.block-container:focus,
.block-container:focus-within,
[data-testid="stAppViewContainer"]:focus,
[data-testid="stAppViewContainer"]:focus-within,
.main:focus,
.main:focus-within {
    outline: 0 !important;
    outline-width: 0 !important;
    outline-style: none !important;
    outline-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    -webkit-tap-highlight-color: transparent !important;
}

/* 1. GLOBAL FOCUS RESET (Simplified) */
/* We reset outline for everything BUT we don't kill box-shadow globally
   because that causes the flash on our container. */
*:focus,
*:focus-visible,
*:focus-within,
*:active {
    outline: none !important;
    outline-width: 0 !important;
    -webkit-tap-highlight-color: transparent !important;
}

/* Prevent Streamlit's default focus behavior */
.stApp *:focus,
.stApp *:active {
    outline: 0 !important;
}

/* 2. TARGET THE SPECIFIC CONTAINERS THAT FLASH BLUE */
/* Explicitly remove shadow/border from the generic wrappers */
[data-testid="stColumn"],
[data-testid="stColumn"]:focus,
[data-testid="stColumn"]:focus-within,
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlock"]:focus,
[data-testid="stVerticalBlock"]:focus-within {
    outline: 0 !important;
    box-shadow: none !important;
    border: none !important;
}

/* 3. THE MAIN CONTAINER - INDESTRUCTIBLE STYLING */
/* Applies to Normal AND all focus states equally */
[data-testid="stHorizontalBlock"],
[data-testid="stHorizontalBlock"]:focus,
[data-testid="stHorizontalBlock"]:focus-within,
[data-testid="stHorizontalBlock"]:active,
[data-testid="stHorizontalBlock"]:focus-visible,
[data-testid="stHorizontalBlock"]:target {
    background-color: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px !important;
    padding: 22px 30px 18px 30px !important;
    border: 4px solid #93c5fd !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02),
                0 20px 40px -12px rgba(14, 165, 233, 0.1) !important;
    margin-top: -40px !important;
    
    /* Performance & Stability Hooks */
    transition: none !important;
    animation: none !important;
    transform: translateZ(0); /* Force GPU layer */
    outline: none !important;
    -webkit-tap-highlight-color: transparent !important;
}

/* Ensure buttons inside don't cause container flash */
[data-testid="stHorizontalBlock"] button:focus,
[data-testid="stHorizontalBlock"] button:active,
[data-testid="stHorizontalBlock"] button:focus-visible {
    outline: none !important;
    box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3) !important; /* Keep button shadow */
}
</style>
"""

FOCUS_FIX_JS = """
<script>
// Prevent focus-related visual feedback on all elements
document.addEventListener('DOMContentLoaded', function() {
    // Prevent focus on containers
    // Prevent focus on containers DOES MORE HARM THAN GOOD FOR CSS-MATCHED CONTAINERS
    // document.addEventListener('focusin', function(e) { ... removed ... }, true);
    
    // Removed textarea focus suppression to allow the new glow effect
});
</script>
"""

LOADING_MODE_CSS = """
<style>
/* Hide EVERYTHING at the top */
header, .stHeader, [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"] { 
    display: none !important; 
    height: 0 !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* Match Background to Blue Gradient (Hides white bars) */
.stApp, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #7dd3fc 0%, #bae6fd 100%) !important;
}

/* Kill container padding */
.block-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Nuclear Iframe Positioning */
iframe[title="streamlit.components.v1.html"], iframe {
    position: fixed;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 2147483647 !important;
    border: none !important;
}
</style>
"""
