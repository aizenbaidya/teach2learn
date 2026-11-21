// import ""
import "../../css/auth/auth-base.css"

const eyeButton = document.getElementById("eye-button");

eyeButton.addEventListener("click", () => {
    const passwordInput = document.getElementById("password-input");
    const eyeIcon = document.getElementById("eye-icon");
    const show = passwordInput.type === "password";

    passwordInput.type = show ? "text" : "password";
    eyeIcon.classList.toggle("eye", !show);
    eyeIcon.classList.toggle("eye-slash", show);
});
