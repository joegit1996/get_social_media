import sys
import os

# Get the parent directory (project root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Change working directory to project root for template resolution
os.chdir(parent_dir)

# Import Flask app - ensure it's fully initialized
from app import app as flask_app

# Verify the app is a Flask instance before exporting
# Vercel Python runtime expects 'handler' to be the WSGI application
if hasattr(flask_app, '__call__'):
    handler = flask_app
else:
    # Fallback: create a simple handler
    def handler(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'Flask app initialization error']

