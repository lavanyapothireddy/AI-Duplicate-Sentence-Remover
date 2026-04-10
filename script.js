async function removeDuplicates() {
    const inputText = document.getElementById("inputText").value;

    document.getElementById("outputText").value = "Processing...";

    try {
        const response = await fetch("https://ai-duplicate-sentence-remover-1.onrender.com/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: inputText,
                threshold: 0.8
            })
        });

        const data = await response.json();

        document.getElementById("outputText").value = data.cleaned_text;

    } catch (error) {
        document.getElementById("outputText").value = "Error connecting to API";
    }
}
