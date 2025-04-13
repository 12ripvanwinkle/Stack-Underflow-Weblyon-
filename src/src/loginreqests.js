document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent page reload

    // user input values
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // API request payload
    const requestData = {
        email: email,
        password: password
    };

    try {
        // Send POST request to backend API
        const response = await fetch("http://127.0.0.1:5000", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        // Handle API response
        const result = await response.json();
        if (response.ok) {
            alert("Login Successful!");
            localStorage.setItem("token", result.token); // Save token if needed
            window.location.href = "dashboard.html"; // Redirect to dashboard
        } else {
            alert("Login Failed: " + result.message);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while logging in.");
    }
});
