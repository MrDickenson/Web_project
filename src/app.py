from flask import Flask
from src.api.routes import api_bp
from src.service.db import init_db

app = Flask(__name__)
app.register_blueprint(api_bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, port=3000)