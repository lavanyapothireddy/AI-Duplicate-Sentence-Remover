async function removeDuplicates() {
    const inputText = document.getElementById("inputText").value;

    if (!inputText) {
        alert("Please enter text");
        return;
    }

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

        document.getElementById("outputText").value = data.result;

    } catch (error) {
        console.error("Error:", error);
        alert("Error connecting to API");
    }
}
