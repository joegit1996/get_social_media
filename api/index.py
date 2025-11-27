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

# Use vercel-python-wsgi adapter for proper Flask handling on Vercel
try:
    from vercel_python_wsgi import VercelWSGI
    handler = VercelWSGI(app)
except ImportError:
    # Fallback: use app directly if vercel-python-wsgi is not available
    handler = app

