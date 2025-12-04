import os
from flask import Flask
from src.api.routes import api_bp
from src.service.db import init_db

current_file_path = os.path.abspath(__file__)
src_directory = os.path.dirname(current_file_path)
project_root = os.path.dirname(src_directory)
template_dir = os.path.join(project_root, 'templates')

print(f"--- DEBUG INFO ---")
print(f"Запущено файл: {current_file_path}")
print(f"Шукаю шаблони в папці: {template_dir}")
print(f"Чи існує ця папка? {os.path.exists(template_dir)}")
if os.path.exists(template_dir):
    print(f"Файли всередині: {os.listdir(template_dir)}")
else:
    print("!!! ПОМИЛКА: Папка templates не знайдена за цим шляхом !!!")
print(f"------------------")

app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(api_bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')