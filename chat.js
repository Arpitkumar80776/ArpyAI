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

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        const now = new Date();
        const userTimestamp = now.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });

        addMessage(message, 'user', userTimestamp);
        messageInput.value = '';

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

            hideTypingIndicator();
            addMessage(data.response, 'bot', data.timestamp);
        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again.', 'bot', userTimestamp);
        }

        suggestions.style.display = 'none';
    });

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

                stream.getTracks().forEach(track => track.stop());
            });

            mediaRecorder.start();
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
        }
    }
});
