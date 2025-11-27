from flask import Flask

# Create a minimal Flask app for testing
test_app = Flask(__name__)

@test_app.route('/')
def hello():
    return {'status': 'ok', 'message': 'Flask is working'}

@test_app.route('/api/test')
def test():
    return {'status': 'ok', 'test': 'success'}

# Export handler
handler = test_app

