from flask import Flask, render_template, send_file
from crontab import CronTab
from os import getlogin

# Incase running on a machine that isn't a raspberry pi.
try:
    import controller
except PermissionError:
    print("Not Running on correct device!")


logging_status = False
logging_status_dictionary = {True: 'Stop', False: 'Start'}

date_time = 0
temp_C_ave = 0
pres_HPa_ave = 0
hum_RH_ave = 0
light_Lx_ave = 0

app = Flask(__name__)

# If the web server is connected to show the main page
@app.route('/')
def index():

    return render_template('index.html')

# If the request data button is click, sensors will measure and upload data to screen.
@app.route('/request_data')
def request_data():

    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data()

    return render_template(
        'index.html',
        date_time=date_time,
        temperature=temp_C_ave,
        pressure=pres_HPa_ave,
        humidity=hum_RH_ave,
        lux=light_Lx_ave)

# if download button is clicked, the CSV file will download
@app.route('/download_data')
def download_data():

    path = "data.csv"

    return send_file(
       path,
       as_attachment=True
    )

def check_logging_status():
    cron = CronTab(user=getlogin())
    
    for job in cron.find_command('controller.py'):
        return job.is_enabled

def start_logging():
    cron = CronTab(user=getlogin())
    
    return

def stop_logging():
    return

@app.route('/start_stop_logging')
def start_recording():
    
    logging_status = check_logging_status()

    return render_template(
        'index.html',
        logging_status = logging_status_dictionary[logging_status])


# only run when directly called
if __name__ == '__main__':
    app.run(host='0.0.0.0')