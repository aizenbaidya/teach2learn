const eyeButton = document.getElementById("eye-button");
const passwordInput = document.getElementById("password-input");

eyeButton.addEventListener("click", () => {
    const show = passwordInput.type === "password";
    passwordInput.type = show ? "text" : "password";
});
