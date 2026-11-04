from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Clearing Agent Portal", version="1.0.0")

body_content = '''
<div class="card">
    <h2>Agent Customs Declaration Portal</h2>
    <div class="form-group">
        <label>Declaration Number</label>
        <input type="text" id="decNum" value="DEC-2026-88">
    </div>
    <div class="form-group">
        <label>Kind</label>
        <select id="kind">
            <option value="COMMERCIAL">COMMERCIAL</option>
            <option value="PERSONAL">PERSONAL</option>
        </select>
    </div>
    <div class="form-group">
        <label>Agent Name</label>
        <input type="text" id="agent" value="Eswatini Express Logistics">
    </div>
    <div class="form-group">
        <label>Vehicle Registration</label>
        <input type="text" id="vehReg" value="BSD-901-BH">
    </div>
    <button onclick="submitDec()">Submit Customs Declaration</button>
    <pre id="output">// Declaration status output...</pre>
</div>

<script>
    async function submitDec() {
        try {
            const res = await fetch('http://127.0.0.1:8004/declarations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    declarationNumber: document.getElementById('decNum').value,
                    kind: document.getElementById('kind').value,
                    agent: document.getElementById('agent').value,
                    vehicleReg: document.getElementById('vehReg').value,
                    items: [
                        { description: "Agricultural Fertilizer", tariffCode: "3102.10", quantity: 50, value: 200, regulated: true }
                    ]
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
    return render_client_page("Clearing Agent & Transporter Portal", "#0284c7", "Agent", "Public / Agents", 8080, body_content)
