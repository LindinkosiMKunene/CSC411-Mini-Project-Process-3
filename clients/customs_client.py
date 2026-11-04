from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Customs Client", version="1.0.0")

body_content = '''
<div class="card">
    <h2>ERS Customs Officer Console</h2>
    <div class="form-group">
        <label>Crossing Case Number</label>
        <input type="text" id="caseNum" value="CASE-2026-901">
    </div>
    <div class="form-group">
        <label>Customs Duty & Risk Assessment Decision</label>
        <select id="decision">
            <option value="APPROVED">APPROVED (Duty Paid & Released)</option>
            <option value="HOLD">HOLD (Inspection Required)</option>
            <option value="REJECTED">REJECTED (Contraband)</option>
        </select>
    </div>
    <button onclick="submitDecision()">Report Customs Decision to Hub</button>
    <pre id="output">// Decision output...</pre>
</div>

<script>
    async function submitDecision() {
        try {
            const caseNum = document.getElementById('caseNum').value;
            const decision = document.getElementById('decision').value;
            const res = await fetch(`http://127.0.0.1:8002/cases/${caseNum}/clearances/customs`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    state: decision,
                    reasonCode: decision === 'APPROVED' ? 'DUTY_PAID' : 'PHYSICAL_INSPECTION',
                    decidedBy: 'officer_ers'
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
    return render_client_page("Customs Officer Console (ERS)", "#b45309", "Customs Officer", "ERS", 8084, body_content)
