// Easter egg :)
const eatingSound = new Audio("static/audio/eating.mp3");
document.getElementById("apple").addEventListener("click", () => {
    eatingSound.currentTime = 0;
    eatingSound.play();
});
