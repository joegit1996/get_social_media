def handler(request):
    """Vercel serverless function handler"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status": "ok", "message": "Handler function works"}'
    }

