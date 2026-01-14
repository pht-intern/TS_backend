"""
Cache busting utilities for static files
"""
import os
import re
from pathlib import Path


def get_versioned_url(file_path: str, file_type: str, frontend_dir: Path) -> str:
    """
    Generate a versioned URL for a static file based on its modification time.
    This enables cache busting while allowing aggressive caching.
    
    Args:
        file_path: Path to the file relative to the css/js directory
        file_type: Either "css" or "js"
        frontend_dir: Path to the frontend directory
    
    Returns:
        URL with version parameter, e.g., "/css/style.css?v=1705140123"
    """
    try:
        if file_type == "css":
            full_path = frontend_dir / "css" / file_path
        elif file_type == "js":
            full_path = frontend_dir / "js" / file_path
        else:
            return f"/{file_type}/{file_path}"
        
        if full_path.exists() and full_path.is_file():
            version = int(os.stat(str(full_path)).st_mtime)
            return f"/{file_type}/{file_path}?v={version}"
        else:
            # File doesn't exist, return URL without version
            return f"/{file_type}/{file_path}"
    except Exception as e:
        print(f"Error generating versioned URL for {file_type}/{file_path}: {str(e)}")
        return f"/{file_type}/{file_path}"


def inject_versioned_urls(html_content: str, frontend_dir: Path) -> str:
    """
    Inject version parameters into CSS and JS file references in HTML content.
    This enables automatic cache busting for static HTML files.
    """
    # Pattern to match CSS links: href="/css/filename.css" or href='/css/filename.css'
    css_pattern = r'(href=["\'])(/css/([^"\']+\.css))(["\'])'
    
    def css_replacer(match):
        quote_start = match.group(1)
        file_path = match.group(3)
        quote_end = match.group(4)
        versioned_url = get_versioned_url(file_path, "css", frontend_dir)
        return f'{quote_start}{versioned_url}{quote_end}'
    
    html_content = re.sub(css_pattern, css_replacer, html_content)
    
    # Pattern to match JS scripts: src="/js/filename.js" or src='/js/filename.js'
    js_pattern = r'(src=["\'])(/js/([^"\']+\.js))(["\'])'
    
    def js_replacer(match):
        quote_start = match.group(1)
        file_path = match.group(3)
        quote_end = match.group(4)
        versioned_url = get_versioned_url(file_path, "js", frontend_dir)
        return f'{quote_start}{versioned_url}{quote_end}'
    
    html_content = re.sub(js_pattern, js_replacer, html_content)
    
    return html_content
