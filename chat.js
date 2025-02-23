document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('messageContainer');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const typingIndicator = document.getElementById('typingIndicator');
    const suggestions = document.getElementById('suggestions');
    const voiceRecordBtn = document.getElementById('voiceRecordBtn');
    const stopRecordingBtn = document.getElementById('stopRecordingBtn');
    const recordingIndicator = document.getElementById('recordingIndicator');
    const recordingTime = document.getElementById('recordingTime');

    let mediaRecorder = null;
    let audioChunks = [];
    let recordingInterval = null;
    let recordingStartTime = null;

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        // Get current time for user message
        const now = new Date();
        const userTimestamp = now.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });

        // Add user message
        addMessage(message, 'user', userTimestamp);
        messageInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Hide typing indicator and add bot response
            hideTypingIndicator();
            addMessage(data.response, 'bot', data.timestamp);

        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again.', 'bot', userTimestamp);
        }

        // Hide suggestions after first interaction
        suggestions.style.display = 'none';
    });

    // Voice recording functionality
    voiceRecordBtn.addEventListener('click', async function() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            stopRecording();
            return;
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await sendAudioMessage(audioBlob);

                // Stop all tracks in the stream
                stream.getTracks().forEach(track => track.stop());
            });

            // Start recording
            mediaRecorder.start();
            recordingStartTime = Date.now();
                      startRecordingTimer();

            // Update UI
            voiceRecordBtn.classList.add('recording');
            recordingIndicator.classList.remove('d-none');
            messageInput.disabled = true;

        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Unable to access microphone. Please ensure you have granted permission.');
        }
    });

    stopRecordingBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            stopRecording();
        }
    });

    function stopRecording() {
        if (mediaRecorder) {
            mediaRecorder.stop();
            clearInterval(recordingInterval);

            // Reset UI
            voiceRecordBtn.classList.remove('recording');
            recordingIndicator.classList.add('d-none');
            messageInput.disabled = false;
            recordingTime.textContent = '0:00';
        }
    }

    function startRecordingTimer() {
        recordingInterval = setInterval(() => {
            const duration = Math.floor((Date.now() - recordingStartTime) / 1000);
            const minutes = Math.floor(duration / 60);
            const seconds = duration % 60;
            recordingTime.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }

    async function sendAudioMessage(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob);

        try {
            const response = await fetch('/chat/audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to send audio message');
            }

            const data = await response.json();

            // Add the audio message to the chat
            addAudioMessage(data.audio_url, 'user', data.timestamp);

            // Add bot response if any
            if (data.response) {
                addMessage(data.response, 'bot', data.timestamp);
            }

        } catch (error) {
            console.error('Error sending audio message:', error);
            alert('Failed to send audio message. Please try again.');
        }
    }

    function addAudioMessage(audioUrl, sender, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const audioElement = document.createElement('audio');
        audioElement.controls = true;
        audioElement.src = audioUrl;
        audioElement.className = 'audio-message';

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = timestamp;

        contentDiv.appendChild(audioElement);
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        messageContainer.appendChild(messageDiv);

        // Scroll to bottom
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Function to add a message to the chat
    function addMessage(message, sender, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = message;

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = timestamp;

        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        messageContainer.appendChild(messageDiv);

        // Scroll to bottom
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
  
    // Function to show typing indicator
    function showTypingIndicator() {
        typingIndicator.classList.remove('d-none');
        messageContainer.appendChild(typingIndicator);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Function to hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.classList.add('d-none');
    }
});

// Function to handle suggestion clicks
function sendSuggestion(button) {
    const message = button.textContent.trim();
    document.getElementById('messageInput').value = message;
    document.getElementById('chatForm').dispatchEvent(new Event('submit'));
}

// Function to save preferences
async function savePreferences() {
    const form = document.getElementById('preferencesForm');
    const formData = {
        theme: form.theme.value,
        message_display: form.message_display.value,
        notification_enabled: form.notification_enabled.checked
    };

    try {
        const response = await fetch('/preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Failed to save preferences');
        }

        const data = await response.json();

        // Apply theme immediately
        document.documentElement.setAttribute('data-bs-theme', data.theme);

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('preferencesModal'));
        modal.hide();

        // Show success message
        addMessage('Preferences updated successfully!', 'bot', new Date().toLocaleString('en-US', { 
            hour: 'numeric', 
            minute: 'numeric', 
            hour12: true 
        }));

    } catch (error) {
        console.error('Error saving preferences:', error);
        alert('Failed to save preferences. Please try again.');
    }
          }
