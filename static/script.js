const socket = io("https://chatapp-production-2659.up.railway.app");
// Username set karein jab connect ho
const username = "User_" + Math.floor(Math.random() * 1000);
document.getElementById("display-name").textContent = username;

socket.on("connect", () => {
    socket.emit("join", username);
});

// Message receive hone par bubble banayein
socket.on("response", function(data) {
    const messages = document.getElementById('messages');
    
    // Naya div banayein bubble styling ke saath
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('bubble', data.type); // 'sent' ya 'received' class add hogi
    
    messageDiv.innerHTML = `
        <span class="name">${data.name}</span>
        ${data.msg}
    `;
    
    messages.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    messages.scrollTop = messages.scrollHeight;
});

function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById("messageText");
    if (input.value.trim() !== "") {
        socket.emit("chat_message", { msg: input.value });
        input.value = '';
    }
}