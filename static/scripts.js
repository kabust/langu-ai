function checkValue() {
    let startBtn = document.getElementById('startBtn');
    let originalLangSelected = document.getElementById('languages');
    let learningLangLangSelected = document.getElementById('languages');
    let dropdownSelector = document.getElementById('dropdownSelector');

    if (languageSelected.value != 'blank') {
        startBtn.disabled = false;
        startBtn.removeAttribute('hidden');
        startBtn.setAttribute('originalLang', originalLangSelected.value)
        startBtn.setAttribute('learningLang', learningLangLangSelected.value)
        dropdownSelector.setAttribute('hidden', '');
    } else {
        startBtn.disabled = true;
    }
};


function startLesson() {
    fetch('/start_lesson')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}
