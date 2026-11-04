from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Environment Client", version="1.0.0")

body_content = '''
<div class="card">
    <h2>Ministry of Tourism & Environment Console</h2>
    <div class="form-group">
        <label>Crossing Case Number</label>
        <input type="text" id="caseNum" value="CASE-2026-901">
    </div>
    <div class="form-group">
        <label>CITES / Wildlife Permit Decision</label>
        <select id="decision">
            <option value="APPROVED">APPROVED (Permit Valid)</option>
            <option value="HOLD">HOLD (Permit Verification Needed)</option>
            <option value="REJECTED">REJECTED (Invalid / Expired CITES)</option>
        </select>
    </div>
    <button onclick="submitDecision()">Report Environment Decision to Hub</button>
    <pre id="output">// Decision output...</pre>
</div>

<script>
    async function submitDecision() {
        try {
            const caseNum = document.getElementById('caseNum').value;
            const decision = document.getElementById('decision').value;
            const res = await fetch(`http://127.0.0.1:8002/cases/${caseNum}/clearances/environment`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    state: decision,
                    reasonCode: decision === 'APPROVED' ? 'PERMIT_VALID' : 'CITES_EXPIRED',
                    decidedBy: 'officer_environment'
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
    return render_client_page("Environment Officer Console", "#15803d", "Environment Officer", "Tourism & Environment", 8086, body_content)
