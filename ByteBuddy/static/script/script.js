var firstMessageSent = false;

function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    var chatBox = document.getElementById("chat-box");
    var introMessage = document.getElementById("intro-message");
    var quote = document.getElementById("quote");
    var byteBuddyLogo = document.getElementById("bytebuddy-logo");

    if (!firstMessageSent) {
        introMessage.remove();
        quote.remove();
        byteBuddyLogo.remove();
        firstMessageSent = true;
    }

    var userMessage = "<p><strong>You:</strong> " + userInput + "</p>";
    chatBox.innerHTML += userMessage;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        var botResponse = "<p><strong>Chatbot:</strong> " + data.message + "</p>";
        chatBox.innerHTML += botResponse;

        if (data.message === "I don't know the answer yet. Can you teach me?") {
            var newAnswer = prompt("Type the answer or 'skip' to skip:");
            if (newAnswer.toLowerCase() !== 'skip') {
                fetch("/learn", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question: userInput, answer: newAnswer })
                }).then(response => {
                    chatBox.innerHTML += "<p><strong>Chatbot:</strong> Thank you! I learned a new response.</p>";
                });
            }
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });

    document.getElementById("user-input").value = "";
}

function logout() {
    window.location.href = "{{ url_for('logout') }}";
}

function redirectToHelp() {
    window.location.href = "/help";
}

function openNav() {
    document.getElementById("mySidepanel").style.width = "250px";
    document.getElementById("chat-container").classList.add("opened");
    togglePanel();
}

function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
    document.getElementById("chat-container").classList.remove("opened");
    togglePanel();
}

function togglePanel() {
    var panel = document.getElementById("mySidepanel");
    var button = document.getElementById("openbtn");
    var panelWidth = window.getComputedStyle(panel).getPropertyValue("width");

    if (panelWidth === "250px") {
        button.style.display = "block";
    } else {
        button.style.display = "none";
    }
}
