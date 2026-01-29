import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """
    Extract clean text from any URL using Jina AI Reader
    This is way better than parsing raw HTML ourselves
    Jina automatically removes ads, menus, etc and returns clean markdown
    """
    try:
        # Special handling for Wikipedia - Jina AI is too aggressive
        if 'wikipedia.org' in url:
            response = requests.get(url, timeout=30)
            return extract_text_from_html(response.text)
        
        # Jina's free service that converts any URL to clean text
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, timeout=60)  # Increased timeout for slow servers
        
        if response.status_code == 200:
            return response.text
        else:
            # if Jina fails, fall back to basic HTML parsing
            fallback_response = requests.get(url, timeout=30)
            return extract_text_from_html(fallback_response.text)
    except requests.Timeout:
        raise Exception(f"Request timed out while fetching {url}. The server might be slow or unresponsive.")
    except requests.RequestException as e:
        raise Exception(f"Network error while fetching {url}: {str(e)}")
    except Exception as e:
        # Last resort fallback
        try:
            fallback_response = requests.get(url, timeout=30)
            return extract_text_from_html(fallback_response.text)
        except:
            raise Exception(f"Failed to extract content from {url}: {str(e)}")



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
