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
from app import app

# Create a WSGI handler function for Vercel
def handler(request, response):
    """Vercel serverless function handler"""
    return app(request.environ, response.start_response)

# Also export app directly as fallback
__all__ = ['handler', 'app']

