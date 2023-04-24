var temperature = [14, 13, 12, 12, 11, 10, 10, 11];
var time = ['-3.5', '-3.0', '-2.5', '-2.0', '-1.5', '-1.0', '-0.5', '0'];

const temperatureChart = document.getElementById('temperature-chart');
const pressureChart = document.getElementById('pressure-chart');
const humidityChart = document.getElementById('humidity-chart');
const luxChart = document.getElementById('lux-chart');

Chart.defaults.color = 'lightgrey'

var loggedDataChart = new Chart(temperatureChart, {
    type: 'line',
    data: {
        labels: time,
        datasets: [{
            data: temperature
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        elements: {
            line: {
                borderColor: 'lightgrey'
            },
            point: {
                pointStyle: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                ticks: {
                    display: false
                }
            },
            y: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                max: 30,
                min: 0
            }
        }
    }
});

var loggedDataChart = new Chart(pressureChart, {
    type: 'line',
    data: {
        labels: time,
        datasets: [{
            data: temperature
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        elements: {
            line: {
                borderColor: 'lightgrey'
            },
            point: {
                pointStyle: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                ticks: {
                    display: false
                }
            },
            y: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                max: 30,
                min: 0
            }
        }
    }
});

var loggedDataChart = new Chart(humidityChart, {
    type: 'line',
    data: {
        labels: time,
        datasets: [{
            data: temperature
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        elements: {
            line: {
                borderColor: 'lightgrey'
            },
            point: {
                pointStyle: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                ticks: {
                    display: false
                }
            },
            y: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                max: 30,
                min: 0
            }
        }
    }
});

var loggedDataChart = new Chart(luxChart, {
    type: 'line',
    data: {
        labels: time,
        datasets: [{
            data: temperature
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        elements: {
            line: {
                borderColor: 'lightgrey'
            },
            point: {
                pointStyle: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                ticks: {
                    display: false
                }
            },
            y: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                max: 30,
                min: 0
            }
        }
    }
});