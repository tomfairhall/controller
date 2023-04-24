from flask import Flask, render_template, send_file, redirect, url_for
from crontab import CronTab, CronItem
from os import getlogin, remove, path
from subprocess import run
from socket import gethostname
from datetime import datetime
from controller import measure_data, DATA_FILE_PATH, leds_on, leds_off
from csv import DictReader

app = Flask(__name__)

VERSION = "0.1.0"

date_time = temp_C = pres_HPa = hum_RH = light_Lx = 0
date_times = temp_Cs = pres_HPas = hum_RHs = light_LXs = []
debug_output = ""

# Main page.
@app.route('/')
def index():

    job, _ = find_logging_job()
    wifi_quality, wifi_strength = find_connection_strength()

    return render_template(
        'index.html',
        date_time = date_time,
        temperature = temp_C,
        pressure = pres_HPa,
        humidity = hum_RH,
        lux = light_Lx,
        times = date_times,
        temp_Cs = temp_Cs,
        pres_HPas = pres_HPas,
        hum_RHs = hum_RHs,
        light_LXs = light_LXs,
        logging_ability = job.is_enabled(),
        file_exists = find_data_file(),
        wifi_quality = wifi_quality,
        wifi_strength = wifi_strength,
        hostname = gethostname(),
        version = VERSION,
        debug_output = debug_output)

# Debug message handler #TODO Make this encapsulated with classes to avoid global varables?
def debug(message):
    global debug_output
    date_time = datetime.now().strftime("%H:%M:%S")

    debug_output = date_time + " " + message

# Check that data file exists.
def find_data_file(file_path = DATA_FILE_PATH):
    return path.exists(file_path)

def find_data_measurements(num = 12):
    if find_data_file():
        global date_times
        global temp_Cs
        global pres_HPas
        global hum_RHs
        global light_LXs

        date_times = temp_Cs = pres_HPas = hum_RHs = light_LXs = []

        with open(DATA_FILE_PATH, newline='') as file:
            reader = DictReader(file)
            for row in reader[-1:(-1*num)]:
                date_times.append(row['Date-Time'])
                temp_Cs.append(row['Temperature (°C)'])
                pres_HPas.append(row['Pressure (HPa)'])
                hum_RHs.append(row['Humidity (RH)'])
                light_LXs.append(row['Lux (lx)'])

# Check current WiFi connection strength.
def find_connection_strength():
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

# Find the data logging function.
def find_logging_job():
    cron = CronTab(user = getlogin())

    for job in cron.find_command('controller.py -w'):
        return job, cron

# If request data button is clicked, the data will be measured and displayed.
@app.route('/request_data')
def request_data():

    global date_time
    global temp_C_ave
    global pres_HPa_ave
    global hum_RH_ave
    global light_Lx_ave
    global date_times
    global temp_Cs
    global pres_HPas
    global hum_RHs
    global light_LXs

    try:
        date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = measure_data()
        date_times = temp_Cs = pres_HPas = hum_RHs = light_LXs = find_data_measurements()
    except:
        debug("Could not request data!")
    else:
        debug("Requested data sucessfully")

    return redirect(url_for('index'))

# If download button is clicked, the CSV file will be download.
@app.route('/download_data')
def download_data():
    #TODO: Handle exceptions
    return send_file(DATA_FILE_PATH, as_attachment=True)

# If delete data button is clicked, the CSV file will be deleted.
@app.route('/delete_data')
def delete_data():
    try:
        remove(DATA_FILE_PATH)
    except:
        debug("Could not delete data file!")
    else:
        debug("Deleted data file sucessfully")

    return redirect(url_for('index'))

# If enable logging checkbox is clicked, the logging cron job will be enabled/disabled.
@app.route('/logging_ability')
def change_logging_ability():
    try:
        job, cron = find_logging_job()

        if job.is_enabled():
            job.enable(False)
        else:
            job.enable()

        cron.write()
    except:
        debug("Could not change logging ability!")
    else:
        debug("Changed logging ability")

    return redirect(url_for('index'))

# If enable light checkbox is clicked, the lights will be enabled/disabled.
@app.route('/light_on')
def light_on():
    try:
        leds_on()
    except:
        debug("Could not turn light on!")
    else:
        debug("Turned light on")

    return redirect(url_for('index'))

# If enable light checkbox is clicked, the lights will be enabled/disabled.
@app.route('/light_off')
def light_off():
    try:
        leds_off()
    except:
        debug("Could not turn light off!")
    else:
        debug("Turned light off")

    return redirect(url_for('index'))

# If reboot button is clicked, the Controller will reboot in 1 minute.
@app.route('/reboot_controller')
def reboot_controller():
    try:
        run(["sudo", "shutdown", "-r", "1"])
    except:
        debug("Could not reboot controller!")
    else:
        debug("Reboting in 1 minute")

    return redirect(url_for('index'))

# If update button is clicked, the Controller will update to the latest version.
@app.route('/update_controller')
def update_controller():
    try:
        result = run(["git", "pull"], cwd="/home/controller/controller", text=True, capture_output=True)
    except:
        debug("Could not update controller!")
    else:
        if result.stdout.find("Already up to date.") > -1:
            debug("Controller upto date!")
        else:
            debug("Updating controller at next reboot")

    return redirect(url_for('index'))

# Only run when directly called.
if __name__ == '__main__':
    app.run(host='0.0.0.0')