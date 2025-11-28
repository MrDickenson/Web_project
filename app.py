from flask import Flask, jsonify, render_template
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

db.init_db()


# НОВИЙ МАРШРУТ: Віддає головну сторінку
@app.route('/')
def index():
    return render_template('index.html')


# API МАРШРУТ: Віддає дані
@app.route('/items', methods=['GET'])
def get_items():
    conn = db.get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()

    items_list = [dict(item) for item in items]
    return jsonify({"status": "success", "data": items_list})


if __name__ == '__main__':
    app.run(port=3000, debug=True)