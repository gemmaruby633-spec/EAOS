"""Script to safely inject root endpoint into apps/api/app/main.py."""

from pathlib import Path


def inject_root_route() -> None:
    """Safely injects @app.get("/") into main.py before @app.get("/health"."""
    main_path = Path("apps/api/app/main.py")
    if not main_path.exists():
        return

    content = main_path.read_text(encoding="utf-8")
    if '@app.get("/")' in content:
        print("  ✔ Root endpoint already exists in main.py")
        return

    root_code = """

@app.get("/")
async def root_system_status() -> dict[str, Any]:
    \"\"\"Root status probe providing system overview and control room links.\"\"\"
    return {
        "system": "Enterprise Architecture Operating System (EAOS)",
        "status": "ACTIVE",
        "version": "0.1.0",
        "governance": "ARCHITECTURE_CONSTITUTION.md v3.0",
        "control_room_dashboard": "/dashboard",
        "api_documentation": "/docs",
        "health_check": "/health",
    }
"""

    target = '@app.get("/health"'
    if target in content:
        new_content = content.replace(target, root_code.strip() + "\n\n\n" + target, 1)
        main_path.write_text(new_content, encoding="utf-8")
        print("  ✔ Injected root endpoint into main.py successfully")


if __name__ == "__main__":
    inject_root_route()
