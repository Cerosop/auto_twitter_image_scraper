import configparser
from datetime import datetime, timedelta
import os
import mysql.connector

def store2db(artist, is_retweet, debug):
    # 讀取配置文件
    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config.read(os.path.join(current_dir, 'config.conf'))

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
    sql = "INSERT INTO graph (artist, is_retweet) VALUES (%s, %s)"
    val = (artist, is_retweet)
    cursor.execute(sql, val)

    # 提交更改
    conn.commit()

    # if debug:
    #     # 顯示插入的數據
    #     cursor.execute("SELECT * FROM graph")
    #     result = cursor.fetchall()
    #     for row in result:
    #         print(row)

    last_id = cursor.lastrowid
    # 關閉連接
    cursor.close()
    conn.close()
    return last_id

def deletedb(day, debug=False):
    # 讀取配置文件
    config = configparser.ConfigParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config.read(os.path.join(current_dir, 'config.conf'))

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
    if day == -1:
        sql = "DELETE FROM graph WHERE download_time < %s AND download_time > %s"
        val = (datetime.today().date() - timedelta(-1), datetime.today().date())
    else:
        sql = "DELETE FROM graph WHERE download_time < %s"
        val = (datetime.today().date() - timedelta(days=day - 1),)
    cursor.execute(sql, val)

    # 提交更改
    conn.commit()

    # if debug:
    #     # 顯示插入的數據
    #     cursor.execute("SELECT * FROM graph")
    #     result = cursor.fetchall()
    #     for row in result:
    #         print(row)

    # 關閉連接
    cursor.close()
    conn.close()