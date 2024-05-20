document.addEventListener("DOMContentLoaded", function() {
    // Get range input used to enter priority index for tasks
    let priority_range_input = document.querySelector("#priority-range-input");

    // If found
    if (priority_range_input) {
        // Set label above the range input to reflect the input's current value.
        // Both "mousemove" and "touchmove" are listened for to support touchscreen devices as well as touchpads/mice.
        priority_range_input.addEventListener("mousemove", function() {
            document.querySelector("#priority-input").innerHTML = "Set Task Priority: " + parseFloat(
                priority_range_input.value
            ).toFixed(1);
        });
        priority_range_input.addEventListener("touchmove", function() {
            document.querySelector("#priority-input").innerHTML = "Set Task Priority: " + parseFloat(
                priority_range_input.value
            ).toFixed(1);
        });
    }
    
    // All the possible log types
    let logTypes = ["Added", "Edited", "Completed", "Deleted"];

    // Begin by enabling all
    let enabledTypes = ["Added", "Edited", "Completed", "Deleted"];

    // Function that updates the table on the history tab to hide logs of a type not in enabledTypes and show others
    function updateHistory() {
        // For each possible type
        for (type of logTypes) {
            // Get all logs (rows in table) of the type (specified by class name)
            logsOfType = document.querySelectorAll(`.${type}`);

            // If the type is in enabledTypes
            if (enabledTypes.includes(type)) {
                // Reset display of all such logs (rows) to be shown
                for (log of logsOfType) {
                    log.style.display = "";
                }
            } else {
                // Set display property of all such logs (rows) as none
                for (log of logsOfType) {
                    log.style.display = "none";
                }
            }
        }
    }

    // Get all check buttons (top left in history.html)
    let checkBtns = document.querySelectorAll(".btn-check");

    // If found
    if (checkBtns) {
        // Add an event listener to each button
        for (btn of checkBtns) {
            btn.addEventListener("change", function() {
                // If the button is checked and enabledTypes doesn't already contain the value of this button,
                // Add the check buttons value to enabledTypes
                if (this.checked) {
                    if (!enabledTypes.includes(this.value)) {
                        enabledTypes.push(this.value);
                    }
                } else {
                    // Otherwise, remove the all occurrences of the check button's value from enabledTypes
                    while (enabledTypes.includes(this.value)) {
                        enabledTypes.splice(enabledTypes.indexOf(this.value), 1);
                    }
                }

                // Update History
                updateHistory();
            });
        }
    }
});
