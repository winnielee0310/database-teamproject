import importlib.util
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
SETUP_PATH = BACKEND_DIR / "setup_db.py"

spec = importlib.util.spec_from_file_location("idol_trade_setup_db", SETUP_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load setup script from {SETUP_PATH}")

setup_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup_module)
setup_database = setup_module.setup_database


if __name__ == "__main__":
    setup_database()
