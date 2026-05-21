const chat =
document.getElementById("chatContainer");

/* Load Chats */

async function loadChats(){

    let response =
    await fetch("/get_chats");

    let data =
    await response.json();

    let list =
    document.getElementById("chatList");

    list.innerHTML = "";

    // Loop Chats

    Object.keys(data.chats).forEach(chatName => {

        let messages =
        data.chats[chatName];

        // First User Message

        let firstUserMessage =
        messages.find(
            msg => msg.role === "user"
        );

        let displayName =
        firstUserMessage
        ? firstUserMessage.content
        : chatName;

        list.innerHTML += `
        <div class="chat-item"
            onclick="switchChat('${chatName}')">

            ${displayName}

        </div>
        `;
    });

    showMessages(data.messages);
}


/* Show Messages */

function showMessages(messages){

    chat.innerHTML = "";

    messages.forEach(msg => {

        chat.innerHTML += `
        <div class="${
            msg.role === "user"
            ? "user-message"
            : "bot-message"
        }">

            ${msg.content}

        </div>
        `;
    });

    // Auto Scroll

    chat.scrollTop =
    chat.scrollHeight;
}

/* Send Message */

async function sendMessage(){

    let input =
    document.getElementById("userInput");

    let message =
    input.value.trim();

    if(message === "") return;

    input.value = "";

    // Send message to Flask AI route
    let response = await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message
        })
    });

    // Get AI response
    let data = await response.json();

    // Save chat to Firebase
    await fetch("/save_chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            user:message,
            ai:data.response
        })
    });

    // Reload chats
    loadChats();
}

/* New Chat */

async function newChat(){

    await fetch("/new_chat",{
        method:"POST"
    });

    loadChats();
}

/* Switch Chat */

async function switchChat(chatName){

    let response =
    await fetch("/switch_chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            chat:chatName
        })
    });

    let data =
    await response.json();

    showMessages(data.messages);
}

/* Voice Input */

function startVoice(){

    let recognition =
    new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult = function(event){

        document.getElementById("userInput")
        .value =
        event.results[0][0].transcript;
    };
}

/* Enter Key */

document
.getElementById("userInput")
.addEventListener("keydown", function(e){

    if(e.key === "Enter"){

        e.preventDefault();

        sendMessage();
    }
});
fetch("/save_chat", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        user: userMessage,
        ai: aiReply
    })
})

/* Start */

loadChats();