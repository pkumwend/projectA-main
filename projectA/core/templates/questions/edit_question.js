
document.addEventListener("DOMContentLoaded", function () {
    const questionType = document.getElementById("id_question_type"); // find the question type dropdown
    const modelAnswer = document.getElementById("id_model_answer"); // find the model answer field
    const choicesSection = document.getElementById("choices-section"); // find the choices section

    if (!questionType || !choicesSection) return;

    const modelAnswerRow = modelAnswer?.closest("p"); // find the model answer field container

    function updateQuestionFields() { // show or hide fields depending on the selected question type
        const selectedType = questionType.value.toLowerCase().trim();

        const isMultipleChoice = selectedType === "multiple choice";
        const isShortAnswer = selectedType === "short answer";

        choicesSection.hidden = !isMultipleChoice; // show choices only for multiple choice questions

        if (modelAnswerRow) {
            modelAnswerRow.hidden = !isShortAnswer; // show model answer only for short answer questions
        }
    }

    questionType.addEventListener("change", updateQuestionFields); // update when the dropdown changes

    updateQuestionFields(); // display the correct fields when the page first loads

    // Make checkbox labels clearer for staff
    choicesSection.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        const label = choicesSection.querySelector(`label[for="${checkbox.id}"]`);
        if (!label) return;

        const labelText = label.textContent.trim().toLowerCase();

        if (labelText === "delete:" || labelText === "delete") {
            label.textContent = "Remove this answer option:";
        } else if (labelText === "correct answer:" || labelText === "correct answer") {
            label.textContent = "Mark as correct answer:";
        }
    });
});
