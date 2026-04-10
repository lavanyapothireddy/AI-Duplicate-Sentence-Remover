async function removeDuplicates() {

    const text = document.getElementById("textInput").value;

    document.getElementById("outputBox").innerText = "Processing...";

    try {
        const response = await fetch("https://parabola-unwomanly-promoter.ngrok-free.dev/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            },
            body: JSON.stringify({
                text: text,
                threshold: 0.8
            })
        });

        const data = await response.json();

        document.getElementById("outputBox").innerText = data.cleaned_text;

    } catch (error) {
        document.getElementById("outputBox").innerText = "Error connecting to API";
    }
}