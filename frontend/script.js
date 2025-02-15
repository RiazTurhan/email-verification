document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("mail");
    const checkButton = document.querySelector(".button");
    const resultText = document.querySelector(".right p");
    const progressBar = document.querySelector(".round");

    checkButton.addEventListener("click", async function () {
        const email = emailInput.value.trim();

        if (!email) {
            resultText.textContent = "Please enter an email address.";
            progressBar.style.backgroundColor = "red";
            return;
        }

        resultText.textContent = "Checking...";
        progressBar.style.backgroundColor = "orange"; // Indicate processing

        try {
            const response = await fetch(`http://127.0.0.1:8000/check-email/?email=${encodeURIComponent(email)}`);
            const data = await response.json();

            if (response.ok) {
                if (data.status === "success") {
                    resultText.textContent = "✅ Yes, the email address exists!";
                    progressBar.style.backgroundColor = "green"; // Email exists
                } else {
                    resultText.textContent = "❌ No, the email address does not exist.";
                    progressBar.style.backgroundColor = "red"; // Email doesn't exist
                }
            } else {
                resultText.textContent = `Error: ${data.detail}`;
                progressBar.style.backgroundColor = "red";
            }
        } catch (error) {
            resultText.textContent = "Error checking email. Please try again.";
            progressBar.style.backgroundColor = "red";
        }
    });
});
