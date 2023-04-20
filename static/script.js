function checkData() {
    if (exists) {
        window.location.href='download_data';
    } else {
        dataAlert()
    }
}

function deleteData() {
    if (exists && confirm('Are you sure you want to delete saved data?')) {
        window.location.href='delete_data'
    } else {
        dataAlert()
    }
}

function dataAlert() {
    alert('File does not exist!');
}

var temperature = [12, 12, 11, 10, 10, 11];
var time = ['-2.5', '-2.0', '-1.5', '-1.0', '-0.5', 'Now'];

const ctx = document.getElementById('logged-data');

var loggedDataChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: time,
        datasets: [{
            label: 'Pop',
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
                borderColor: 'red'
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                ticks: {
                    color: 'lightgrey',
                    padding: 10
                }
            },
            y: {
                grid: {
                    color: 'lightslategrey',
                    tickLength: 0
                },
                ticks: {
                    color: 'lightgrey',
                    padding: 10
                }
            }
        }
    }
});