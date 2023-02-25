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