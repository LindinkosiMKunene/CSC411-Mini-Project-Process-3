import subprocess
import sys
import time

services = [
    ("Auth Service", "auth.main:app", 8001),
    ("Coordinator Service", "coordinator.main:app", 8002),
    ("Immigration Service", "immigration.main:app", 8003),
    ("Customs Service", "customs.main:app", 8004),
    ("Port Health Service", "health.main:app", 8005),
    ("Environment Service", "environment.main:app", 8006),
    ("Foreign Adapter", "foreign_adapter.main:app", 8007),
    ("API Gateway", "gateway.main:app", 8000),
    
    # Dedicated Agency Web Clients
    ("Clearing Agent Portal", "clients.agent_portal:app", 8080),
    ("Coordinator Hub Console", "clients.coordinator_client:app", 8082),
    ("Immigration Web Client", "clients.immigration_client:app", 8083),
    ("Customs Web Client", "clients.customs_client:app", 8084),
    ("Port Health Web Client", "clients.health_client:app", 8085),
    ("Environment Web Client", "clients.environment_client:app", 8086),
    ("Foreign Adapter Client", "clients.foreign_client:app", 8087),
]

processes = []

print("========================================================================")
print("Starting Eswatini Border Management System (Separated Agency Web Clients)")
print("========================================================================")

try:
    for name, app_path, port in services:
        print(f"Starting {name} on http://127.0.0.1:{port}...")
        cmd = [sys.executable, "-m", "uvicorn", app_path, "--host", "127.0.0.1", "--port", str(port)]
        proc = subprocess.Popen(cmd)
        processes.append(proc)
        time.sleep(0.4)

    print("\n========================================================================")
    print("DEDICATED AGENCY WEB CLIENT PORTALS READY:")
    print("------------------------------------------------------------------------")
    print(" -> Clearing Agent Portal:              http://127.0.0.1:8080")
    print(" -> Coordinator Hub Console:            http://127.0.0.1:8082")
    print(" -> Immigration Client (Home Affairs):  http://127.0.0.1:8083")
    print(" -> Customs Client (ERS):               http://127.0.0.1:8084")
    print(" -> Port Health Client (Health):       http://127.0.0.1:8085")
    print(" -> Environment Client (Environment):  http://127.0.0.1:8086")
    print(" -> Foreign Adapter Client (SARS/Moz): http://127.0.0.1:8087")
    print("========================================================================")
    print("Press Ctrl+C to terminate all services cleanly.\n")
        
    for proc in processes:
        proc.wait()

except KeyboardInterrupt:
    print("\nStopping all microservices and web clients...")
    for proc in processes:
        proc.terminate()
    print("All processes stopped successfully.")
