function checkLogin(event) {
    event.preventDefault(); // Prevent form submission

    console.log("Check login initiated.");

    // Get the input values
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    console.log("Username:", username);
    console.log("Password:", password);

    // Validate input
    if (!username || !password) {
        console.log("Input validation failed: Please enter both username and password.");
        alert("Please enter both username and password.");
        return; // Exit the function if input is invalid
    }

    console.log("Input validation passed.");

    // Define the valid credentials
    var validCredentials = [
        { email: "sagardubey1622@gmail.com", password: "1234567890" },
        { email: "bytemasterdubey@gmail.com", password: "1234567890" },
        { email: "xyz@gmail.com", password: "1234567890" }
    ];

    // Check if the entered credentials match any of the valid credentials
    var isValid = validCredentials.some(function (credential) {
        return credential.email === username && credential.password === password;
    });

    console.log("isValid:", isValid);

    if (isValid) {
        // Redirect to index.html if login is successful
        console.log("Login successful. Redirecting to index.html");
        window.location.href = "index.html";
    } else {
        // Display an error message or perform any other action for invalid login
        console.log("Login failed: Invalid username or password.");
        alert("Invalid username or password. Please try again.");
    }
}

function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var toggleButton = document.querySelector(".toggle-password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.innerHTML = '<img src="/static/images/bxs-show.svg" alt="Show Password">';
    } else {
        passwordInput.type = "password";
        toggleButton.innerHTML = '<img src="/static/images/bxs-hide.svg" alt="Hide Password">';
    }
}
