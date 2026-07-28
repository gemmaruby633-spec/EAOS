"""Script fixing syntax errors and SQLite handle leaks in test_eaos_master.py."""

from pathlib import Path


def repair_test_eaos_master() -> None:
    """Fixes test_pgvector_memory_adapter_sqlite_fallback with valid syntax."""
    p = Path("tests/test_eaos_master.py")
    if not p.exists():
        return

    code = p.read_text(encoding="utf-8")

    clean_test_function = '''def test_pgvector_memory_adapter_sqlite_fallback(tmp_path: Any) -> None:
    """Verifies architecture memory adapter with SQLite fallback."""
    import gc

    db_file = tmp_path / "test_memory.db"
    db_url = f"sqlite:///{db_file}"

    adapter = PgVectorArchitectureMemoryAdapter(db_url=db_url)
    try:
        record = ArchitectureMemoryRecordAggregate(
            memory_id="MEM-PG-01",
            tier=MemoryTier.SEMANTIC,
            memory_type=MemoryType.PATTERN_RULE,
            title="Hexagonal Coupling Protection",
            context_summary="Domain layer isolation pattern",
            lesson_learned="Never import infrastructure in domain",
        )

        adapter.save(record)

        fetched = adapter.find_by_id("MEM-PG-01")
        assert fetched is not None
        assert fetched.memory_id == "MEM-PG-01"
        assert fetched.title == "Hexagonal Coupling Protection"
    finally:
        if hasattr(adapter, "engine") and adapter.engine:
            adapter.engine.dispose()
        gc.collect()'''

    lines = code.splitlines()
    new_lines = []
    in_target_func = False

    for line in lines:
        if "def test_pgvector_memory_adapter_sqlite_fallback" in line:
            in_target_func = True
            new_lines.append(clean_test_function)
            continue

        if in_target_func:
            if line.startswith("def test_"):
                in_target_func = False
                new_lines.append(line)
            continue

        new_lines.append(line)

    p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print("  ✔ Successfully repaired tests/test_eaos_master.py syntax")


if __name__ == "__main__":
    repair_test_eaos_master()
