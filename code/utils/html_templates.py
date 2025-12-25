
# This file contains large HTML templates used in the Streamlit application.

LOADING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
  <style>
    body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); font-family: 'Inter', sans-serif; }
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

    /* Fluid Background Animation */
    .fluid-shape {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.4;
        animation: fluid-move 14s infinite ease-in-out;
        will-change: transform;
        mix-blend-mode: multiply;
        z-index: 0;
    }
    .shape-1 { background: #7dd3fc; width: 65vw; height: 65vw; top: -15%; left: -10%; animation-duration: 16s; }
    .shape-2 { background: #bae6fd; width: 70vw; height: 70vw; top: 25%; right: -25%; animation-duration: 20s; animation-delay: -4s; }
    .shape-3 { background: #a5f3fc; width: 55vw; height: 55vw; bottom: -15%; left: 15%; animation-duration: 14s; animation-delay: -8s; }
    @keyframes fluid-move {
        0% { transform: translate(0, 0) scale(1) rotate(0deg); }
        33% { transform: translate(45px, 65px) scale(1.1) rotate(8deg); }
        66% { transform: translate(-35px, 25px) scale(0.9) rotate(-6deg); }
        100% { transform: translate(0, 0) scale(1) rotate(0deg); }
    }
  </style>
</head>
<body>
    <div class="fluid-shape shape-1"></div>
    <div class="fluid-shape shape-2"></div>
    <div class="fluid-shape shape-3"></div>
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
