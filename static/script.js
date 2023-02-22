function change_logging_status_button() {

    var element = document.getElementById("logging_status_button");

    if (element.textContent.includes("Stop Logging")) {
        element.style.color = "red";
    } else if (element.textContent.includes("Start Logging")) {
        element.style.color = "green"
    }
}