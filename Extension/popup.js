document.getElementById('checkBtn').addEventListener('click', async () => {
    let url = document.getElementById('urlInput').value;

    // If input is empty, use active tab URL
    if (!url) {
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        url = tab.url;
    }

    // Send URL to backend
    try {
        const response = await fetch('http://127.0.0.1:5000/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        // Show results
        document.getElementById('status').innerText = "Status: " + data.status;
        document.getElementById('risk').innerText = "Risk: " + data.risk_percentage + "%";

    } catch (error) {
        console.error(error);
        document.getElementById('status').innerText = "Error connecting to backend!";
    }
});
