const temperatureChart = document.getElementById('temperature-chart');
const pressureChart = document.getElementById('pressure-chart');
const humidityChart = document.getElementById('humidity-chart');
const lightChart = document.getElementById('light-chart');

Chart.defaults.color = 'lightgrey';
Chart.defaults.borderColor = 'lightslategrey';
Chart.defaults.elements.point.pointStyle = false;
Chart.defaults.plugins.legend.display = false;

var chart = new Chart(temperatureChart, {
    type: 'line',
    data: {
        labels: timeData,
        datasets: [{
            data: temperatureData
        }]
    }
});

var chart = new Chart(pressureChart, {
    type: 'line',
    data: {
        labels: timeData,
        datasets: [{
            data: pressureData
        }]
    }
});

var chart = new Chart(humidityChart, {
    type: 'line',
    data: {
        labels: timeData,
        datasets: [{
            data: humidityData
        }]
    }
});

var chart = new Chart(lightChart, {
    type: 'line',
    data: {
        labels: timeData,
        datasets: [{
            data: lightData
        }]
    }
});