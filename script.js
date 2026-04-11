// 1. SET YOUR API URL
// Make sure this matches your Render URL exactly. 
// Do NOT put a "/" at the end.
const API_URL = "https://ai-duplicate-sentence-remover-1.onrender.com";

/**
 * FEATURE 1: FILE PREVIEW
 * When a user selects a PDF, Word, or PPTX file, this code 
 * sends it to the backend and puts the text into the INPUT box.
 */
document.getElementById('fileInput').addEventListener('change', async function() {
    const file = this.files[0];
    const inputText = document.getElementById("inputText");
    const fileNameDisplay = document.getElementById("fileNameDisplay");

    if (!file) return;

    // UI Feedback
    fileNameDisplay.innerText = "⏳ Extracting: " + file.name;
    inputText.value = "Reading file content... please wait.";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/read-file`, {
            method: "POST",
            body: formData
        });

        // Handle 404 or other server errors
        if (response.status === 404) {
            alert("Error 404: The endpoint /read-file was not found. Check your main.py routes.");
            inputText.value = "";
            return;
        }

        const data = await response.json();

        if (data.text) {
            inputText.value = data.text; // Text appears in the box
            fileNameDisplay.innerText = "✅ Loaded: " + file.name;
        } else {
            inputText.value = "Error: " + (data.result || "Could not read file.");
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        inputText.value = "Connection failed. Check if the backend is 'Live' on Render.";
        alert("Network Error: Could not connect to the API.");
    }
});

/**
 * FEATURE 2: REMOVE DUPLICATES
 * Takes the text currently visible in the input box, 
 * cleans it, and puts it in the output box.
 */
async function removeDuplicates() {
    const inputText = document.getElementById("inputText").value;
    const outputBox = document.getElementById("outputText");

    if (!inputText || inputText.startsWith("Reading file")) {
        alert("Please enter text or wait for the file to finish loading.");
        return;
    }

    outputBox.value = "⏳ Processing duplicates...";

    const formData = new FormData();
    formData.append("text", inputText);

    try {
        const response = await fetch(`${API_URL}/process`, {
            method: "POST",
            body: formData
        });

        if (response.status === 404) {
            alert("Error 404: The endpoint /process was not found.");
            outputBox.value = "";
            return;
        }

        const data = await response.json();

        if (data.result) {
            outputBox.value = data.result;
        } else {
            outputBox.value = "Processing complete, but no result returned.";
        }

    } catch (error) {
        console.error("Processing Error:", error);
        outputBox.value = "Error: Could not connect to API.";
    }
}
