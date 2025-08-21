const btn = document.querySelector('.talk');
const content = document.querySelector('.content');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.onstart = function () {
    content.textContent = "Listening...";
};

recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    content.textContent = `You said: "${transcript}"`;

    fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: transcript })
    })
    .then(res => res.json())
    .then(data => {
        const utterance = new SpeechSynthesisUtterance(data.response);
        speechSynthesis.speak(utterance);
    });
};

btn.addEventListener('click', () => {
    recognition.start();
});
