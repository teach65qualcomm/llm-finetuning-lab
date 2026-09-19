"""Initialize the SQLite database."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from case_summary_assistant.repository import init_db
init_db()
print("Database initialized at data/cases.db")
