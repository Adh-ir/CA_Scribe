import webbrowser
import os
import time
import subprocess
import threading
from pathlib import Path

# 1. Define Loading HTML content (Identical to original launcher.py but redirects to port 8501)
LOADING_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CA Scribe - Loading...</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
  <style>
    body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: linear-gradient(135deg, #7dd3fc 0%, #bae6fd 100%); font-family: 'Inter', sans-serif; cursor: wait; }
    #container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; z-index: 9999; }
    #introCanvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; transition: opacity 1.5s ease-out; }
    #precise-text { position: relative; z-index: 2; opacity: 0; transition: opacity 1.5s ease-out; display: flex; flex-direction: column; align-items: center; justify-content: center; -webkit-font-smoothing: antialiased; }
    #loading-label { 
        position: absolute; 
        top: 50%; 
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
    .brand-star { font-family: 'Inter', sans-serif; color: #0ea5e9; margin-left: 0.25em; margin-bottom: 0.4em; }
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
          <span class="brand-star" id="dom-star" style="display: inline-flex; align-items: center;"><svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="transform: rotate(28deg);"><path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z" fill="#0ea5e9"/></svg></span>
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
      formationDuration: 5000, 
      densityStep: 1, 
      colors: { ca: '#003B5C', scribe: '#005F88', star: '#0ea5e9', subtitle: '#334155' },
      offsetX: 2, 
      offsetY: 6
    };

    let width, height;
    let particles = [];
    
    // STATE MACHINE
    const STATE = { WAITING: 0, FORMING: 1, DONE: 2 };
    let currentState = STATE.WAITING;
    let formationStartTime = null;

    document.fonts.ready.then(() => { setTimeout(init, 200); });

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
      
      const starSize = mainSize * 0.45; // Matched to main app
      elStar.style.fontSize = starSize + 'px';
      
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
       scanElement(elStar, CONFIG.colors.star); // Generic scan for character
       scanElement(elSub, CONFIG.colors.subtitle);

       return targets;
    }

    class Particle {
      constructor(target, w, h) {
        this.tx = target.x;
        this.ty = target.y;
        this.color = target.color;
        
        // --- FORMATION SIZE MIX (Normal) ---
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
        this.driftVx = -(0.5 + Math.random() * 0.5); // Slow Left
        
        this.phase = Math.random() * Math.PI * 2;
        this.swirlRange = 15 + Math.random() * 30; 
        
        const nx = this.tx / w; 
        this.arrivalDuration = 1500 + (nx * 1000); 
      }

      update(time, elapsedFormation) {
        let targetSize = this.driftSize;
        
        if (currentState === STATE.WAITING) {
            // Infinite Drift
            this.x += this.driftVx;
            this.y += Math.sin(time * 0.001 + this.phase) * 0.5;
            
            // --- REPULSION FROM TEXT (Loading...) ---
            const cx = width / 2;
            const cy = height / 2;
            const dx = this.x - cx;
            const dy = this.y - cy;
            const dist = Math.sqrt(dx*dx + dy*dy);
            const repelRadius = 130; 
            
            if (dist < repelRadius) {
               const force = (repelRadius - dist) / repelRadius;
               const angle = Math.atan2(dy, dx);
               this.x += Math.cos(angle) * force * 5; 
               this.y += Math.sin(angle) * force * 5;
            }
            
            if (this.x < 0) this.x = width;
            targetSize = this.driftSize;
            
        } else if (currentState === STATE.FORMING) {
            targetSize = this.formationSize; 
            const crystallizeStart = 3500; 
            
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
               const p = (elapsedFormation - crystallizeStart) / (5000 - crystallizeStart);
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
      checkServer();
    }

    function checkServer() {
        if (currentState !== STATE.WAITING) return;
        
        // PING STREAMLIT HEALTHZ
        fetch('http://localhost:8501/_stcore/health')
        .then(res => {
            if (res.ok) {
                console.log("Streamlit ready! Starting formation.");
                currentState = STATE.FORMING;
                formationStartTime = performance.now();
                const lbl = document.getElementById('loading-label');
                if(lbl) lbl.style.opacity = '0';
            } else {
                setTimeout(checkServer, 500);
            }
        })
        .catch(() => {
            setTimeout(checkServer, 500);
        });
    }

    function animate(timestamp) {
      if (!formationStartTime && currentState === STATE.FORMING) formationStartTime = timestamp;
      const elapsedFormation = currentState === STATE.FORMING ? (timestamp - formationStartTime) : 0;
      
      ctx.clearRect(0, 0, width, height);
      if (particles.length > 0) {
        for (let i = 0; i < particles.length; i++) {
          particles[i].update(timestamp, elapsedFormation);
          particles[i].draw(ctx);
        }
      }
      
      if (currentState === STATE.FORMING) {
         if (elapsedFormation > 4200) {
             document.body.classList.add('cross-fade');
         }
         if (elapsedFormation > 5500) {
             // REDIRECT TO STREAMLIT
             window.location.replace("http://localhost:8501");
             return; 
         }
      }
      requestAnimationFrame(animate);
    }
  </script>
</body>
</html>
"""

# 2. Write loading.html to CWD
loading_path = Path("loading.html").resolve()
with open(loading_path, "w", encoding="utf-8") as f:
    f.write(LOADING_HTML)

print(f"Opening loader: {loading_path.as_uri()}")

# 3. Open Browser
def open_browser():
    time.sleep(1) # Give it a split second
    webbrowser.open(loading_path.as_uri())

threading.Thread(target=open_browser).start()

# 4. Start Streamlit (in this process or subprocess)
# Since Streamlit needs to take over main thread usually, or be run as subprocess.
# The cleanest way for a launcher script is to call `streamlit run` as a subprocess and wait.
# We assume this script is run via python.

print("Starting Streamlit Server on port 8501...")
try:
    cmd = ["streamlit", "run", "code/streamlit_app.py", "--server.port=8501", "--server.headless=true"]
    subprocess.run(cmd)
except KeyboardInterrupt:
    pass
