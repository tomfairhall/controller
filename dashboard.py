from flask import Flask, render_template, send_file, redirect, url_for
from crontab import CronTab, CronItem
from os import getlogin, remove, path
from subprocess import run
from socket import gethostname
import sys

try:
    from controller import measure_data, DATA_FILE_PATH, leds_on, leds_off
except PermissionError:
    print("Not Running on correct device!")

app = Flask(__name__)

VERSION = "error"

date_time = temp_C_ave = pres_HPa_ave = hum_RH_ave = light_Lx_ave = 0
debug_output = ""

# Main page.
@app.route('/')
def index():

    job, _ = find_logging_job()
    wifi_quality, wifi_strength = find_connection_strength()

    return render_template(
        'index.html',
        date_time = date_time,
        temperature = temp_C_ave,
        pressure = pres_HPa_ave,
        humidity = hum_RH_ave,
        lux = light_Lx_ave,
        logging_ability = job.is_enabled(),
        file_exists = find_data_file(),
        wifi_quality = wifi_quality,
        wifi_strength = wifi_strength,
        hostname = gethostname(),
        version = VERSION,
        debug_output = debug_output)

def debug(message):
    global debug_output
    debug_output = message

# Check that data file exists.
def find_data_file():
    return path.exists(DATA_FILE_PATH)

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

    cron = CronTab(user=getlogin())

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

    try:
        date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = measure_data()
    except:
        debug("Could not request data!")

    return redirect(url_for('index'))

# If download button is clicked, the CSV file will be download.
@app.route('/download_data')
def download_data():

    return send_file(DATA_FILE_PATH, as_attachment=True)

# If delete data button is clicked, the CSV file will be deleted.
@app.route('/delete_data')
def delete_data():

    remove(DATA_FILE_PATH)

    return redirect(url_for('index'))

# If enable logging checkbox is clicked, the logging cron job will be enabled/disabled.
@app.route('/logging_ability')
def change_logging_ability():

    job, cron = find_logging_job()

    if job.is_enabled():
        job.enable(False)
    else:
        job.enable()

    cron.write()

    return redirect(url_for('index'))

# If enable light checkbox is clicked, the lights will be enabled/disabled.
@app.route('/light_on')
def light_on():

    leds_on()

    return redirect(url_for('index'))

# If enable light checkbox is clicked, the lights will be enabled/disabled.
@app.route('/light_off')
def light_off():

    leds_off()

    return redirect(url_for('index'))

# If reboot button is clicked, the Controller will reboot in 1 minute.
@app.route('/reboot_controller')
def reboot_controller():
    run(["sudo", "shutdown", "-r", "1"])

    return redirect(url_for('index'))

# If update button is clicked, the Controller will update to the latest version.
@app.route('/update_controller')
def update_controller():
    run(["git", "pull"], cwd="/home/controller/controller")

    return redirect(url_for('index'))

# Only run when directly called.
if __name__ == '__main__':
    app.run(host='0.0.0.0')