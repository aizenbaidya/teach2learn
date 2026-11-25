import "../../css/teach/index.css";

const teacherInput = document.getElementById("teacher-input");

async function sendMessage() {
    const teacherText = teacherInput.value.trim();
    teacherInput.disabled = true;
    if (!teacherText) return;

    const response = await fetch("/teach/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ teacherText }),
    });

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data.output_text;
}

if (teacherInput) {
    teacherInput.addEventListener("input", () => {
        teacherInput.style.height = "auto";
        teacherInput.style.height = teacherInput.scrollHeight + "px";
    });

    teacherInput.addEventListener("keydown", async (event) => {
        if (event.key == "Enter" && !event.shiftKey) {
            event.preventDefault();
            const outputText = await sendMessage();
            const studentResponse = document.getElementById("student-response");
            if (studentResponse) studentResponse.textContent = outputText;
            teacherInput.value = "";
            teacherInput.disabled = false;
            teacherInput.focus();
        }
    });
}
