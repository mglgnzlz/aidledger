document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Retrieve form data
        const formData = new FormData(signupForm);
        const ethAddress = formData.get("eth_address");
        console.log("Ethereum Address:", ethAddress);  // Log eth_address value

        // Check if ethAddress is correctly populated
        if (!ethAddress) {
            console.error("Ethereum address is missing.");
            return;
        }

        // Send form data to the server using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open("POST", signupForm.action);
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken")); // Ensure CSRF token is included
        xhr.setRequestHeader("Content-Type", "application/json");

        // Convert form data to JSON format
        const jsonData = JSON.stringify({
            username: ethAddress, // Use ethAddress as username
            userType: formData.get("userType"),
            accountName: formData.get("accountName"), // Include account type in the JSON data
        });

        // Handle AJAX response
        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                console.log("Redirecting to:", response.redirect_url);
                window.location.href = response.redirect_url; // Redirect to the response URL (dashboard)
            } else {
                // Handle errors or display error messages to the user
                console.error("Error:", xhr.statusText);
            }
        };

        // Send JSON data
        xhr.send(jsonData);
        console.log("JSON Data Sent:", jsonData);
    });

    // Function to retrieve CSRF token from cookies
    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
});
