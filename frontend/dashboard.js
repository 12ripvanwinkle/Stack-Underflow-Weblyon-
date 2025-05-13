const fs = require('fs');
const path = require('path');
const { ipcRenderer } = require('electron');

// SIGN OUT button
document.getElementById('signOut').addEventListener('click', () => {
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

  // 1) Load and display workspaces
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

        // Target the workspace-list container
        const listContainer = document.querySelector('.workspace-list');
        listContainer.innerHTML = ''; // clear any placeholder

        result.companies.forEach(company => {
          const card = document.createElement('div');
          card.className = 'workspace-card';
          card.textContent = company;
          listContainer.appendChild(card);
        });

      } else {
        console.warn('Unexpected or empty response format:', result);
      }

    } catch (error) {
      console.error('Error loading workspaces:', error);
    }
  });

  // 2) Attachment (paperclip) button
  const fileInput = document.getElementById('fileInput');
  fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log('Selected file:', file.path);
      // TODO: send file.path or file data to main process / API
      // ipcRenderer.send('upload-file', file.path);
    }
  });

  // 3) Send Chat (paper-plane) button
  document.getElementById('sendChat').addEventListener('click', () => {
    const promptText = document.getElementById('chatInput').value.trim();
    if (!promptText) return;
    console.log('Sending prompt:', promptText);

    // TODO: Replace with your AI-call or IPC sending
    // ipcRenderer.invoke('send-prompt', promptText).then(response => {
    //   // display AI response...
    // });
    
    // Clear the input
    document.getElementById('chatInput').value = '';
  });
});
