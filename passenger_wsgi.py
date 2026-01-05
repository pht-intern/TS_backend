"""
Passenger WSGI entry point for cPanel deployment

IMPORTANT: This file must be kept in Backend/ directory for Passenger to work.
Do not modify the structure or indentation of this file.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Get project root directory (parent of Backend directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Find Backend directory (case-insensitive)
BACKEND_DIR = None
for dir_name in ["Backend", "backend"]:
    potential_dir = PROJECT_ROOT / dir_name
    if potential_dir.exists() and potential_dir.is_dir():
        BACKEND_DIR = potential_dir
        break

if BACKEND_DIR is None:
    BACKEND_DIR = PROJECT_ROOT / "Backend"

# Load environment variables
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

# Configure Python path
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Set working directory
os.chdir(str(BACKEND_DIR))

# Import WSGI application from app.py
# The 'application' variable is defined at the end of app.py
# This is a Flask WSGI application (native WSGI, no wrapper needed)
#
# CRITICAL: DO NOT use the old method:
#   ❌ wsgi = imp.load_source('wsgi', 'wsgi.py')  # OBSOLETE - causes ImportError
#   ❌ from wsgi import application  # OBSOLETE - wsgi.py should not exist
#
# The correct method (current):
#   ✅ from app import application  # Direct Flask import (native WSGI)
#
# Note: Flask is native WSGI, so no ASGI wrapper (AsgiToWsgi) is needed or should be used.
from app import application
