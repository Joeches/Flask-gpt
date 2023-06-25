document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message !== '') {
            sendMessage(message);
            messageInput.value = '';
        }
    });

    function sendMessage(message) {
        const chatEntry = document.createElement('div');
        chatEntry.classList.add('chat-entry', 'user-message');
        chatEntry.textContent = message;
        chatLog.appendChild(chatEntry);

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(message)}`,
        })
        .then(response => response.json())
        .then(data => {
            const botEntry = document.createElement('div');
            botEntry.classList.add('chat-entry', 'bot-message');
            botEntry.textContent = data.message;
            chatLog.appendChild(botEntry);
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});
