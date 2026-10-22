"""DB password helper for the one-off maintenance scripts (repo root).

The local development password is intentionally NOT stored in these files
anymore. Export PGPASSWORD (standard libpq variable) or BOOKSTORE_DB_PASSWORD
before running any script that connects to PostgreSQL, e.g.:

    Windows cmd:  set PGPASSWORD=... 
    PowerShell:   $env:PGPASSWORD = "..."
    bash:         export PGPASSWORD=...
"""
import os


def db_password():
    password = os.environ.get("PGPASSWORD") or os.environ.get("BOOKSTORE_DB_PASSWORD")
    if not password:
        raise SystemExit(
            "PostgreSQL password not set. Export PGPASSWORD or "
            "BOOKSTORE_DB_PASSWORD first; credentials are not committed."
        )
    return password


# Used by the screenshot/demo scripts when a dev admin password other than
# the seed default is bootstrapped via DbSeeder env vars.
def admin_ui_password():
    return os.environ.get("BOOKSTORE_ADMIN_PASSWORD", "1234")
