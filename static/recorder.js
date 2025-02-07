let audioCtx;
let buffer;
let source;

let mediaRecorder;
let chunks = [];

const soundClips = document.querySelector(".sound-clips");

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    console.log("getUserMedia supported.");

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (e) => {
                chunks.push(e.data);
            };

            mediaRecorder.onstop = () => {
                console.log("Recorder stopped");

                const startBtn = document.getElementById("startBtn");
                const play = document.getElementById("play");
                const message = document.getElementById("streamMessage");
                const loader = document.getElementById("loader");
                loader.hidden = false;

                const blob = new Blob(chunks, { type: "audio/mpeg;" });
                const file = new File([blob], "recording.mp3", { type: "audio/mpeg;" });
                const formData = new FormData();
                formData.append("file", file);
                startBtn.disabled = true;
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                };
                fetch("/gpt/prepare_answer", {
                    method: "POST",
                    body: formData
                })
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }

                        const contentType = response.headers.get("content-type");
                        if (!contentType.includes("audio")) {
                            throw new Error(`Received invalid content instead of audio! (${contentType})`);
                        }
                        message.style.display = "none";
                        message.innerHTML = decodeURIComponent(response.headers.get("X-Message"));
                        return response.arrayBuffer();
                    })
                    .then(arrayBuffer => audioCtx.decodeAudioData(arrayBuffer))
                    .then(buffer => {
                        message.style.display = "block";
                        startBtn.disabled = false;
                        source = audioCtx.createBufferSource();
                        source.buffer = buffer;
                        source.connect(audioCtx.destination);
                        source.start();
                        play.disabled = true;
                        loader.hidden = true;
                    });
            }
        })
        .catch((err) => {
            console.error(`The following getUserMedia error occurred: ${err}`);
        });
} else {
    console.error("getUserMedia not supported on your browser!");
}


function recordClip() {
    if (!mediaRecorder) {
        console.error("MediaRecorder is not initialized yet.");
        return;
    }

    const startStopButton = document.getElementById("startBtn");
    startStopButton.classList.remove("btn-primary");
    startStopButton.classList.add("btn-danger");
    mediaRecorder.start();
    console.log(mediaRecorder.state);
    startStopButton.style.background = "red";
    startStopButton.style.color = "black";
    startStopButton.setAttribute("onclick", "stopClip()");
}


function stopClip() {
    if (!mediaRecorder) {
        console.error("MediaRecorder is not initialized yet.");
        return;
    }

    const startStopButton = document.getElementById("startBtn");
    startStopButton.classList.add("btn-primary");
    startStopButton.classList.remove("btn-danger");
    mediaRecorder.stop();
    console.log(mediaRecorder.state);
    startStopButton.style.background = "";
    startStopButton.style.color = "";
    startStopButton.setAttribute("onclick", "recordClip()");
}
