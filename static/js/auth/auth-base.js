import "../../css/auth/auth-base.css";

const eyeButton = document.getElementById("eye-button");
if (eyeButton) {
    eyeButton.addEventListener("click", () => {
        const passwordInput = document.getElementById("password-input");
        const eyeIcon = document.getElementById("eye-icon");
        const show = passwordInput.type === "password";

        passwordInput.type = show ? "text" : "password";
        eyeIcon.classList.toggle("eye", !show);
        eyeIcon.classList.toggle("eye-slash", show);
    });
}

function setError(box, message, hasError) {
    box.classList.toggle("is-error", hasError);
    message.classList.toggle("d-none", !hasError);
}

const authForm = document.getElementById("auth-form");
if (authForm) {
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");

    authForm.addEventListener("submit", (event) => {
        const usernameValid = usernameInput.checkValidity();
        const passwordValid = passwordInput.checkValidity();

        setError(usernameInput, usernameError, !usernameValid);
        setError(passwordInput, passwordError, !passwordValid);

        if (!usernameValid) {
            event.preventDefault();
            usernameInput.focus();
        } else if (!passwordValid) {
            event.preventDefault();
            passwordInput.focus();
        }
    });

    usernameInput.addEventListener("input", () => {
        if (usernameInput.checkValidity()) {
            setError(usernameInput, usernameError, false);
        }
    });

    passwordInput.addEventListener("input", () => {
        if (passwordInput.checkValidity()) {
            setError(passwordInput, passwordError, false);
        }
    });
}
