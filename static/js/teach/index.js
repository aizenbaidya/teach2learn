import cytoscape from "cytoscape";

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

    if (response.status === 403) {
        endForm.submit();
        return;
    }

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

const timer = document.getElementById("timer");
const endForm = document.getElementById("end-form");
let endsAt = null;

function formatTime(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = Math.floor(totalSeconds % 60);
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function syncTimer(remainingSeconds) {
    endsAt = Date.now() + remainingSeconds * 1000;
}

syncTimer(Number(timer.dataset.remainingSeconds));

let lastShown = null;

const timerInterval = setInterval(() => {
    if (endsAt === null) return;
    const left = Math.max(0, Math.ceil((endsAt - Date.now()) / 1000));
    if (left !== lastShown) {
        timer.textContent = formatTime(left);
        lastShown = left;
    }
    if (left === 0) {
        clearInterval(timerInterval);
        teacherInput.disabled = true;
        endForm.submit();
    }
}, 250);

// const kgButton = document.getElementById("knowledge-graph-button");
// const kgDialog = document.getElementById("knowledge-graph-dialog");
// kgButton.addEventListener("click", () => kgDialog.showModal());

// const todoListButton = document.getElementById("todo-list-button");
// const todoListDialog = document.getElementById("todo-list-dialog");
// todoListButton.addEventListener("click", () => todoListDialog.showModal());

const kgButton = document.getElementById("knowledge-graph-button");
const kgDialog = document.getElementById("knowledge-graph-dialog");
const kgContainer = document.getElementById("knowledge-graph");
const kgStatus = document.getElementById("knowledge-graph-status");
let cy = null;

async function loadKnowledgeGraph() {
    if (cy) {
        cy.resize();
        cy.fit();
        return;
    }

    kgStatus.textContent = "Simmering...";
    const response = await fetch("/teach/knowledge-graph");
    if (!response.ok) {
        kgStatus.textContent = `Error: ${response.status}`;
        return;
    }
    const data = await response.json();
    kgStatus.textContent = "";

    cy = cytoscape({
        container: kgContainer,
        elements: data.elements,
        style: [
            {
                selector: "node",
                style: {
                    label: "data(label)",
                    "background-color": "#209cee",
                    "font-family": "'Press Start 2P'",
                    "font-size": 8,
                    "text-valign": "bottom",
                    "text-margin-y": 4,
                },
            },
            {
                selector: "edge",
                style: {
                    label: "data(label)",
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                    width: 2,
                    "line-color": "#999",
                    "target-arrow-color": "#999",
                    "font-size": 6,
                    "text-rotation": "autorotate",
                    "text-background-color": "#fff",
                    "text-background-opacity": 1,
                },
            },
        ],
        layout: { name: "cose", animate: false, padding: 20 },
    });
}

kgButton.addEventListener("click", async () => {
    kgDialog.showModal();
    await loadKnowledgeGraph();
});
