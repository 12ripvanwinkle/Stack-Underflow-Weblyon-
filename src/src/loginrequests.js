// loginrequests.js
console.log("loginrequests.js loaded");

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById("loginForm");
  if (!loginForm) return;

  loginForm.addEventListener("submit", async event => {
    event.preventDefault(); // Prevent page reload

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    // Basic validation
    if (!email || !password) {
      return alert("Email and password are required");
    }

    try {
      // Send POST request to backend API
      const response = await fetch("http://localhost:5000/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const result = await response.json();
      console.log("🔑 login response:", result);

      if (response.ok) {
        alert(result.message || "Login successful!");
        // Optionally store userId or token
        // localStorage.setItem("userId", result.userId);
        window.location.href = "dashboard.html";
      } else {
        alert("Login failed: " + result.message);
      }
    } catch (error) {
      console.error("Network error:", error);
      alert("Network error: could not reach the server.");
    }
  });
});
