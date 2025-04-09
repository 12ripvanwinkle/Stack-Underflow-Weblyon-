document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    function redirectToPrompts(event, targetURL = "welcome.html") {
        if (event) {
          event.preventDefault(); // Prevents actual form submission
        }
        window.location.href = "prompts_one.html"; // Redirects to the new page
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("http://localhost:5000/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();
            alert(data.message);

            // Redirect after successful login (modify as needed)
            if (response.ok) { // or if(data.success) or similar condition
                redirectToPrompts();
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const firstName = document.getElementById("firstName").value;
            const lastName = document.getElementById("lastName").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("http://localhost:5000/api/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ firstName, lastName, email, password })
            });

            const data = await response.json();
            alert(data.message);

            // Redirect after successful registration (modify as needed)
            if (response.ok) { // or if(data.success) or similar condition
                redirectToPrompts();
            }
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        const companyBtn = document.querySelector(".company-btn");

        if (companyBtn) {
            companyBtn.style.cursor = "pointer";
            companyBtn.addEventListener("click", function () {
                window.location.href = "company-register.html"; // Change this to the correct file name
            });
        }
    });
});