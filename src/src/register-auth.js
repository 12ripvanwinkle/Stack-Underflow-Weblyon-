const registerUser = async () => {
    const url = "http://127.0.0.1:5000/users";
    const userData = {
        "Username": "john_doe",
        "Password": "securepassword123",
        "Email": "johndoe@example.com"
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();
        console.log("Server Response:", result);
        return result;  // Return the server response
    } catch (error) {
        console.error("Error submitting data:", error);
        return null;  // Return null if an error occurs
    }
};

// Call the function and print the result
registerUser().then(response => console.log("Printed Response:", response));
