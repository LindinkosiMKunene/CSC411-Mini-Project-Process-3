from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = httpx.AsyncClient(timeout=10.0)

ROUTES = {
    "auth": "http://127.0.0.1:8001",
    "cases": "http://127.0.0.1:8002",
    "travellers": "http://127.0.0.1:8003",
    "declarations": "http://127.0.0.1:8004"
}

@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_proxy(service: str, path: str, request: Request):
    if service not in ROUTES:
        return Response(content='{"detail":"Service not found"}', status_code=404)
    
    target_url = f"{ROUTES[service]}/{path}"
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    
    response = await client.request(request.method, target_url, content=body, headers=headers, params=request.query_params)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.get("/health")
def health():
    return {"status": "healthy", "service": "gateway"}
