import "../css/teach.css";

const userInput = document.getElementById("user-input");
const aiResponse = document.getElementById("ai-response");

userInput.addEventListener("keydown", async (e) => {
    if (e.key !== "Enter" || e.shiftKey) return;
    e.preventDefault();

    userInput.contentEditable = false;
    const inputText = userInput.textContent;

    const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ inputText }),
    });
    const data = await response.json();
    aiResponse.textContent = data.output_text;

    userInput.textContent = "";
    userInput.contentEditable = true;
    userInput.focus();
});
