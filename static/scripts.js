function checkValue() {
    let startBtn = document.getElementById('startBtn');
    let languageSelected = document.getElementById('languages');
    let dropdownSelector = document.getElementById('dropdownSelector');

    if (languageSelected.value != 'blank') {
        startBtn.disabled = false;
        dropdownSelector.setAttribute('hidden', '');
    } else {
        startBtn.disabled = true;
    }
};
