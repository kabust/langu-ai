function checkValue() {
    let submitSelectedLanguages = document.getElementById('submitSelectedLanguages');
    let languageNative = document.getElementById('languageNative');
    let languageToLearn = document.getElementById('languageToLearn');

    if (languageNative.value != '1' && languageToLearn.value != '1') {
        submitSelectedLanguages.disabled = false;
    } else {
        submitSelectedLanguages.disabled = true;
    }

    for (let i = 1; i <= languageNative.options.length; i++) {
        document.querySelector(`#languageNative > option:nth-child(${i})`).disabled = false;
    }

    for (let i = 1; i <= languageToLearn.options.length; i++) {
        document.querySelector(`#languageToLearn > option:nth-child(${i})`).disabled = false;
    }

    if (languageToLearn.value != "1") {
        document.querySelector(`#languageNative > option:nth-child(${languageToLearn.value})`).disabled = true;
    }

    if (languageNative.value != "1") {
        document.querySelector(`#languageToLearn > option:nth-child(${languageNative.value})`).disabled = true;
    }
};


async function submitLanguagesSelection() {
    const languageNative = document.getElementById("languageNative");
    const languageToLearn = document.getElementById("languageToLearn");
    const languageNativeText = languageNative.options[languageNative.selectedIndex].text;
    const languageToLearnText = languageToLearn.options[languageToLearn.selectedIndex].text;

    const formData = new URLSearchParams();
    formData.append("languageNative", languageNativeText);
    formData.append("languageToLearn", languageToLearnText);

    try {
        const response = await fetch("http://127.0.0.1:8000/set_languages", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (response.ok) {
            swapIndexElems();
        } else {
            alert("Couldn't set languages for your profile, try to re-login.");
        }
    } catch (error) {
        console.error("Error logging in:", error);
        alert("Error during login. Please try again later");
    }
}


async function swapIndexElems() {
    const indexInit = document.getElementById("index-init");
    const indexStart = document.getElementById("index-start");

    indexInit.animate([
        // key frames
        { transform: 'translateX(0px)', opacity: 1 },
        { transform: 'translateX(-400px)', opacity: 0 }
    ], {
        // sync options
        duration: 700,
        iterations: 1
    });

    await new Promise(r => setTimeout(r, 700));

    indexInit.hidden = true;
    indexStart.hidden = false;

    indexStart.animate([
        // key frames
        { transform: 'translateX(400px)', opacity: 0 },
        { transform: 'translateX(0px)', opacity: 1 }
    ], {
        // sync options
        duration: 700,
        easing: 'ease-out',
        iterations: 1
    });
}


async function initLesson() {
    let audioCtx;
    let buffer;
    let source;

    const startBtn = document.getElementById("startBtn");
    startBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/></svg>';
    const play = document.getElementById("play");
    const message = document.getElementById("streamMessage")
    message.style.display = "none";
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        try {
            // Load an audio file
            const response = await fetch("/gpt/init_lesson", {
                headers: { "Accept": "audio/mpeg" }
            });

            if (!response.ok) {
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }

            const contentType = response.headers.get("content-type");
            if (!contentType.includes("audio")) {
                throw new Error(`Received invalid content instead of audio! (${contentType})`);
            }

            // Decode it
            const arrayBuffer = await response.arrayBuffer();
            buffer = await audioCtx.decodeAudioData(arrayBuffer);

            // Show message
            message.innerHTML = response.headers.get("X-Message");
            message.style.display = "block";
        } catch (err) {
            console.error(`Unable to fetch the audio file. Error: ${err.message}`);
            alert("Error during getting a response from OpenAI. Try again later.");
        }
    }
    // startBtn.id = "record";
    startBtn.setAttribute("onclick", "recordClip()");
    source = audioCtx.createBufferSource();
    source.buffer = buffer;
    source.connect(audioCtx.destination);
    source.start();
    play.disabled = true;
}


window.addEventListener('load', async function () {
    const response = await fetch("/get_languages");
    const data = await response.json();
    console.log(data);

    if (response.ok && data && data.languageNative && data.languageToLearn) {
        const indexInit = document.getElementById("index-init");
        const indexStart = document.getElementById("index-start");

        indexInit.hidden = true;
        indexStart.hidden = false;
    }
})
