from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Port Health Client", version="1.0.0")

body_content = '''
<div class="card">
    <h2>Ministry of Health Port Health Console</h2>
    <div class="form-group">
        <label>Crossing Case Number</label>
        <input type="text" id="caseNum" value="CASE-2026-901">
    </div>
    <div class="form-group">
        <label>Health Screening Decision</label>
        <select id="decision">
            <option value="APPROVED">APPROVED (Health Clear)</option>
            <option value="HOLD">HOLD (Quarantine Required)</option>
            <option value="REJECTED">REJECTED (Contagion Flag)</option>
        </select>
    </div>
    <button onclick="submitDecision()">Report Port Health Decision to Hub</button>
    <pre id="output">// Decision output...</pre>
</div>

<script>
    async function submitDecision() {
        try {
            const caseNum = document.getElementById('caseNum').value;
            const decision = document.getElementById('decision').value;
            const res = await fetch(`http://127.0.0.1:8002/cases/${caseNum}/clearances/health`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    state: decision,
                    reasonCode: decision === 'APPROVED' ? 'TEMP_NORMAL' : 'QUARANTINE_ORDER',
                    decidedBy: 'officer_health'
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
    return render_client_page("Port Health Officer Console", "#4338ca", "Port Health Officer", "Ministry of Health", 8085, body_content)
