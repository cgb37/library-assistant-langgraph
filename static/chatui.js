// static/chatui.js
// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle?.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
});

// Sidebar toggle for mobile (optional, if you want to add responsive behavior)
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
sidebarToggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('hidden');
});

// Chat form submit - Updated to use footer form with loading feedback
document.getElementById('chatForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const submitButton = e.target.querySelector('button[type="submit"]');
    const chatWindow = document.getElementById('chatWindow');
    
    if (input.value.trim()) {
        // Show user bubble
        const userBubble = document.createElement('div');
        userBubble.className = 'self-end max-w-lg bg-blue-600 text-white rounded-lg px-4 py-2 shadow';
        userBubble.textContent = input.value;
        chatWindow.appendChild(userBubble);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Show loading indicator
        const loadingBubble = document.createElement('div');
        loadingBubble.className = 'self-start max-w-lg bg-gray-700 text-white rounded-lg px-4 py-2 shadow loading-bubble';
        loadingBubble.innerHTML = `
            <div class="flex items-center space-x-2">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style="animation-delay: 0.1s;"></div>
                    <div class="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style="animation-delay: 0.2s;"></div>
                </div>
                <span class="text-sm">Assistant is thinking...</span>
            </div>
        `;
        chatWindow.appendChild(loadingBubble);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Disable submit button and change text
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
        submitButton.className = submitButton.className.replace('bg-blue-600', 'bg-gray-500 cursor-not-allowed').replace('hover:bg-blue-700', '');

        const userQuery = input.value;
        input.value = '';

        // Send to backend
        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: userQuery })
            });
            const data = await res.json();
            
            // Remove loading bubble
            chatWindow.removeChild(loadingBubble);
            
            if (data.response) {
                const botBubble = document.createElement('div');
                botBubble.className = 'self-start max-w-lg bg-gray-800 text-white rounded-lg px-4 py-2 shadow';
                
                // Add routing info if available
                let responseText = data.response;
                if (data.support_level && data.routing_reason) {
                    responseText = `🎯 ${data.support_level.toUpperCase()} Support\n💭 ${data.routing_reason}\n\n${responseText}`;
                }
                
                botBubble.style.whiteSpace = 'pre-wrap';
                botBubble.textContent = responseText;
                chatWindow.appendChild(botBubble);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            } else if (data.error) {
                const errorBubble = document.createElement('div');
                errorBubble.className = 'self-start max-w-lg bg-red-600 text-white rounded-lg px-4 py-2 shadow';
                errorBubble.textContent = '❌ Error: ' + data.error;
                chatWindow.appendChild(errorBubble);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        } catch (err) {
            // Remove loading bubble on error
            if (chatWindow.contains(loadingBubble)) {
                chatWindow.removeChild(loadingBubble);
            }
            
            const errorBubble = document.createElement('div');
            errorBubble.className = 'self-start max-w-lg bg-red-600 text-white rounded-lg px-4 py-2 shadow';
            errorBubble.textContent = '❌ Network error. Please try again.';
            chatWindow.appendChild(errorBubble);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        } finally {
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
            submitButton.className = submitButton.className.replace('bg-gray-500 cursor-not-allowed', 'bg-blue-600') + ' hover:bg-blue-700';
        }
    }
});

// Image upload button (placeholder)
document.getElementById('imageUpload')?.addEventListener('change', function(e) {
    alert('Image upload is not implemented in this mockup.');
});
