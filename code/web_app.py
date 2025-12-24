from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import uvicorn
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

# Easter Egg: Creator Signature
print("   _____          _____ _____          _____                 _ _           ")
print("  / ____|   /\\   |_   _/ ____|   /\\   / ____|               (_) |          ")
print(" | (___    /  \\    | || |       /  \\ | (___   ___ _ __ _ __ _| |__   ___   ")
print("  \\___ \\  / /\\ \\   | || |      / /\\ \\ \\___ \\ / __| '__| '__| | '_ \\ / _ \\  ")
print("  ____) |/ ____ \\ _| || |____ / ____ \\____) | (__| |  | |  | | |_) |  __/  ")
print(" |_____/_/    \\_\\_____\\_____/_/    \\_\\_____/ \\___|_|  |_|  |_|_.__/ \\___|  ")
print("                                                         Made by Adhir Singh")

from ingestion.framework_loader import load_saica_framework
from analysis.mapper import map_activity_to_competency
from reporting.generator import generate_markdown_content
from config import GOOGLE_API_KEY, GROQ_API_KEY, LLM_PROVIDER, save_keys

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SAICA_Web")

app = FastAPI(title="SAICA Scribe UI")

# Templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Global Framework Data (Lazy Load)
framework_data = None

def has_valid_keys():
    """Checks if at least one API key is configured."""
    # Reload env to be sure
    load_dotenv()
    google = os.getenv("GOOGLE_API_KEY")
    groq = os.getenv("GROQ_API_KEY")
    github = os.getenv("GITHUB_TOKEN")
    return bool(google or groq or github)

@app.on_event("startup")
async def startup_event():
    global framework_data
    logger.info("Initializing... Made by Adhir Singh")
    if has_valid_keys():
        logger.info("Keys found. Loading framework data...")
        framework_data = load_saica_framework()
        logger.info("Framework data loaded.")
    else:
        logger.warning("No API keys found. Waiting for user setup.")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if not has_valid_keys():
        return RedirectResponse(url="/setup")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/setup", response_class=HTMLResponse)
async def setup_page(request: Request):
    if has_valid_keys():
        return RedirectResponse(url="/")
    return templates.TemplateResponse("setup.html", {"request": request})

@app.get("/guide", response_class=HTMLResponse)
async def guide_page(request: Request):
    return templates.TemplateResponse("guide.html", {"request": request})

@app.get("/api/status")
async def get_status():
    """Returns the current provider status."""
    load_dotenv()
    return {
        "google_configured": bool(os.getenv("GOOGLE_API_KEY")),
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "github_configured": bool(os.getenv("GITHUB_TOKEN")),
        "current_provider": os.getenv("LLM_PROVIDER", "gemini")
    }

@app.post("/api/settings")
async def update_settings(
    google_key: str = Form(None),
    groq_key: str = Form(None),
    github_key: str = Form(None),
    github_model: str = Form(None),
    provider: str = Form(None)
):
    """Updates API keys and provider settings."""
    try:
        save_keys(
            google_key=google_key, 
            groq_key=groq_key, 
            github_key=github_key,
            provider=provider,
            github_model=github_model
        )
        load_dotenv(override=True) # Force reload of new keys
        
        # Reload framework data if this was first setup
        global framework_data
        if not framework_data:
             # Reload config vars into memory for specific modules if needed
             # (Though os.getenv is used directly in config.py, mapper imports it)
             # Ideally we restart, but reloading data is a good step.
             # Note: mapper.py imports GOOGLE_API_KEY from config. 
             # We might need to handle hot-reloading of those vars or just restart.
             # For now, we will rely on os.getenv in mapper via a small tweak or just accept it.
             # Actually, best practice is to have mapper read os.getenv at runtime or reload config.
             pass 

        return JSONResponse({"status": "success", "message": "Settings saved."})
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.post("/api/map")
async def map_competencies(
    activity: str = Form(...),
    provider: str = Form("gemini")
):
    global framework_data
    
    # Ensure keys are loaded (hot fix for mapper import)
    # Since mapper imports from config, and config reads env at top level,
    # we might need to tell mapper to re-read or pass keys explicitly.
    # The refactored mapper inputs from config. 
    # Let's trust python-dotenv re-read or just reload framework data if null.
    
    if not framework_data:
        # Load now that keys might exist
        framework_data = load_saica_framework()
        
    logger.info(f"Mapping request via {provider}: {activity[:50]}...")
    
    # Pass provider explicitly to handle logic switch
    mappings = map_activity_to_competency(activity, framework_data, provider=provider)
    report_md = generate_markdown_content(mappings)
    
    return {
        "mappings": mappings,
        "markdown_report": report_md
    }

if __name__ == "__main__":
    uvicorn.run("web_app:app", host="127.0.0.1", port=8000, reload=True)
