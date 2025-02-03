async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorAlert = document.getElementById("error-alert");

    if (!email || !password) {
        errorAlert.innerHTML = "Please enter both email and password";
        errorAlert.style.display = "block";
        return;
    }

    const formData = new URLSearchParams();
    formData.append("email", email);
    formData.append("password", password);

    try {
        const response = await fetch("http://127.0.0.1:8000/user/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (response.redirected) {
            window.location.href = response.url;
        } else {
            const data = await response.json();
            
            if (Array.isArray(data.detail)) {
                data.detail.forEach(element => {
                    console.log(element);
                    errorAlert.innerHTML += element.msg + "<br>";
                });
            } else {
                errorAlert.innerHTML = data.detail;
            }
            errorAlert.style.display = "block";
        }
    } catch (error) {
        console.error("Error logging in:", error);
        alert("Error during login. Please try again later")
    }
}
