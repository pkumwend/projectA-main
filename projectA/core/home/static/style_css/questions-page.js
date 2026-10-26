
const params = new URLSearchParams(window.location.search); // get the URL parameters

const groupName = params.get("groupName"); // get the group name value from the URL parameters

const groupDisplay = document.getElementById("groupDisplay"); // find the group name display in the HTML

if (groupDisplay && groupName) { // display the group name if the element exists on the page
    groupDisplay.textContent = groupName;
}

const clockDisplay = document.getElementById("clock"); // find the HTML element with the id "clock" to display the current time

function updateClock() { // create function to update the clock
    if (!clockDisplay) return; // prevent errors on pages without a clock

    const currentTime = new Date(); // get the current date and time

    // display the current time using hours and minutes
    clockDisplay.textContent = currentTime.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

updateClock(); // display current time when page opens

if (clockDisplay) setInterval(updateClock, 1000); // update the time every second


// Student photo upload and preview
document.querySelectorAll(".questions-page .answer-content").forEach(answerArea => {
    const fileInput = answerArea.querySelector('input[type="file"]'); // find the photo upload field
    if (!fileInput) return; // skip questions without photo uploads

    const fieldParagraph = fileInput.closest("p"); // find the Django form field container
    const preview = answerArea.querySelector(".photo-preview"); // find the photo preview container
    const previewImage = preview?.querySelector("img"); // find the preview image
    const previewName = preview?.querySelector(".photo-preview-name"); // find the photo filename

    if (!fieldParagraph || !preview || !previewImage || !previewName) return;

    const currentLink = fieldParagraph.querySelector('a[href]'); // find the existing uploaded photo link
    const clearCheckbox = fieldParagraph.querySelector('input[type="checkbox"]'); // find the remove photo checkbox
    const savedPhotoUrl = currentLink?.href; // get the saved photo URL
    const savedPhotoName = currentLink?.textContent.trim(); // get the saved photo filename

    // Hide Django's original filename and default text
    fieldParagraph.childNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE) {
            node.textContent = "";
        }
    });

    if (currentLink) {
        currentLink.style.display = "none"; // hide the long uploaded filename link
    }

    // Display the existing uploaded photo or a newly selected photo
    let previewUrl = null;

    const updatePreview = () => {
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl); // release the previous temporary image URL
            previewUrl = null;
        }

        const file = fileInput.files?.[0]; // get the selected photo

        if (file && file.type.startsWith("image/")) {
            previewUrl = URL.createObjectURL(file); // create a temporary preview URL
            previewImage.src = previewUrl; // display the selected photo
            previewName.textContent = file.name; // display the selected filename
            preview.hidden = false; // show the photo preview
        } else if (savedPhotoUrl && !clearCheckbox?.checked) {
            previewImage.src = savedPhotoUrl; // display the previously uploaded photo
            previewName.textContent = savedPhotoName || "Previously uploaded photo";
            preview.hidden = false; // show the saved photo preview
        } else {
            previewImage.removeAttribute("src"); // remove the image when no photo is available
            previewName.textContent = "";
            preview.hidden = true; // hide the photo preview
        }
    };

    fileInput.addEventListener("change", updatePreview); // update preview when a new photo is selected
    clearCheckbox?.addEventListener("change", updatePreview); // update preview when removal is selected

    // Move Django's removal checkbox underneath the upload field
    if (clearCheckbox) {
        const clearLabel = fieldParagraph.querySelector(
            `label[for="${clearCheckbox.id}"]`
        );

        const removeRow = document.createElement("div"); // create a separate row for photo removal
        removeRow.className = "remove-photo-row";

        removeRow.appendChild(clearCheckbox); // move the existing checkbox into the new row

        if (clearLabel) {
            clearLabel.textContent = "Remove current photo"; // rename Django's default Clear label
            removeRow.appendChild(clearLabel);
        } else {
            const label = document.createElement("label");
            label.htmlFor = clearCheckbox.id;
            label.textContent = "Remove current photo";
            removeRow.appendChild(label);
        }

        fieldParagraph.after(removeRow); // place the removal option underneath the upload field
    }

    updatePreview(); // show the existing image immediately when returning to the questions page
});


