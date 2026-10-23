# DEÜ Kitap Satış — Bookstore Management System

E-commerce + back-office platform built for the Dokuz Eylül University
Faculty of Engineering bookstore: students browse/sell engineering titles,
order online with shipping or in-person pickup (order code verification at
the counter, cash sale support), and admins run inventory, users, contact
messages and reports from an admin panel. Emails (order confirmations,
verification codes) go through SMTP; a PowerShell script takes scheduled
PostgreSQL backups and mails the result.

Co-developed project (majority of commits by a teammate); documentation in
this repo is primarily Turkish — this README is the English index.

## Screenshots (from this repository, real captures)

| Storefront | Admin — inventory | Admin — dashboard |
|---|---|---|
| ![Storefront](manual_assets/02_home.png) | ![Inventory](manual_assets/books_mockup.png) | ![Dashboard](manual_assets/dashboard_mockup.png) |
| Admin — orders | Admin — reports | Customer checkout |
|![Orders](manual_assets/orders_mockup.png) |![Reports](manual_assets/reports_mockup.png) |![Checkout](manual_assets/04_cart_step2.png) |

More flows (checkout steps, distance-sale form, contact, reports) in
`manual_assets/`, referenced by the admin manual below.

## Stack (verified)

- **API** — ASP.NET Core 8 (`net8.0`), EF Core + Npgsql (PostgreSQL),
  JWT bearer auth, BCrypt password hashing, Swashbuckle (dev-only),
  background SMTP sending (`Services/EmailService.cs`).
- **Frontend** — React 19 + Vite 7 + react-router-dom 7 + axios; dev server
  proxies `/api` to the API on `http://localhost:5229` (`BookStore.Web/vite.config.js`).
- **DB** — PostgreSQL; 20+ EF migrations in `BookStore.Api/Migrations`,
  schema applied automatically at startup (`Program.cs` calls
  `Database.Migrate()`, then seeds admin user + book catalog).

## Layout

```
BookStore.Api/          # REST API (Controllers, EF models, migrations, services)
  appsettings.json      # connection string, JWT, EmailSettings placeholders
BookStore.Web/          # Vite + React storefront and admin panel
manual_assets/          # screenshots used by the admin manual
admin_manual.md|.html   # Turkish admin usage guide (with real screenshots)
DEU_*.{docx,pdf}        # legal texts: distance-sale contract, KVKK, forms
backup_db.ps1           # pg_dump + zip + retention + email report (config at top)
*.py / generate_*.py    # one-off data migration & doc generation utilities (scratch, root)
```

## Running locally

Prereqs: .NET 8 SDK, Node 20+, PostgreSQL 15+, (optional) Gmail app password
for SMTP.

```bash
# 1. Database: create role/db; appsettings ships an EMPTY password by design.
#    Point the app at your local db via env var (never commit it):
#    $env:ConnectionStrings__DefaultConnection = "Host=...;Database=...;Username=...;Password=..."

# 2. API
cd BookStore.Api
dotnet run          # https://localhost:5001 / http://localhost:5229; Swagger at /swagger (Development only)

# 3. Frontend
cd BookStore.Web
npm install
npm run dev         # http://localhost:5173 (proxies /api to :5229)
```

On first start the API migrates the schema, seeds the book catalog from
`books_data_v2.json`, and bootstraps the admin user:

- **Development:** `admin / 1234` (printed warning — never deploy this pair).
- **Production:** seeded only when `BOOKSTORE_ADMIN_PASSWORD` (optionally
  `BOOKSTORE_ADMIN_EMAIL`) is set; otherwise seeding is skipped. Use a one-time
  bootstrap value, log in, change the password, then unset the variable.

Required/overridable configuration (env vars follow the standard
`Section__Key` convention, or use `dotnet user-secrets` for Development):

| Variable | Purpose | Behavior if unset |
|---|---|---|
| `Jwt__Key` | HMAC signing secret (≥32 chars) | app refuses to start outside Development; placeholder in `appsettings.json` is rejected the same way |
| `ConnectionStrings__DefaultConnection` | PostgreSQL connection | falls back to the local dev string in `appsettings.json` |
| `EmailSettings__Host/Port/Username/Password` | SMTP | EmailService logs `[MOCK EMAIL]` instead of sending (placeholder detection) |
| `Cors__AllowedOrigins__0…` | extra frontend origins | dev default `http://localhost:5173` |
| `BOOKSTORE_ADMIN_PASSWORD` | first-run admin bootstrap | production: no admin seeded |

## API surface (controllers, all under `/api`)

| Controller | Purpose |
|---|---|
| `auth` | register, login (JWT), email verify |
| `Book` | catalog CRUD, admin bulk price/status updates |
| `Cart` | add/update/remove/list cart items |
| `Orders` | checkout, admin checkout (counter sale), pickup verification, cancel, return, my-orders |
| `Users` | profile, change password (code by e-mail), admin user management, block |
| `Addresses` | CRUD + default address |
| `Contact` | support messages, admin read/reply |
| `Dashboard` | admin stats |

## Security notes — read before deploying anywhere

- **A real SMTP account password (`kitapsatis@deu.edu.tr` @ mail.deu.edu.tr:27002)
  is visible in git history** (commit `0e9a327`; the working tree only ever
  holds a placeholder). The mailbox password must be rotated by its owner —
  treat it as compromised. Erasing history (force-push) is a separate,
  destructive decision and was not taken.
- The former committed JWT key
  remains in history; tokens signed with it must not be trusted and any real
  deployment needs a fresh `Jwt__Key` (startup now hard-fails in Production
  without one).
- `appsettings.json` no longer contains a contributor's personal Gmail
  address; SMTP identity comes from `EmailSettings__Username`.
- CORS origins are configurable (`Cors:AllowedOrigins`) with a dev-only
  default; Swagger is Development-only. `admin/1234` exists only in the
  Development seeding path (see configuration table above).
- `EmailService` logs full message bodies only in MOCK mode (placeholder
  credentials); real SMTP failures log the exception, never the password.

## Testing, CI, quality

No automated tests exist for either side, and there is no CI. `dotnet build`
and `vite build` runs are recorded in the audit reports
(`VALIDATION_RESULTS.md` in the handoff). Manual QA evidence lives in
`manual_assets/` and `admin_manual.md`.

## Maintenance issues worth knowing

- Root-level utility scripts (`check_fk.py`, `rebuild_db.py`,
  `sync_all_data.py`, `update_*.py`, `take_*_screenshots.py`, …) are one-off
  migration/demo tools, not runtime code. DB-touching scripts now require
  `PGPASSWORD` (or `BOOKSTORE_DB_PASSWORD`) via `pg_env.py`; they no longer
  embed the dev password.
- `admin_manual.md` mentions 2FA; the implementation is an e-mail code for
  password change, not an OTP login factor.
- The backup script keeps its config as empty placeholders — fill the top of
  `backup_db.ps1` or pass values; it uses `pg_dump`, zips, prunes >14 days.
- No repository LICENSE file. Choose one (or mark internal-only) before
  publishing reuse terms.

## Docs

- Admin guide: [`admin_manual.md`](admin_manual.md) (TR, with screenshots in
  `manual_assets/`) — also available as [`admin_manual.html`](admin_manual.html)
- Legal/contract documents: `DEU_*.docx` / `DEÜ*.pdf` at repo root
- E-mail integration: [`email_implementation_guide.md`](email_implementation_guide.md)
