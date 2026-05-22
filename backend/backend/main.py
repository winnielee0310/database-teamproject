import importlib.util
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
BACKEND_MAIN = BACKEND_DIR / "main.py"

sys.path.insert(0, str(BACKEND_DIR))

spec = importlib.util.spec_from_file_location("idol_trade_backend_main", BACKEND_MAIN)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load backend app from {BACKEND_MAIN}")

backend_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_main)

app = backend_main.app
