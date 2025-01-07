from flask import Flask, request, jsonify
import sqlite3
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(filename='weather_data.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            password TEXT,
            dateutc TEXT,
            winddir INTEGER,
            windspeedmph INTEGER,
            windgustmph INTEGER,
            tempf INTEGER,
            rainin REAL,
            baromin REAL,
            dewptf REAL,
            humidity INTEGER,
            weather TEXT,
            clouds TEXT,
            softwaretype TEXT,
            action TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO weather_data (user_id, password, dateutc, winddir, windspeedmph, windgustmph, tempf, rainin, baromin, dewptf, humidity, weather, clouds, softwaretype, action, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def updateraw():
    user_id = request.args.get('ID')
    password = request.args.get('PASSWORD')
    dateutc = request.args.get('dateutc')
    winddir = request.args.get('winddir')
    windspeedmph = request.args.get('windspeedmph')
    windgustmph = request.args.get('windgustmph')
    tempf = request.args.get('tempf')
    rainin = request.args.get('rainin')
    baromin = request.args.get('baromin')
    dewptf = request.args.get('dewptf')
    humidity = request.args.get('humidity')
    weather = request.args.get('weather', '')
    clouds = request.args.get('clouds', '')
    softwaretype = request.args.get('softwaretype')
    action = request.args.get('action')

    log_message = f"Received request from {user_id} at {datetime.now()}. Parameters: {request.args}"
    logging.info(log_message)

    data = (
        user_id, password, dateutc, winddir, windspeedmph, windgustmph, tempf, rainin,
        baromin, dewptf, humidity, weather, clouds, softwaretype, action, datetime.now()
    )
    insert_data(data)

    return jsonify({'message': 'Data successfully updated'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
