import os
from flask import Flask

# Get the port number from the environment variable or use a default value of 5000
port = int(os.environ.get('PORT', 5000))

# Create a Flask app
app = Flask(__name__)

# Define a route and handler for the root URL
@app.route('/')
def hello():
    return f'Hello, World! Running on port {port}'

# Start the Flask app on the specified port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
