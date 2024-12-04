document.getElementById("confirm-btn").addEventListener("click", function() {
    var confirmation = confirm("Are you sure you want to proceed?");
    
    if (confirmation) {
        // Proceed with the action
        console.log("User confirmed the action");
        // For example, make an AJAX request or redirect
    } else {
        // If the user cancels
        console.log("User canceled the action");
    }
});