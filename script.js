const API_URL = "https://ai-duplicate-sentence-remover-1.onrender.com";

/* ── Utility: count sentences in a string ── */
function countSentences(text) {
    if (!text || !text.trim()) return 0;
    const parts = text.trim().split(/(?<=[.!?])\s+/);
    return parts.filter(s => s.trim().length > 0).length;
}

/* ── Live input counter ── */
const inputTextarea = document.getElementById("inputText");
const inputMeta     = document.getElementById("inputMeta");

inputTextarea.addEventListener("input", () => {
    const n = countSentences(inputTextarea.value);
    inputMeta.textContent = n === 1 ? "1 sentence" : `${n} sentences`;
});

/* ── FEATURE: FILE UPLOAD ── */
document.getElementById("fileInput").addEventListener("change", async function () {
    const file = this.files[0];
    const fileNameDisplay = document.getElementById("fileNameDisplay");

    if (!file) return;

    fileNameDisplay.className = "loading";
    fileNameDisplay.textContent = "⏳ Reading " + file.name + "…";
    inputTextarea.value = "";
    inputMeta.textContent = "—";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/read-file`, {
            method: "POST",
            body: formData
        });

        if (response.status === 404) {
            inputTextarea.value = "Error 404: /read-file route not found on backend.";
            fileNameDisplay.className = "";
            fileNameDisplay.textContent = "❌ Route missing";
            return;
        }

        const data = await response.json();

        if (data.text) {
            inputTextarea.value = data.text;
            fileNameDisplay.className = "success";
            fileNameDisplay.textContent = "✅ " + file.name;
            // Trigger live counter
            const n = countSentences(data.text);
            inputMeta.textContent = n === 1 ? "1 sentence" : `${n} sentences`;
        } else {
            inputTextarea.value = "Extraction failed: " + (data.result || "Unknown error");
            fileNameDisplay.className = "";
            fileNameDisplay.textContent = "❌ Failed";
        }
    } catch (err) {
        console.error("Fetch Error:", err);
        inputTextarea.value = "Connection failed. Make sure the Render service is live.";
        fileNameDisplay.className = "";
        fileNameDisplay.textContent = "❌ Connection error";
    }
});

/* ── FEATURE: REMOVE DUPLICATES ── */
async function removeDuplicates() {
    const inputVal  = inputTextarea.value.trim();
    const outputBox = document.getElementById("outputText");
    const outputMeta = document.getElementById("outputMeta");
    const removedCount = document.getElementById("removedCount");
    const btn = document.getElementById("processBtn");

    if (!inputVal || inputVal.startsWith("Reading file")) {
        outputBox.value = "Please enter text or upload a file first.";
        return;
    }

    // Loading state
    btn.classList.add("loading");
    btn.innerHTML = '<span class="btn-icon">⏳</span> Processing…';
    outputBox.value = "";
    outputMeta.textContent = "Working…";
    removedCount.textContent = "…";
    removedCount.className = "stat-value";

    const formData = new FormData();
    formData.append("text", inputVal);

    try {
        const response = await fetch(`${API_URL}/process`, {
            method: "POST",
            body: formData
        });

        if (response.status === 404) {
            outputBox.value = "Error 404: /process route not found on backend.";
            resetBtn();
            return;
        }

        const data = await response.json();

        if (data.result) {
            outputBox.value = data.result;

            const inCount  = countSentences(inputVal);
            const outCount = countSentences(data.result);
            const diff     = Math.max(0, inCount - outCount);

            // Update stat chip
            removedCount.textContent = diff;
            removedCount.className   = diff > 0 ? "stat-value positive" : "stat-value";

            // Update output panel meta
            outputMeta.textContent = `${outCount} sentences · ${diff} duplicate${diff !== 1 ? "s" : ""} removed`;
        } else {
            outputBox.value = "No result returned from the server.";
            outputMeta.textContent = "—";
        }
    } catch (err) {
        console.error("Processing Error:", err);
        outputBox.value = "Connection Error: The backend might be sleeping. Try again in a moment.";
        outputMeta.textContent = "—";
    } finally {
        resetBtn();
    }
}

function resetBtn() {
    const btn = document.getElementById("processBtn");
    btn.classList.remove("loading");
    btn.innerHTML = '<span class="btn-icon">⚡</span> Remove Duplicates';
}

/* ── FEATURE: COPY OUTPUT ── */
function copyOutput() {
    const text = document.getElementById("outputText").value;
    if (!text || text === "Clean output will appear here…") return;

    navigator.clipboard.writeText(text).then(() => {
        const btn = document.querySelector(".copy-btn");
        btn.textContent = "✅ Copied!";
        setTimeout(() => { btn.innerHTML = "📋 Copy"; }, 2000);
    });
}
