import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def fetch_saica_framework(urls):
    """
    Fetches and extracts text from the provided SAICA website URLs.
    
    Args:
        urls (list): List of URL strings.
        
    Returns:
        dict: A dictionary where key is URL and value is extracted text.
    """
    content = {}
    for url in urls:
        try:
            logger.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Simple extraction: all paragraph text
                # We can refine this to target specific divs if needed
                text = soup.get_text(separator=' ', strip=True)
                content[url] = text
            else:
                logger.warning(f"Failed to fetch {url}: Status {response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            
    return content
