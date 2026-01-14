"""
Configuration module for shared paths and settings
This ensures consistent path handling across the application
"""
from pathlib import Path
import os

# Get project root directory (parent of backend directory)
# This works whether we're in backend/ or backend/routes/ or backend/utils/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Get backend directory
BACKEND_DIR = Path(__file__).resolve().parent

# Find frontend directory (case-insensitive)
FRONTEND_DIR = None
for dir_name in ["frontend", "Frontend", "FRONTEND"]:
    potential_dir = PROJECT_ROOT / dir_name
    if potential_dir.exists() and potential_dir.is_dir():
        FRONTEND_DIR = potential_dir
        break

if FRONTEND_DIR is None:
    FRONTEND_DIR = PROJECT_ROOT / "frontend"
    if not FRONTEND_DIR.exists():
        print(f"WARNING: Frontend directory not found at {FRONTEND_DIR}. Static file serving may be limited.")
    else:
        print(f"INFO: Using frontend directory: {FRONTEND_DIR}")

# Images directory (relative to project root for cPanel compatibility)
# In production, images are typically stored in a public directory
# Check if images exist in frontend/images (old structure) or project root/images (new structure)
IMAGES_DIR = None
if FRONTEND_DIR and (FRONTEND_DIR / "images").exists():
    # Use frontend/images structure (matches old app.py.backup)
    IMAGES_DIR = FRONTEND_DIR / "images"
elif (PROJECT_ROOT / "images").exists():
    IMAGES_DIR = PROJECT_ROOT / "images"
else:
    # Default to frontend/images if frontend exists, otherwise project root/images
    if FRONTEND_DIR and FRONTEND_DIR.exists():
        IMAGES_DIR = FRONTEND_DIR / "images"
    else:
        IMAGES_DIR = PROJECT_ROOT / "images"
    # Create it if it doesn't exist
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Get environment file path
ENV_FILE = PROJECT_ROOT / ".env"

# Export paths for use in other modules
__all__ = [
    'PROJECT_ROOT',
    'BACKEND_DIR',
    'FRONTEND_DIR',
    'IMAGES_DIR',
    'ENV_FILE'
]
