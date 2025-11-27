import sys
import os

try:
    # Get the parent directory (project root)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Add parent directory to Python path
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Change working directory to project root for template resolution
    os.chdir(parent_dir)
    
    # Import Flask app
    from app import app
    
    # Vercel Python runtime expects 'handler' to be the WSGI application
    # Flask app is already a WSGI application, so we can use it directly
    handler = app
    
except Exception as e:
    # If there's an import error, create a simple error handler
    def handler(request):
        return {
            'statusCode': 500,
            'body': f'Import error: {str(e)}'
        }

