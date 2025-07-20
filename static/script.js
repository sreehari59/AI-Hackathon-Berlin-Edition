document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const recordButton = document.getElementById('record-button');

    // Store conversation history
    let conversationHistory = [
        { role: 'system', content: 'Hello! I\'m your AI travel assistant. How can I help you today?' }
    ];

    // Audio recording variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // Auto-resize textarea as user types
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';
    });

    // Handle form submission
    messageForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        // Add user message to UI
        addMessageToUI('user', userMessage);

        // Add user message to conversation history
        conversationHistory.push({ role: 'user', content: userMessage });

        // Clear input
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Show loading indicator
        const loadingElement = addLoadingIndicator();

        try {
            // Send message to backend
            const response = await sendMessageToBackend(conversationHistory);

            // Remove loading indicator
            loadingElement.remove();

            // Add assistant response to UI
            addMessageToUI('assistant', response.message.content);

            // Add assistant response to conversation history
            conversationHistory.push({ role: 'assistant', content: response.message.content });

            // Scroll to bottom
            scrollToBottom();
        } catch (error) {
            // Remove loading indicator
            loadingElement.remove();

            // Show error message
            addMessageToUI('system', 'Sorry, there was an error processing your request. Please try again.');
            console.error('Error:', error);
        }
    });

    // Function to add a message to the UI
    function addMessageToUI(role, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', role);

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = content;

        messageElement.appendChild(contentElement);
        chatMessages.appendChild(messageElement);

        // Scroll to bottom
        scrollToBottom();
    }

    // Function to add loading indicator
    function addLoadingIndicator() {
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('message', 'assistant', 'loading');

        const dotsElement = document.createElement('div');
        dotsElement.classList.add('loading-dots');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dotsElement.appendChild(dot);
        }

        loadingElement.appendChild(dotsElement);
        chatMessages.appendChild(loadingElement);

        // Scroll to bottom
        scrollToBottom();

        return loadingElement;
    }

    // Function to scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to send message to backend
    async function sendMessageToBackend(messages) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messages.map(msg => ({
                    role: msg.role,
                    content: msg.content
                }))
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    // Initial scroll to bottom
    scrollToBottom();

    // Handle record button click
    recordButton.addEventListener('click', async () => {
        if (!isRecording) {
            // Start recording
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', async () => {
                    // Convert audio chunks to base64
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const reader = new FileReader();

                    reader.onloadend = async () => {
                        const base64Audio = reader.result.split(',')[1];

                        // Show loading indicator
                        const loadingElement = addLoadingIndicator();

                        try {
                            // Send audio to backend
                            const response = await fetch('/api/voice/process', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    audio_base64: base64Audio
                                })
                            });

                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status}`);
                            }

                            const data = await response.json();

                            // Remove loading indicator
                            loadingElement.remove();

                            // Add transcribed text to input
                            messageInput.value = data.transcript;
                            messageInput.style.height = 'auto';
                            messageInput.style.height = (messageInput.scrollHeight) + 'px';
                            messageInput.focus();

                        } catch (error) {
                            // Remove loading indicator
                            loadingElement.remove();

                            // Show error message
                            addMessageToUI('system', 'Sorry, there was an error processing your audio. Please try again.');
                            console.error('Error:', error);
                        }
                    };

                    reader.readAsDataURL(audioBlob);
                });

                // Start recording
                mediaRecorder.start();
                isRecording = true;
                recordButton.classList.add('recording');

            } catch (error) {
                console.error('Error accessing microphone:', error);
                addMessageToUI('system', 'Error accessing microphone. Please check your browser permissions.');
            }
        } else {
            // Stop recording
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();

                // Stop all audio tracks
                mediaRecorder.stream.getTracks().forEach(track => track.stop());

                isRecording = false;
                recordButton.classList.remove('recording');
            }
        }
    });
});
