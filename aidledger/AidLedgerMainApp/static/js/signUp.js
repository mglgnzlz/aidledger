document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Retrieve form data
        const formData = new FormData(signupForm);
        const ethAddress = formData.get("ethAddress");

        // Perform client-side form validation if necessary

        // Send form data to the server using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open("POST", signupForm.action);
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken")); // Ensure CSRF token is included
        xhr.setRequestHeader("Content-Type", "application/json");

        // Convert form data to JSON format
        const jsonData = JSON.stringify({
            ethAddress: ethAddress,
            userType: formData.get("userType")  // Include account type in the JSON data
            // Add other form fields as needed
        });

        // Handle AJAX response
        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const dashboardUrl = response.dashboard_url;
                window.location.href = dashboardUrl; // Redirect to the dashboard URL
            } else {
                // Handle errors or display error messages to the user
                console.error("Error:", xhr.statusText);
            }
        };

        // Send JSON data
        xhr.send(jsonData);
    });

    // Function to retrieve CSRF token from cookies
    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
});
