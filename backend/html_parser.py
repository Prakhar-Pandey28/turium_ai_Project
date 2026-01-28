import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """
    Extract clean text from any URL using Jina AI Reader
    This is way better than parsing raw HTML ourselves
    Jina automatically removes ads, menus, etc and returns clean markdown
    """
    try:
        # Jina's free service that converts any URL to clean text
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, timeout=30)
        
        if response.status_code == 200:
            return response.text
        else:
            # if Jina fails, fall back to basic HTML parsing
            return extract_text_from_html(requests.get(url).text)
    except:
        # fallback in case of any errors
        return extract_text_from_html(requests.get(url).text)

def extract_text_from_html(html_content):
    """Backup method - basic HTML to text conversion"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # remove scripts, styles, navigation
    for script in soup(["script", "style", "nav", "header", "footer"]):
        script.decompose()
    
    text = soup.get_text()
    
    # clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text
