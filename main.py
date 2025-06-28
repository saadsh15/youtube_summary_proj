from flask import Flask
from app import app as flask_app

if __name__ == "__main__":
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
