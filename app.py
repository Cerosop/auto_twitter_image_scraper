import configparser
import mysql.connector
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)
static_folder = 'static'
image_folders = 'images'
id_map = {}

# 讀取配置文件
config = configparser.ConfigParser()
config.read('config.conf')

# 獲取數據庫連接配置
db_config = {
    'user': config['DATABASE']['user'],
    'password': config['DATABASE']['password'],
    'host': config['DATABASE']['host'],
    'database': config['DATABASE']['database']
}

# 連接到 MySQL 數據庫
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 插入數據
sql = "select * from graph"
cursor.execute(sql)

result = cursor.fetchall()
for row in result:
    id_map[str(row[0])] = (row[1], True if row[2] == 1 else False)

# 關閉連接
cursor.close()
conn.close()


@app.route('/')
def index():
    images_folder = os.listdir(os.path.join(static_folder, image_folders, "high"))
    images = {}
    for i in images_folder:
        images[i] = os.listdir(os.path.join(static_folder, image_folders, "high", i))

    return render_template('index.html', folder=image_folders, images=images, id_map=id_map, keys=reversed(images.keys()))


@app.route('/download')
def download():
    folder_name = request.args.get('folder_name')
    image_name = request.args.get('image_name')
    return send_file(os.path.join(static_folder, image_folders, 'high', folder_name, image_name), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

