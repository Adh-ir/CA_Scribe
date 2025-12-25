
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
/* NUCLEAR FIX: Force ALL Horizontal Blocks to be White + Padded */
[data-testid="stHorizontalBlock"] {
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
[data-testid="stHorizontalBlock"]:focus,
[data-testid="stHorizontalBlock"]:focus-within {
    background-color: #ffffff !important;
    border-radius: 20px !important;
    padding: 30px !important;
    border: 4px solid #93c5fd !important;
    outline: none !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02),
                0 20px 40px -12px rgba(14, 165, 233, 0.1) !important;
    transition: none !important;
    animation: none !important;
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
    border: 1px solid #e0f2fe !important; /* Softer border to match button */
    background-color: #ffffff !important;
    border-radius: 0.75rem !important; /* Match button radius */
    color: #1e293b;
    transition: all 0.2s ease-in-out;
}

/* Remove default Streamlit outer border to prevent double-border */
[data-baseweb="textarea"], [data-baseweb="input"] {
    border: none !important;
    background: transparent !important;
}

.stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
    border: 2px solid #38bdf8 !important; /* Double thickness (2px) + Sky Blue */
    padding: calc(0.75rem - 1px) !important; /* Adjust padding to prevent layout shift */
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.5) !important; /* Increased glow (+20%) */
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

/* Secondary Button - Strict Override */
div.stButton > button[kind="secondary"] {
    border: 1px solid #e0f2fe !important;
    background: white !important;
    color: #0369a1 !important;
    font-weight: 600 !important;
    border-radius: 0.75rem !important;
    padding: 0.75rem 1.5rem !important;
    outline: none !important;
}

div.stButton > button[kind="secondary"]:hover {
    border-color: #7dd3fc !important;
    color: #0284c7 !important;
    background: #f0f9ff !important;
}

div.stButton > button[kind="secondary"]:focus,
div.stButton > button[kind="secondary"]:active,
div.stButton > button[kind="secondary"]:focus-visible {
    outline: none !important;
    border: 1px solid #e0f2fe !important;
    box-shadow: none !important;
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
    background: rgba(255, 255, 255, 0.75);
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

/* Nuclear option: Remove ALL focus indicators from EVERYTHING */
*,
*:before,
*:after {
    outline: 0 !important;
    outline-width: 0 !important;
    -webkit-tap-highlight-color: transparent !important;
}

*:focus,
*:active,
*:focus-visible,
*:focus-within {
    outline: 0 !important;
    outline-width: 0 !important;
    outline-style: none !important;
    outline-color: transparent !important;
    box-shadow: none !important;
    border-color: inherit !important;
    -webkit-tap-highlight-color: transparent !important;
}

/* Prevent Streamlit's default focus behavior */
.stApp *:focus,
.stApp *:active {
    outline: 0 !important;
    box-shadow: none !important;
}

/* TARGET THE SPECIFIC CONTAINERS THAT FLASH BLUE */
/* Excludes HorizontalBlock to allow custom shadow */
[data-testid="stColumn"],
[data-testid="stColumn"]:focus,
[data-testid="stColumn"]:focus-within,
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlock"]:focus,
[data-testid="stVerticalBlock"]:focus-within {
    outline: 0 !important;
    outline-width: 0 !important;
    outline-style: none !important;
    outline-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    -webkit-tap-highlight-color: transparent !important;
}

/* Force Main Container Shadow on Focus (Override Nuclear Option) */
[data-testid="stHorizontalBlock"]:focus,
[data-testid="stHorizontalBlock"]:focus-within {
    background-color: #ffffff !important;
    border-radius: 20px !important;
    padding: 30px !important;
    border: 4px solid #93c5fd !important;
    outline: none !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02),
                0 20px 40px -12px rgba(14, 165, 233, 0.1) !important;
    transition: none !important;
    animation: none !important;
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
