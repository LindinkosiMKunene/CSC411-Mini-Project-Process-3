from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Foreign Agency Adapter Client", version="1.0.0")

body_content = '''
<div class="card">
    <h2>Foreign Agency Gateway (SARS / Mozambique)</h2>
    <div class="form-group">
        <label>Crossing Case Number</label>
        <input type="text" id="caseNum" value="CASE-2026-901">
    </div>
    <div class="form-group">
        <label>Destination Country</label>
        <select id="dest">
            <option value="SOUTH_AFRICA">South Africa (SARS)</option>
            <option value="MOZAMBIQUE">Mozambique</option>
        </select>
    </div>
    <button onclick="sendNotice()">Dispatch Pre-Arrival / Clearance Notice</button>
    <pre id="output">// Notice status output...</pre>
</div>

<script>
    async function sendNotice() {
        try {
            const res = await fetch('http://127.0.0.1:8007/notices', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    caseNumber: document.getElementById('caseNum').value,
                    noticeType: 'CLEARANCE_RELEASE',
                    destinationCountry: document.getElementById('dest').value
                })
            });
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        } catch(err) {
            document.getElementById('output').innerText = "Error: " + err.message;
        }
    }
</script>
'''

@app.get("/", response_class=HTMLResponse)
def index():
    return render_client_page("Foreign Agency Gateway (SARS / Mozambique)", "#475569", "Adapter", "Foreign Agencies", 8087, body_content)
