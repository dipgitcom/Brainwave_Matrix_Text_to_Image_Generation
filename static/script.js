function generateImage() {
    const prompt = document.getElementById("prompt").value;
    if (!prompt) {
        alert("Please enter a prompt!");
        return;
    }

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_url) {
            document.getElementById("generatedImage").src = data.image_url;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}
