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


function disableBlank() {
    let blankOption = document.getElementById
}


function startLesson() {
    fetch('/start_lesson')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
}
