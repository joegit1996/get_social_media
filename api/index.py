import sys
import os

# Get the parent directory (project root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to Python path
sys.path.insert(0, parent_dir)

# Change working directory to project root for template resolution
os.chdir(parent_dir)

# Import Flask app
from app import app

# Export handler - Vercel expects this name
handler = app

