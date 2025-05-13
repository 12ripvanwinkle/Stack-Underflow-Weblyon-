const fs = require('fs');
const path = require('path');
const { ipcRenderer } = require('electron');

window.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('login');

  loginBtn?.addEventListener('click', async () => {
    const emailInput = document.getElementById('email').value.trim();
    const passwordInput = document.getElementById('password').value.trim();

    if (!emailInput || !passwordInput) {
      alert('Please enter both email and password.');
      return;
    }

    loginBtn.disabled = true;

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': '*/*',
          'Cache-Control': 'no-cache'
        },
        body: JSON.stringify({ email: emailInput, password: passwordInput })
      });

      const result = await response.json();

      if (response.ok) {
        console.log('Login successful:', result);

        const filePath = path.join(__dirname, 'state.json');

        fs.readFile(filePath, 'utf8', (err, data) => {
          if (err) {
            console.error('Error reading state.json:', err);
            return;
          }

          try {
            const state = JSON.parse(data);
            state.email = result.email;
            state.username = result.username;
            state.password = passwordInput;

            fs.writeFile(filePath, JSON.stringify(state, null, 2), (err) => {
              if (err) {
                console.error('Error writing to state.json:', err);
              } else {
                console.log('Login data saved to state.json');
              }
              ipcRenderer.send('redirect', 'dashboard.html');
            });
          } catch (parseErr) {
            console.error('Failed to parse state.json:', parseErr);
            loginBtn.disabled = false;
            alert('Could not save login data.');
          }
        });
      } else {
        alert(result.message || 'Login failed.');
        loginBtn.disabled = false;
      }
    } catch (err) {
      console.error('Fetch error:', err);
      alert('An error occurred during login.');
      loginBtn.disabled = false;
    }
  });
});
