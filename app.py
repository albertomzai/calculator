import os
from backend.app import app

if __name__ == '__main__':
    # Use environment variable to set port if needed
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)