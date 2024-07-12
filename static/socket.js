
        const socket = io();
        let clientId;

        socket.on('connect', () => {
            console.log('Connected to server');
            clientId = socket.id;
        });

        socket.on('previous_messages', (msgs) => {
            const messages = document.getElementById('messages');
            messages.innerHTML = '';   
            msgs.forEach((msg) => {
                displayMessage(msg);
            });
            messages.scrollTop = messages.scrollHeight;  
        });

        socket.on('message', (msg) => {
            displayMessage(msg);
            const messages = document.getElementById('messages');
            messages.scrollTop = messages.scrollHeight;  
        });

        function sendMessage() {
            const input = document.getElementById('message');
            const message = input.value;
            socket.send(message);
            input.value = '';
        }

        function displayMessage(msg) {
            const messages = document.getElementById('messages');
            const message = document.createElement('div');
            message.classList.add('message');
            
            const username = document.createElement('div');
            username.textContent = msg.username;
            username.classList.add('username');
            message.appendChild(username);

            const text = document.createElement('div');
            text.textContent = msg.text;
            message.appendChild(text);

            const timestamp = document.createElement('div');
            timestamp.textContent = msg.timestamp;
            timestamp.classList.add('timestamp');
            message.appendChild(timestamp);

            if (msg.id === clientId) {
                message.classList.add('my-message');
            } else {
                message.classList.add('other-message');
            }
            messages.appendChild(message);
        }
    