const chatContainer = document.querySelector('.chat-container');
const sendBtn = document.getElementById('sendChat');
const chatInput = document.getElementById('chatInput');

// Append chat message to UI
function appendMessage(role, text) {
  const msg = document.createElement('div');
  msg.classList.add('chat-message', role);
  msg.textContent = text;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  console.log(`[${role}] ${text}`);
}

// Send on click
sendBtn.addEventListener('click', async () => {
  const promptText = chatInput.value.trim();
  if (!promptText) return;

  console.log('Sending prompt:', promptText);

  // 1️⃣ Show user bubble
  appendMessage('user', promptText);
  chatInput.value = '';

  // 2️⃣ Call your AI back-end
  try {
    const resp = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: promptText })
    });

    const data = await resp.json();
    console.log('Response from /chat:', data);

    // 3️⃣ Show AI response
    appendMessage('ai', data.reply || "⚠️ Empty response");

    // 4️⃣ Show templates if available
    if (Array.isArray(data.templates) && data.templates.length) {
      const opts = document.createElement('div');
      opts.classList.add('template-options');

      data.templates.forEach(t => {
        const card = document.createElement('div');
        card.classList.add('template-card');
        card.textContent = t.label;
        opts.appendChild(card);
      });

      chatContainer.appendChild(opts);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }

  } catch (err) {
    console.error('❌ Fetch failed:', err);
    appendMessage('ai', '⚠️ Couldn’t reach the AI service.');
  }
});

// Send on Enter key
chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendBtn.click();
  }
});

// Optional system message on load
appendMessage('ai', 'What type of website would you like to create: portfolio or ecommerce?');
