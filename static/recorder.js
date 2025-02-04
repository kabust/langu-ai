let mediaRecorder;
let chunks = [];

const soundClips = document.querySelector(".sound-clips");

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    console.log("getUserMedia supported.");

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            mediaRecorder = new MediaRecorder(stream);

            // ✅ Attach event listeners *inside* the promise after initialization
            mediaRecorder.ondataavailable = (e) => {
                chunks.push(e.data);
            };

            mediaRecorder.onstop = () => {
                console.log("Recorder stopped");

                const blob = new Blob(chunks, { type: "audio/mpeg; codecs=opus" });
                // const formData = new URLSearchParams();
                // formData.append("file", blob);
                fetch("/gpt/process_recording", {
                    method: "POST",
                    headers: { "Content-Type": "audio/mpeg" },
                    body: {"file": blob}
                })
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }

                        return response.blob();
                    });
            };
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
    console.log("Recorder started");
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
    console.log("Recorder stopped");
    startStopButton.style.background = "";
    startStopButton.style.color = "";
    startStopButton.setAttribute("onclick", "recordClip()");
}
