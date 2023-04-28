from flask import Flask, g, render_template, send_file, redirect, url_for
from crontab import CronTab
from os import getlogin
from subprocess import run
from socket import gethostname
import controller
import sqlite3
import csv

VERSION = "0.1.0"
CSV_FILE_PATH = '/home/controller/data.csv'

app = Flask(__name__)

# Main page.
@app.route('/')
def index():
    job, _ = get_logging_job()
    wifi_quality, wifi_strength = get_connection_strength()
    date_time, temperature, pressure, humidity, light = controller.measure_data()

    rows = query_database('SELECT * FROM measurements ORDER BY datetime DESC LIMIT 20')

    time_data = []
    temperature_data = []
    pressure_data = []
    humidity_data = []
    light_data = []

    for row in rows:
        time_data.insert(0, row[0][11:16])
        temperature_data.insert(0, row[1])
        pressure_data.insert(0, row[2])
        humidity_data.insert(0, row[3])
        light_data.insert(0, row[4])

    return render_template(
        'index.html',
        date_time = date_time,
        temperature = temperature,
        pressure = pressure,
        humidity = humidity,
        light = light,
        time_data = time_data,
        temperature_data = temperature_data,
        pressure_data = pressure_data,
        humidity_data = humidity_data,
        light_data = light_data,
        logging_ability = job.is_enabled(),
        wifi_quality = wifi_quality,
        wifi_strength = wifi_strength,
        hostname = gethostname(),
        version = VERSION)

def get_connection_strength():
    link_start = "Link Quality="
    link_end = "/70"
    signal_start = "Signal level="
    signal_end   = " dBm"

    result = run(["iwconfig","wlan0"], text=True, capture_output=True)

    link_index_start = result.stdout.find(link_start)
    link_index_end = result.stdout.find(link_end, link_index_start)
    signal_index_start = result.stdout.find(signal_start)
    signal_index_end = result.stdout.find(signal_end, signal_index_start)

    index_link_start = link_index_start+len(link_start)
    index_link_end = link_index_end
    index_signal_start = signal_index_start+len(signal_start)
    index_signal_end = signal_index_end

    return(int(result.stdout[index_link_start:index_link_end]), int(result.stdout[index_signal_start:index_signal_end]))

def get_logging_job():
    cron = CronTab(user = getlogin())

    for job in cron.find_command('controller.py -w'):
        return job, cron

def get_database() -> sqlite3.Connection:
    database = getattr(g, '_database', None) 
    if database is None:
        database = g._database = sqlite3.connect(controller.DATABASE_PATH)
        database.row_factory = sqlite3.Row
    return database

def query_database(query, args=(), one=False):
    cursor = get_database().execute(query, args)
    rows = cursor.fetchall()
    cursor.close()
    return (rows[0] if rows else None) if one else rows

def database_to_csv():
    column_names = query_database('SELECT name FROM PRAGMA_TABLE_INFO(\'measurements\')')

    for name in column_names:
        print(name)

    
    rows = query_database('SELECT * FROM measurements')
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

@app.route('/download_data')
def download_data():
    database_to_csv()
    return send_file(CSV_FILE_PATH, as_attachment=True)

@app.route('/delete_data')
def delete_data():
    connection = sqlite3.connect(controller.DATABASE_PATH)
    connection.execute('DROP TABLE IF EXISTS ?;', (controller.DATABASE))
    connection.close()

    return redirect(url_for('index'))

@app.route('/logging_ability')
def change_logging_ability():
    job, cron = get_logging_job()

    if job.is_enabled():
        job.enable(False)
    else:
        job.enable()

    cron.write()

    return redirect(url_for('index'))

@app.route('/light_on')
def light_on():
    controller.light_on()

    return redirect(url_for('index'))

@app.route('/light_off')
def light_off():
    controller.light_off()

    return redirect(url_for('index'))

@app.route('/reboot_controller')
def reboot_controller():
    run(["sudo", "shutdown", "-r", "1"])

    return redirect(url_for('index'))

@app.route('/update_controller')
def update_controller():
    result = run(["git", "pull"], cwd="/home/controller/controller", text=True, capture_output=True)

    return redirect(url_for('index'))

@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')