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
# 1. Database: create role/db, defaults expect postgres/1234 @ localhost:5432/kitapsatisdb
#    (override without editing appsettings via env var:)
#    $env:ConnectionStrings__DefaultConnection = "Host=...;Database=...;Username=...;Password=..."

# 2. API
cd BookStore.Api
dotnet run          # https://localhost:5001 / http://localhost:5229; Swagger at /swagger (Development only)

# 3. Frontend
cd BookStore.Web
npm install
npm run dev         # http://localhost:5173 (proxies /api to :5229)
```

A fresh start creates tables and seeds `admin / 1234` plus the book catalog
from `books_data_v2.json`.

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
  was committed in history** (commit `0e9a327`, later replaced with a
  placeholder). Rotate that mailbox password; erasing history is a separate,
  destructive step this repo has intentionally not taken.
- `appsettings.json` ships a placeholder JWT signing key
  (`SUPER_SECRET_KEY_32_CHAR_MINIMUM_123456`). Anyone who can see the repo can
  forge tokens with it — always override
  `Jwt:Key` via environment/user-secrets in any non-local deployment.
- Seeded admin uses `admin / 1234`; force a change immediately after first
  login.
- CORS allows only the Vite dev origin and Swagger is Development-only —
  both must be revisited for production hosting.
- Gmail address of a contributor appears in `appsettings.json` default
  config; remove if it should not be public.

## Testing, CI, quality

No automated tests exist for either side, and there is no CI. The API build
was not re-run in this audit environment (no .NET 8 SDK installed);
frontend `vite build` result is recorded in the audit reports. Manual QA
evidence lives in `manual_assets/` and `admin_manual.md`.

## Maintenance issues worth knowing

- Root-level utility scripts (`extract_books_v2.py`, `generate_docx.py`,
  `take_*_screenshots.py`, …) are one-off migrations/tools referencing the
  dev DB password `1234`; they are not part of the runtime.
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
