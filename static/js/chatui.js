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
                botBubble.className = 'self-start max-w-lg bg-gray-800 text-white rounded-lg px-4 py-2 shadow relative group';
                
                // Add routing info if available
                let responseText = data.response;
                if (data.support_level && data.routing_reason) {
                    responseText = `🎯 ${data.support_level.toUpperCase()} Support\n💭 ${data.routing_reason}\n\n${responseText}`;
                }
                
                // Create response container with buttons
                const responseContainer = document.createElement('div');
                responseContainer.style.whiteSpace = 'pre-wrap';
                responseContainer.textContent = responseText;
                
                // Create buttons container
                const buttonsContainer = document.createElement('div');
                buttonsContainer.className = 'absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex space-x-1';
                
                // Copy button
                const copyButton = document.createElement('button');
                copyButton.className = 'p-1 bg-gray-600 hover:bg-gray-500 rounded text-xs transition-colors duration-200';
                copyButton.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                `;
                copyButton.title = 'Copy to clipboard';
                copyButton.addEventListener('click', async () => {
                    try {
                        await navigator.clipboard.writeText(data.response);
                        copyButton.innerHTML = `
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        `;
                        setTimeout(() => {
                            copyButton.innerHTML = `
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                                </svg>
                            `;
                        }, 2000);
                    } catch (err) {
                        console.error('Failed to copy text: ', err);
                    }
                });
                
                // Save button
                const saveButton = document.createElement('button');
                saveButton.className = 'p-1 bg-blue-600 hover:bg-blue-500 rounded text-xs transition-colors duration-200';
                saveButton.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
                    </svg>
                `;
                saveButton.title = 'Save chat';
                saveButton.addEventListener('click', async () => {
                    try {
                        const originalHTML = saveButton.innerHTML;
                        saveButton.innerHTML = `
                            <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                            </svg>
                        `;
                        
                        const response = await fetch('/api/chats/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                user_query: userQuery,
                                ai_response: data.response,
                                model_used: 'llama3.3',
                                support_level: data.support_level,
                                routing_reason: data.routing_reason
                            })
                        });
                        
                        if (response.ok) {
                            saveButton.innerHTML = `
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                            `;
                            setTimeout(() => {
                                saveButton.innerHTML = originalHTML;
                            }, 2000);
                        } else {
                            saveButton.innerHTML = originalHTML;
                            console.error('Failed to save chat');
                        }
                    } catch (err) {
                        console.error('Failed to save chat: ', err);
                        saveButton.innerHTML = originalHTML;
                    }
                });
                
                buttonsContainer.appendChild(copyButton);
                buttonsContainer.appendChild(saveButton);
                
                botBubble.appendChild(responseContainer);
                botBubble.appendChild(buttonsContainer);
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
