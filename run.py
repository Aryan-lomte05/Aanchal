"""
Aanchal Root Execution Entry Point
Run: python run.py
"""

import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.run_all import main

if __name__ == "__main__":
    main()
