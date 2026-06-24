// BangLense — "Listen in Bangla" using the browser's built-in speech.
// No backend, no cost. Reads the on-screen Bangla text aloud.

(function () {
    const button = document.getElementById('listen-btn');
    const label = document.getElementById('listen-label');
    if (!button) return;

    // Collect all the Bangla text on the page (explanation + what to do).
    const parts = document.querySelectorAll('.bangla-text');
    let textToRead = '';
    parts.forEach(function (p) {
        textToRead += p.textContent.trim() + '. ';
    });

    // If the browser can't do speech, hide the button gracefully.
    if (!('speechSynthesis' in window)) {
        button.style.display = 'none';
        return;
    }

    let speaking = false;

    function pickBengaliVoice() {
        const voices = window.speechSynthesis.getVoices();
        // Prefer Bangladeshi voice, then any Bengali voice, else use default.
        return (
            voices.find(function (v) { return v.lang === 'bn-BD'; }) ||
            voices.find(function (v) { return v.lang && v.lang.indexOf('bn') === 0; }) ||
            null
        );
    }

    function speak() {
        const utterance = new SpeechSynthesisUtterance(textToRead);
        utterance.lang = 'bn-BD';
        const voice = pickBengaliVoice();
        if (voice) utterance.voice = voice;
        utterance.rate = 0.9;  // slightly slower — kinder for elderly listeners

        utterance.onend = function () {
            speaking = false;
            label.textContent = 'Listen in Bangla';
        };

        window.speechSynthesis.cancel();  // stop anything already playing
        window.speechSynthesis.speak(utterance);
        speaking = true;
        label.textContent = 'Stop';
    }

    // Toggle: tap once to listen, tap again to stop.
    button.addEventListener('click', function () {
        if (speaking) {
            window.speechSynthesis.cancel();
            speaking = false;
            label.textContent = 'Listen in Bangla';
        } else {
            speak();
        }
    });

    // Some browsers load voices asynchronously — this nudges them.
    window.speechSynthesis.onvoiceschanged = pickBengaliVoice;

})();
