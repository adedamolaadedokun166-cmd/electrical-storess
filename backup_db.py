import shutil
from datetime import datetime
from pathlib import Path

source = Path(__file__).resolve().parent / "database.db"
destination_dir = Path(__file__).resolve().parent / "backups"
destination_dir.mkdir(exist_ok=True)

if source.exists():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = destination_dir / f"database_{timestamp}.db"
    shutil.copy2(source, destination)
    print(f"Database backup created at {destination}")
else:
    print("No database found to back up")
