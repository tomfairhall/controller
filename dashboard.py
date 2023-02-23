from flask import Flask, render_template, send_file
from crontab import CronTab, CronItem
from os import getlogin

# Incase running on a machine that isn't a raspberry pi.
try:
    import controller
except PermissionError:
    print("Not Running on correct device!")

logging_status_dictionary = {True: 'Stop', False: 'Start'}

app = Flask(__name__)

# If webserver connect or data is requested serve index page
@app.route('/')
@app.route('/request_data')
def index():

    job, _ = find_logging_job()
    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data()

    return render_template(
        'index.html',
        date_time = date_time,
        temperature = temp_C_ave,
        pressure = pres_HPa_ave,
        humidity = hum_RH_ave,
        lux = light_Lx_ave,
        logging_status = logging_status_dictionary[job.is_enabled()])

# If download button is clicked, the CSV file will download
@app.route('/download_data')
def download_data():

    path = "data.csv"

    return send_file(
       path,
       as_attachment=True
    )

def find_logging_job():
    
    cron = CronTab(user=getlogin())
    
    for job in cron.find_command('controller.py -w'):
        return job, cron

# If Start/Stop Logging button is clicked, the logging cron job will be enabled/disabled
@app.route('/logging_ability')
def change_logging_ability():

    job, cron = find_logging_job()
    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data()

    if job.is_enabled():
        job.enable(False)
    else:
        job.enable()

    cron.write()

    return render_template(
        'index.html',
        date_time = date_time,
        temperature = temp_C_ave,
        pressure = pres_HPa_ave,
        humidity = hum_RH_ave,
        lux = light_Lx_ave,
        logging_ability = logging_status_dictionary[job.is_enabled()])

# only run when directly called
if __name__ == '__main__':
    app.run(host='0.0.0.0')