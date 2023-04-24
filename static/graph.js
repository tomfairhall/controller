const TEMP_MIN = 0;
const TEMP_MAX = 30;

const temperatureChart = document.getElementById('temperature-chart');
const pressureChart = document.getElementById('pressure-chart');
const humidityChart = document.getElementById('humidity-chart');
const luxChart = document.getElementById('lux-chart');

Chart.defaults.color = 'lightgrey';
Chart.defaults.borderColor = 'lightslategrey';
Chart.defaults.elements.point.pointStyle = false;
Chart.defaults.plugins.legend.display = false;

var loggedDataChart = new Chart(temperatureChart, {
    type: 'line',
    data: {
        labels: times,
        datasets: [{
            data: temp_Cs
        }]
    },
    options: {
        scales: {
            y: {
                max: TEMP_MAX,
                min: TEMP_MIN
            }
        }
    }
});

var loggedDataChart = new Chart(pressureChart, {
    type: 'line',
    data: {
        labels: times,
        datasets: [{
            data: pres_HPas
        }]
    }
});

var loggedDataChart = new Chart(humidityChart, {
    type: 'line',
    data: {
        labels: times,
        datasets: [{
            data: hum_RHs
        }]
    }
});

var loggedDataChart = new Chart(luxChart, {
    type: 'line',
    data: {
        labels: times,
        datasets: [{
            data: luxChart
        }]
    }
});