const params = new URLSearchParams(window.location.search); // get the URL parameters

const groupName = params.get("groupName"); // get the group name value from the URL parameters

const groupDisplay = document.getElementById("groupDisplay"); // find the group name display in the HTML

if (groupDisplay) { // display the group name if the element exists on the page
    groupDisplay.textContent = groupName;
}

const clockDisplay = document.getElementById("clock"); // find the HTML element with the id "clock" to display the current time

function updateClock() { // create function to update the clock
    const currentTime = new Date(); // get the current date and time
    // display the current time using hours and minutes
    clockDisplay.textContent = currentTime.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

updateClock(); // display current time when page opens

setInterval(updateClock, 1000); // update the time every second