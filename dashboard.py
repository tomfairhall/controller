from flask import Flask, render_template, send_file, redirect, url_for
from crontab import CronTab, CronItem
from os import getlogin, remove, path

try:
    from controller import measure_data, DATA_FILE_PATH
except PermissionError:
    print("Not Running on correct device!")

DATA_PATH = "data.csv"

app = Flask(__name__)

# Main page.
@app.route('/')
def index():

    job, _ = find_logging_job()
    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = measure_data()

    return render_template(
        'index.html',
        date_time = date_time,
        temperature = temp_C_ave,
        pressure = pres_HPa_ave,
        humidity = hum_RH_ave,
        lux = light_Lx_ave,
        logging_ability = job.is_enabled(),
        file_exists = find_data_file())

def find_data_file():
    return path.exists(DATA_FILE_PATH)

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
        print("Logging is disabled")
    else:
        job.enable()
        print("Logging is enabled")

    cron.write()

    return redirect(url_for('index'))

# only run when directly called
if __name__ == '__main__':
    app.run(host='0.0.0.0')