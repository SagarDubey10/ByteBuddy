document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const introSection = document.getElementById('intro-message');
    const sendBtn = document.getElementById('send-button');
    const sidePanel = document.getElementById('mySidepanel');
    const openBtn = document.getElementById('toggleButton');
    const quote = document.getElementById('quote');
    const logo = document.getElementById('company-logo');

    var firstMessageSent = false;

    // Toggle event handler
    openBtn.addEventListener('click', function () {
        toggleNav();  // Use toggleNav function
    });

    function toggleNav() {
        sidePanel.classList.toggle('open');
        document.querySelector('.chat-container').classList.toggle('opened');

        // Change icon
        if (sidePanel.classList.contains('open')) {
            openBtn.innerHTML = '&larr;';  // Left arrow when open
        } else {
            openBtn.innerHTML = '☰';       // Hamburger when closed
        }
    }

    function openNav() {
        sidePanel.classList.add('open');
        document.querySelector('.chat-container').classList.add('opened');
    }

    function appendMessage(content, sender) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('message-wrapper', sender); // user or bot

        const messageDiv = document.createElement('div');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        messageDiv.innerText = content;

        wrapper.appendChild(messageDiv);
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function botTypingAnimation() {
        const wrapper = document.createElement('div');
        wrapper.classList.add('message-wrapper', 'bot');

        const typingDiv = document.createElement('div');
        typingDiv.classList.add('bot-message', 'typing');
        typingDiv.textContent = "Byte Buddy is typing...";

        wrapper.appendChild(typingDiv);
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;

        return wrapper; // return the entire wrapper so it can be removed later
    }

    function sendMessage() {
        var userInputText = userInput.value.trim();
        if (userInputText === "") return;

        if (!firstMessageSent) {
            introSection.style.display = 'none';
            quote.classList.add('hidden');
            logo.style.display = 'none';
            firstMessageSent = true;
        }

        appendMessage(userInputText, 'user');
        userInput.value = "";
        const typingDiv = botTypingAnimation();

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userInputText })
        })
            .then(response => response.json())
            .then(data => {
                typingDiv.remove();  // Remove typing animation
                appendMessage(data.message, 'bot');  // Display bot's message

                // If the bot doesn't know the answer, prompt user to teach
                if (data.message === "I don't know the answer yet. Can you teach me?") {
                    var newAnswer = prompt("Type the answer or 'skip' to skip:");
                    if (newAnswer.toLowerCase() !== 'skip') {
                        fetch("/learn", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ question: userInputText, answer: newAnswer })
                        }).then(response => {
                            appendMessage("Thank you! I learned a new response.", 'bot');
                        });
                    }
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    // Logout function
    function logout() {
        window.location.href = "{{ url_for('logout') }}";
    }

    // Redirect to help page
    function redirectToHelp() {
        window.location.href = "/help";
    }
});
