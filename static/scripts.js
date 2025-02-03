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


function startLesson() {
    fetch('/start_lesson')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
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
