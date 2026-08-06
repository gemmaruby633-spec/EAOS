"""Evidence-Driven Anchor Patcher for change_propagation_adapter.py."""

from __future__ import annotations

from pathlib import Path


def patch_file() -> bool:
    target = Path("packages/business_architecture/adapters") / "change_propagation_adapter.py"
    if not target.exists():
        print(f"❌ File not found: {target}")
        return False

    content = target.read_text(encoding="utf-8")

    start_anchor = "changed_count = 1"
    end_anchor = "return ImpactAnalysisMatrix("

    start_idx = content.find(start_anchor)
    end_idx = content.find(end_anchor)

    if start_idx == -1 or end_idx == -1:
        print("❌ Start or End Anchor not found in file.")
        start_find = content.find("analyze_impact")
        excerpt = content[start_find : start_find + 300]
        print(f"Observed Content Excerpt:\n{excerpt}")
        return False

    observed_snippet = content[start_idx:end_idx]
    print("=== OBSERVED SNIPPET BEFORE PATCH ===")
    print(observed_snippet)

    replacement = (
        "changed_count = 1\n"
        "        if (\n"
        "            old_ir\n"
        "            and old_ir.rules\n"
        "            and new_ir.rules\n"
        "            and (\n"
        "                old_ir.rules[0].discount_percentage\n"
        "                != new_ir.rules[0].discount_percentage\n"
        "            )\n"
        "        ):\n"
        "            changed_count += 1\n\n        "
    )

    new_content = content[:start_idx] + replacement + content[end_idx:]
    target.write_text(new_content, encoding="utf-8")

    print("=== OBSERVED SNIPPET AFTER PATCH ===")
    print(replacement)
    print("✔ Patch applied successfully via Anchor Replacement!")
    return True


if __name__ == "__main__":
    patch_file()
