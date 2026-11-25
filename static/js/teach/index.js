import "../../css/teach/index.css";

const teacherInput = document.getElementById("teacher-input");
if (teacherInput) {
    teacherInput.addEventListener("input", () => {
        teacherInput.style.height = "auto";
        teacherInput.style.height = teacherInput.scrollHeight + "px";
    });
}
