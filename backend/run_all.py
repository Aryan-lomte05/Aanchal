"""
Unified Service Launcher for Aanchal
Spawns District Node Service (Port 8000) and National Aggregator Service (Port 9000) concurrently.
"""

import sys
import os
import time
import threading
import uvicorn

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)


def run_node_service():
    os.environ["NODE_ID"] = os.getenv("NODE_ID", "district_pune")
    os.environ["AGGREGATOR_URL"] = os.getenv("AGGREGATOR_URL", "http://localhost:9000")
    print("\n[Aanchal] 🚀 Starting District Node Service on http://localhost:8000 ...")
    uvicorn.run("node_service.main:app", host="0.0.0.0", port=8000, log_level="info")


def run_aggregator_service():
    print("\n[Aanchal] 🏛️ Starting National Aggregator Service on http://localhost:9000 ...")
    uvicorn.run("aggregator_service.main:app", host="0.0.0.0", port=9000, log_level="info")


def main():
    print("=" * 70)
    print("  🌸 AANCHAL: CONTINUOUS CARE & PRIVATE DISTRESS MONITORING 🌸")
    print("  SIH26094 · Ministry of Social Justice and Empowerment")
    print("  KJSSE CSI Gemini Hackday 2.0")
    print("=" * 70)
    print("  📍 District Node Service : http://localhost:8000")
    print("  📍 National Aggregator   : http://localhost:9000")
    print("  📍 PWA Frontend Web App  : http://localhost:8000/pwa/index.html")
    print("=" * 70)

    t_agg = threading.Thread(target=run_aggregator_service, daemon=True)
    t_agg.start()

    time.sleep(1.0)
    run_node_service()


if __name__ == "__main__":
    main()
