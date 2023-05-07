from flask import Flask, g, render_template, send_file, redirect, url_for
from crontab import CronTab
from os import getlogin
from subprocess import run
from socket import gethostname
import sqlite3
import csv
import controller

CSV_PATH = '/home/controller/data.csv'
IMAGE_PATH = '/home/controller/controller/static/image.jpg'

app = Flask(__name__)

@app.route('/')
def index():
    job, _ = get_logging_job()
    wifi_quality, wifi_strength = get_connection_strength()
    version = get_version_hash()
    date_time, temperature, pressure, humidity, light = controller.read_data()

    rows = query_database('SELECT * FROM measurements ORDER BY "date time" DESC LIMIT 20')

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
        version = version)

def get_connection_strength():
    link_start = 'Link Quality='
    link_end = '/70'
    signal_start = 'Signal level='
    signal_end   = ' dBm'

    result = run(['iwconfig','wlan0'], text=True, capture_output=True)

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
    cron = CronTab(user=getlogin())
    for job in cron.find_command('controller.py -w'):
        return job, cron

def get_version_hash():
    result = run(['git', 'rev-parse', '--short', 'main'], cwd='/home/controller/controller', text=True, capture_output=True)
    return result.stdout

def get_database() -> sqlite3.Connection:
    database = getattr(g, '_database', None) 
    if database is None:
        database = g._database = sqlite3.connect(controller.DATABASE_PATH)
        database.row_factory = sqlite3.Row
    return database

def init_database():
    with app.app_context():
        database = get_database()
        with app.open_resource(controller.DATABASE_SCHEMA_PATH, mode='r') as file:
            database.cursor().executescript(file.read())
        database.commit()

def execute_database(query, args=()):
    cursor = get_database()
    cursor.execute(query, args)
    cursor.commit()

def query_database(query, args=(), one=False, names=False):
    cursor = get_database().execute(query, args)
    rows = cursor.fetchall()
    if names:
        names = [name[0] for name in cursor.description]
        rows.insert(0, names)
    cursor.close()
    return (rows[0] if rows else None) if one else rows

@app.cli.command('initdb')
def init_database_command():
    init_database()
    print("Initalised the database")

@app.route('/logging_ability')
def change_logging_ability():
    job, cron = get_logging_job()
    if job.is_enabled():
        job.enable(False)
    else:
        job.enable()
    cron.write()
    return redirect(url_for('index'))

@app.route('/download_data') #TODO Stream file rather than create an intermediate file & add header to CSV
def download_data():
        rows = query_database('SELECT * FROM measurements', names=True)
        with open(CSV_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return send_file(CSV_PATH, mimetype='text/csv', as_attachment=True, max_age=0)

@app.route('/delete_data')
def delete_data():
    execute_database('DELETE FROM measurements')
    return redirect(url_for('index'))

@app.route('/log_data')
def log_data():
    controller.write_data(controller.read_data(), mode='m')
    return redirect(url_for('index'))

@app.route('/capture_image')
def capture_image():
    run(['raspistill', '-o', IMAGE_PATH])
    return redirect(url_for('index'))

@app.route('/delete_image')
def delete_image():
    run(['rm', IMAGE_PATH])
    return redirect(url_for('index'))

@app.route('/reboot_controller')
def reboot_controller():
    run(["sudo", "shutdown", "-r", "1"])
    return redirect(url_for('index'))

@app.route('/update_controller')
def update_controller():
    run(["git", "pull"], cwd="/home/controller/controller")
    return redirect(url_for('index'))

@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()
    
    