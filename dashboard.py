from flask import Flask, render_template

try:
    import controller
except PermissionError:
    print("ERROR: Not Running on correct device!")

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

    print("here")

    date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data()

    print(temp_C_ave)

    return render_template('index.html', 
                           date_time = date_time,
                           temperature = temp_C_ave, 
                           pressure = pres_HPa_ave, 
                           humidity = hum_RH_ave, 
                           lux = light_Lx_ave)

# 
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')