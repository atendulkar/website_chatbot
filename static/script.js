function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  appendToChat("You: " + message);
  input.value = "";

  fetch("/ask", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ question: message })
  })
  .then(res => res.json())
  .then(data => appendToChat("Bot: " + data.answer))
  .catch(err => appendToChat("Bot: Error fetching response."));
}

function appendToChat(msg) {
  const chat = document.getElementById("chatbox");
  chat.innerHTML += `<div>${msg}</div>`;
  chat.scrollTop = chat.scrollHeight;
}
