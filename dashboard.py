from flask import Flask, render_template
import controller

app = Flask(__name__)

# route route directory
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/request_data')
def your_flask_route():

    print("here")

    temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = controller.measure_data(3)

    print(temp_C_ave)

    return render_template('index.html')

# 
if __name__ == '__main__':
  app.run(debug=True)