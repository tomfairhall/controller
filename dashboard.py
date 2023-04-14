from flask import Flask, render_template, send_file, redirect, url_for
from crontab import CronTab, CronItem
from os import getlogin, remove, path
from subprocess import run

try:
    from controller import measure_data, DATA_FILE_PATH
except PermissionError:
    print("Not Running on correct device!")

app = Flask(__name__)

# Main page.
@app.route('/')
def index():

    job, _ = find_logging_job()
    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = measure_data()
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
        wifi_strength = wifi_strength)

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

# If download button is clicked, the CSV file will be download.
@app.route('/download_data')
def download_data():

    return send_file(
    DATA_FILE_PATH,
    as_attachment=True)

# If delete data button is clicked, the CSV file will be deleted.
@app.route('/delete_data')
def delete_data():

    remove(DATA_FILE_PATH)

    return redirect(url_for('index'))

# Find the data logging function.
def find_logging_job():

    cron = CronTab(user=getlogin())

    for job in cron.find_command('controller.py -w'):
        return job, cron

# If Start/Stop Logging button is clicked, the logging cron job will be enabled/disabled.
@app.route('/logging_ability')
def change_logging_ability():

    job, cron = find_logging_job()

    if job.is_enabled():
        job.enable(False)
    else:
        job.enable()

    cron.write()

    return redirect(url_for('index'))

# Only run when directly called.
if __name__ == '__main__':
    app.run(host='0.0.0.0')