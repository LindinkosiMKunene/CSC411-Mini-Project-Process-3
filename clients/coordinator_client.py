from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from clients.common import render_client_page

app = FastAPI(title="Coordinator Hub Console", version="1.0.0")

body_content = '''
<div class="card">
    <h2>1. Create Integrated Crossing Case</h2>
    <div class="form-group">
        <label>Case Number</label>
        <input type="text" id="caseNum" value="CASE-2026-901">
    </div>
    <div class="form-group">
        <label>Border Post</label>
        <select id="post">
            <option value="NGWENYA">Ngwenya</option>
            <option value="MAHAMBA">Mahamba</option>
            <option value="LOMAHASHA">Lomahasha</option>
        </select>
    </div>
    <div class="form-group">
        <label>Direction & Case Type</label>
        <select id="dir">
            <option value="ENTRY">ENTRY</option>
            <option value="EXIT">EXIT</option>
        </select>
    </div>
    <button onclick="createCase()">Create Crossing Case</button>
</div>

<div class="card">
    <h2>2. Case Release Rule Evaluator</h2>
    <div class="form-group">
        <label>Case Number</label>
        <input type="text" id="checkCaseNum" value="CASE-2026-901">
    </div>
    <button onclick="checkCase()">Check Combined Case Status</button>
    <pre id="output">// Combined case status...</pre>
</div>

<script>
    async function createCase() {
        try {
            const res = await fetch('http://127.0.0.1:8002/cases', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    caseNumber: document.getElementById('caseNum').value,
                    post: document.getElementById('post').value,
                    direction: document.getElementById('dir').value,
                    caseType: "BOTH",
                    travellerId: "TR-8821",
                    declarationNumber: "DEC-2026-88"
                })
            });
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        } catch(err) {
            document.getElementById('output').innerText = "Error: " + err.message;
        }
    }

    async function checkCase() {
        try {
            const caseNum = document.getElementById('checkCaseNum').value;
            const res = await fetch(`http://127.0.0.1:8002/cases/${caseNum}`);
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
    return render_client_page("Border Coordinator Hub Console", "#1e3a8a", "Coordinator Admin", "Border Coordinator", 8082, body_content)
