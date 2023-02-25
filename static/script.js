function checkData() {

    if (exists) {
        window.location.href='download_data';
    } else {
        alert('File does not exist!');
    }
}

function deleteData() {
   
    if (exists && confirm('Are you sure you want to delete saved data?')) {
        window.location.href='delete_data'
    } else {
        alert('File to delete does not exist')
    }
}