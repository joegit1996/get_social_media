import sys
import os

# Add parent directory to path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Change to parent directory to ensure templates can be found
os.chdir(parent_dir)

from app import app

# Vercel expects the handler to be named 'handler'
# Flask app works directly as a WSGI application
handler = app

