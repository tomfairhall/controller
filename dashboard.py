from flask import Flask, render_template
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

# route route directory
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/request_data')
def your_flask_route():

    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data()

    return render_template('index.html', 
                           date_time = date_time,
                           temperature = temp_C_ave, 
                           pressure = pres_HPa_ave, 
                           humidity = hum_RH_ave, 
                           lux = light_Lx_ave)

@app.route('/download_data')
def your_flask_route():

    return render_template('index.html')

# 
if __name__ == '__main__':
  if (args.debug):
    app.run(debug=True, host='0.0.0.0')
  else:
    app.run(host="0.0.0.0")