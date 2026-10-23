# BookStore.Web — storefront + admin panel (React + Vite)

Frontend of the DEÜ Kitap Satış platform. See the
[repository README](../README.md) for the full architecture, setup and
security notes. This directory only covers the client.

## Develop

```bash
npm install
npm run dev     # http://localhost:5173
```

The dev server proxies `/api/*` to `http://localhost:5229`
(`vite.config.js`), which is the `dotnet run` HTTP profile of
`BookStore.Api` — start the API first or every request 502s.

## Build

```bash
npm run build   # output: dist/ (deployed by IIS/nginx as static files)
npm run preview
```

## Structure

- `src/pages/` — storefront (home via `App.jsx`, book detail, cart/checkout,
  distance-sales form, contact, login/register, profile with orders,
  addresses, favorites) and `Admin/` (dashboard, book & order & user
  management, contact messages, settings, reports).
- `src/components/` — navbar, sidebar, footer, book cards, modals.
- `public/images/books/` — locally served catalog cover images (~45 MB of
  JPEGs committed on purpose so the catalog renders offline).
- `src/data/turkeyCities.js` — city list for address/shipping forms.
