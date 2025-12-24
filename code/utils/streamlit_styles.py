
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
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Light Gradient Background for Setup */
.stApp {
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    color: #1e3a8a;
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
    filter: blur(80px); /* Increased blur */
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
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border: 2px solid rgba(147, 197, 253, 0.5);
    box-shadow: 
        0 4px 6px -1px rgba(0, 0, 0, 0.05),
        0 20px 40px -12px rgba(14, 165, 233, 0.15);
    border-radius: 24px;
    padding: 2.5rem;
    animation: none !important;
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
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15) !important;
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
    filter: blur(65px);
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

/* NUCLEAR FIX: Force ALL Horizontal Blocks to be White + Padded */
div[class*="stHorizontalBlock"] {
    background-color: #ffffff !important;
    border-radius: 20px;
    padding: 30px !important;
    border: 4px solid #93c5fd !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02),
                0 20px 40px -12px rgba(14, 165, 233, 0.1) !important;
    margin-top: -40px !important;
    transition: none !important;
    animation: none !important;
}

/* Prevent focus-related visual changes on horizontal block */
div[class*="stHorizontalBlock"]:focus,
div[class*="stHorizontalBlock"]:focus-within {
    border: 4px solid #93c5fd !important;
    outline: none !important;
}

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

/* --- UI ELEMENTS --- */

/* Text Area & Inputs */
.stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stTextInput input {
    border: 1px solid #cbd5e1;
    background-color: #ffffff !important; /* Solid White Items */
    border-radius: 1rem;
    color: #1e293b;
}

.stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
    border-color: #cbd5e1;
    /* Removed blue glow: box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.2); */
}


/* Primary Button (Gradient Blue) */
button[kind="primary"] {
    background: linear-gradient(to right, #0ea5e9, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.5rem !important;
    transition: transform 0.1s !important;
    box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3) !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    opacity: 0.95 !important;
}

/* Secondary Button (Helper) */
button[kind="secondary"] {
    border: 1px solid #e0f2fe !important;
    background: white !important;
    color: #0369a1 !important;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    color: #0f172a;
}
</style>
"""
