# Vercel Deployment Troubleshooting

## Current Issue: FUNCTION_INVOCATION_FAILED

If you're seeing this error, check the following:

### 1. Check Vercel Function Logs

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your project: `get-social-media`
3. Go to **Deployments** → Click on the latest deployment
4. Go to **Functions** tab
5. Click on `api/index.py`
6. Check the **Logs** section for the actual error message

Common errors you might see:
- `ModuleNotFoundError` - Missing dependency
- `ImportError` - Import path issue
- `TemplateNotFound` - Template path issue
- `AttributeError` - Handler format issue

### 2. Verify Requirements.txt

Make sure `requirements.txt` has all dependencies:
```
Flask==3.1.2
Flask-CORS==6.0.1
requests==2.32.5
python-dotenv==1.2.1
```

### 3. Check Python Version

Vercel uses Python 3.9 by default. If you need a specific version, create `runtime.txt`:
```
python-3.9
```

### 4. Verify File Structure

Ensure your project has:
```
.
├── api/
│   └── index.py          # Must exist
├── templates/
│   └── index.html        # Must exist
├── app.py                # Must exist
├── vercel.json           # Must exist
└── requirements.txt      # Must exist
```

### 5. Test Handler Locally

You can test the handler locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Test the import
python -c "import sys; sys.path.insert(0, '.'); from api.index import handler; print('OK')"
```

### 6. Alternative Handler Format

If the current handler doesn't work, try this alternative in `api/index.py`:

```python
from vercel_python_wsgi import VercelWSGI
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
os.chdir(parent_dir)

from app import app

handler = VercelWSGI(app)
```

But first, you'd need to add to `requirements.txt`:
```
vercel-python-wsgi
```

### 7. Check Environment Variables

Make sure environment variables are set correctly in Vercel dashboard:
- Go to **Settings** → **Environment Variables**
- Verify `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` are set (if using)

### 8. Common Fixes

**If you see "ModuleNotFoundError: No module named 'app'":**
- The path resolution might be wrong
- Check that `app.py` is in the root directory

**If you see "TemplateNotFound":**
- Verify `templates/` directory exists
- Check that `template_folder='templates'` is set in Flask app

**If you see "Handler not found":**
- Ensure `handler = app` is at the end of `api/index.py`
- Verify the file is named exactly `index.py` (not `Index.py`)

## Next Steps

1. **Check the logs** in Vercel dashboard to see the exact error
2. **Share the error message** so we can provide a targeted fix
3. **Try redeploying** after any fixes

## Quick Test After Fix

Once deployed, test with:
```bash
curl "https://get-social-media.vercel.app/api/find?business_name=Apple&country=USA"
```

