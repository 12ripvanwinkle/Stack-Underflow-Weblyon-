const fs = require('fs');
const path = require('path');
const { ipcRenderer } = require('electron');


document.getElementById('Sign Out').addEventListener('click', () => {
  const filePath = path.join(__dirname, 'state.json');

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading state.json:', err);
      return;
    }

    try {
      const state = JSON.parse(data);

      // Clear the values
      state.username = "";
      state.email = "";
      state.password = "";

      // Write the updated JSON
      fs.writeFile(filePath, JSON.stringify(state, null, 2), (err) => {
        if (err) {
          console.error('Error writing to state.json:', err);
        } else {
          console.log('User data cleared from state.json');
          // Redirect to login page
          ipcRenderer.send('redirect', 'login.html');
          
        }
      });

    } catch (parseErr) {
      console.error('Failed to parse state.json:', parseErr);
    }
  });
});

window.addEventListener('DOMContentLoaded', () => {
    const filePath = path.join(__dirname, 'state.json');
  
    fs.readFile(filePath, 'utf8', async (err, data) => {
      if (err) {
        console.error('Failed to read state.json:', err);
        return;
      }
  
      try {
        const state = JSON.parse(data);
  
        if (!state.email || !state.password) {
          console.warn('Missing credentials');
          return;
        }
  
        const response = await fetch('http://127.0.0.1:5000/companies', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Cache-Control': 'no-cache'
          },
          body: JSON.stringify({
            email: state.email,
            password: state.password
          })
        });
  
        const result = await response.json();
  
        if (response.ok && Array.isArray(result.companies)) {
          console.log('Fetched workspaces:', result.companies);
  
          const container = document.querySelector('div');
          const listTitle = document.createElement('h4');
          listTitle.textContent = "Your Workspaces:";
          container.appendChild(listTitle);
  
          result.companies.forEach(company => {
            const item = document.createElement('p');
            item.textContent = `${company}`;
            container.appendChild(item);
          });
  
        } else {
          console.warn('Unexpected or empty response format:', result);
        }
  
      } catch (error) {
        console.error('Error loading workspaces:', error);
      }
    });
  });