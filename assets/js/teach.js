const myDiv = document.getElementById("my-div");

const response = await fetch("/api/chat", {
    method: "POST",
});
const data = await response.json();

myDiv.textContent = data.text;
