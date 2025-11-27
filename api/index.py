import sys
import os

# Get the parent directory (project root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Change working directory to project root for template resolution
os.chdir(parent_dir)

# Import Flask app
from app import app as flask_app

# Vercel Python runtime handler
# Export the Flask WSGI application directly
handler = flask_app

