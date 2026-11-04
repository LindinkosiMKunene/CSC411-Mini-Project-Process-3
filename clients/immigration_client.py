from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Immigration Client", version="1.0.0")

body_content = '''
<div class="card">
    <h2>Home Affairs Immigration Officer Console</h2>
    <div class="form-group">
        <label>Crossing Case Number</label>
        <input type="text" id="caseNum" value="CASE-2026-901">
    </div>
    <div class="form-group">
        <label>Passport Number / Document Verification</label>
        <input type="text" id="passport" value="P999999">
    </div>
    <div class="form-group">
        <label>Immigration Clearance Decision</label>
        <select id="decision">
            <option value="APPROVED">APPROVED</option>
            <option value="HOLD">HOLD</option>
            <option value="REJECTED">REJECTED (Watchlist Hit)</option>
        </select>
    </div>
    <button onclick="submitDecision()">Report Immigration Decision to Hub</button>
    <pre id="output">// Decision output...</pre>
</div>

<script>
    async function submitDecision() {
        try {
            const caseNum = document.getElementById('caseNum').value;
            const decision = document.getElementById('decision').value;
            const res = await fetch(`http://127.0.0.1:8002/cases/${caseNum}/clearances/immigration`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    state: decision,
                    reasonCode: decision === 'APPROVED' ? 'CLEAR' : 'WATCHLIST_FLAG',
                    decidedBy: 'officer_home_affairs'
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
    return render_client_page("Immigration Officer Console (Home Affairs)", "#047857", "Immigration Officer", "Home Affairs", 8083, body_content)
