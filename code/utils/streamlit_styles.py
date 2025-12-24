
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

/* Base Dark Theme for Setup */
.stApp {
    background-color: #02040a; /* Deepest blue-black */
    color: white;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* --- RAYCAST-LIKE AURORA --- */
.aurora-container {
    position: fixed;
    top: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 250vw;
    height: 250vh;
    z-index: 0;
    pointer-events: none;
    background: 
        radial-gradient(circle at 60% 60%, rgba(56, 189, 248, 0.4), transparent 40%),
        conic-gradient(from 0deg at 50% 50%, rgba(14, 165, 233, 0.1), rgba(6, 182, 212, 0.3), rgba(37, 99, 235, 0.2), rgba(14, 165, 233, 0.1));
    filter: blur(60px);
    animation: rotateAurora 40s linear infinite;
    mix-blend-mode: screen;
}

.aurora-secondary {
    position: fixed;
    top: -30%;
    left: 40%;
    width: 200vw;
    height: 200vh;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.2), transparent 60%);
    filter: blur(80px);
    animation: pulseGlow 10s ease-in-out infinite alternate;
    mix-blend-mode: screen;
}

.beam {
    position: absolute;
    top: -20%;
    left: 50%;
    width: 150px;
    height: 150vh;
    background: linear-gradient(180deg, rgba(56, 189, 248, 0.6), transparent);
    filter: blur(50px);
    transform-origin: top center;
    animation: swingBeam 8s ease-in-out infinite alternate;
    mix-blend-mode: overlay;
}

.beam-2 {
    animation-duration: 12s;
    background: linear-gradient(180deg, rgba(168, 85, 247, 0.4), transparent); /* Subtle purple hint */
    height: 180vh;
    width: 200px;
    animation-delay: -5s;
}

@keyframes rotateAurora {
    from { transform: translateX(-50%) rotate(0deg); }
    to { transform: translateX(-50%) rotate(360deg); }
}

@keyframes swingBeam {
    from { transform: translateX(-50%) rotate(-25deg); }
    to { transform: translateX(-50%) rotate(25deg); }
}

@keyframes pulseGlow {
    0% { opacity: 0.3; transform: scale(1); }
    100% { opacity: 0.7; transform: scale(1.1); }
}

/* --- STARS --- */
.stars {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: 
        radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
        radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px);
    background-size: 550px 550px, 350px 350px;
    background-position: 0 0, 40px 60px;
    opacity: 0.4;
    z-index: 0;
    animation: twinkle 5s infinite alternate;
}

@keyframes twinkle {
    0% { opacity: 0.3; }
    100% { opacity: 0.5; }
}

/* --- GLASS CARD (Applied to Streamlit Form) --- */
[data-testid="stForm"] {
    position: relative;
    z-index: 10;
    background: rgba(10, 10, 15, 0.75); /* Darker, more contrast */
    backdrop-filter: blur(40px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 
        0 0 0 1px rgba(0,0,0,0.5),
        0 20px 40px -10px rgba(0,0,0,0.8),
        0 0 120px rgba(56, 189, 248, 0.25); /* Stronger blue glow */
    border-radius: 20px;
    padding: 3rem;
    animation: cardFloat 6s ease-in-out infinite alternate;
}

@keyframes cardFloat {
    0% { transform: translateY(0); }
    100% { transform: translateY(-10px); }
}

/* --- TEXT STYLES --- */
h1 {
    font-weight: 700;
}

/* Inputs */
.stTextInput input {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTextInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15) !important;
}

/* Labels */
label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
}

/* Button */
.stButton button {
    background: white !important;
    color: black !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 1rem !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.3) !important;
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
/* NUCLEAR FIX: Force ALL Horizontal Blocks to be White + Padded */
div[class*="stHorizontalBlock"] {
    background-color: #ffffff !important;
    border-radius: 20px;
    padding: 30px !important;
    border: 4px solid #93c5fd !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02),
                0 20px 40px -12px rgba(14, 165, 233, 0.1) !important;
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
    border-color: #38bdf8;
    box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.2);
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
