from flask import Flask, render_template, send_file
import argparse

#incase running on a test machine that isn't a raspberry pi
try:
    import controller
except PermissionError:
    print("ERROR: Not Running on correct device!")

# initialize the input argument parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("-d", "--debug", help="run server in debug mode", action="store_true")

# parse input arguments
args = parser.parse_args()

date_time = 0
temp_C_ave = 0
pres_HPa_ave = 0
hum_RH_ave = 0
light_Lx_ave = 0

app = Flask(__name__)

# if the web server is connected to show the main page
@app.route('/')
def index():

    return render_template('index.html')

# if the request data button is click, sensors will measure and upload data to screen
@app.route('/request_data')
def request_data():

    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data()

    return render_template(
        'index.html', 
        date_time = date_time,
        temperature = temp_C_ave, 
        pressure = pres_HPa_ave, 
        humidity = hum_RH_ave, 
        lux = light_Lx_ave)

# if download button is clicked, the CSV file will download
@app.route('/download_data')
def download_data():

    path = "data.csv"

    return send_file(
       path,
       as_attachment=True
    )

# only run when directly called
if __name__ == '__main__':
  
  # run webs server in specified mode
  if (args.debug):
    app.run(debug=True, host='0.0.0.0')
  else:
    app.run(host="0.0.0.0")