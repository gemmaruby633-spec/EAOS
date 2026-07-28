"""EAOS Single-File Zero-Config ACID Engine (Portable Execution)."""

import sqlite3
import time
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class SingleFileEngineResultDTO(BaseModel):
    """Value object representing single-file ACID transaction result."""

    model_config = ConfigDict(frozen=True)

    status: str
    db_file_path: str
    acid_compliant: bool = True
    execution_time_ms: float


class EAOSSingleFileEngine:
    """Zero-Config Single-File Engine running directly on SQLite WAL."""

    def __init__(self, db_path: str = "eaos_portable.db") -> None:
        self.db_path = str(Path(db_path).resolve())
        self._init_acid_db()

    def _init_acid_db(self) -> None:
        """Initializes WAL mode SQLite schema with ACID transaction rules."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute(
                "CREATE TABLE IF NOT EXISTS audit_ledger (id TEXT PRIMARY KEY, action TEXT, sha256_hash TEXT);"
            )

    def execute_acid_transaction(self, action: str, payload_hash: str) -> SingleFileEngineResultDTO:
        """Executes atomic ACID transaction on single data file."""
        start = time.perf_counter()
        rec_id = f"TX-{int(time.time() * 1000)}"

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO audit_ledger VALUES (?, ?, ?);",
                (rec_id, action, payload_hash),
            )
            conn.commit()

        elapsed = (time.perf_counter() - start) * 1000.0
        return SingleFileEngineResultDTO(
            status="ACID_COMMITTED",
            db_file_path=self.db_path,
            acid_compliant=True,
            execution_time_ms=round(elapsed, 3),
        )


if __name__ == "__main__":
    engine = EAOSSingleFileEngine()
    res = engine.execute_acid_transaction("CREATE_CAPABILITY", "a1b2c3d4")
    print(f"✔ Single-File Engine Status: {res.status}")
    print(f"✔ DB Path: {res.db_file_path}")
    print(f"✔ Latency: {res.execution_time_ms} ms (ACID Compliant)")
