# Business Page (Admin)

The Business page is an admin-only area for configuring fulfillment mode and provider integrations. Customers never see this UI.

---

## Access

- **URL:** `/business/`
- **Required:** Staff or superuser account
- **Non-admin users:** Redirected to login or 403

Log in as a staff user, then use the **Business** link in the main navigation bar.

---

## Sections

### Effective Configuration Summary

Displays the current settings:

- **Mode:** MANUAL (Self-Fulfillment) or POD (Print-on-Demand)
- **Manual provider:** shippo, easypost, or none
- **POD provider:** printful, printify, gelato, or none
- **Secrets:** env-only (recommended) or db-local (local demos only)

### Fulfillment Mode Toggle

- **Self-Fulfillment (artist ships):** You handle packing and shipping. Optionally integrate Shippo or EasyPost for labels.
- **Print-on-Demand (outsourced):** A third-party produces and ships. Optionally integrate Printful, Printify, or Gelato.

Use the **Use env vars for API keys** checkbox. **Production should always use env-only secrets.**

### Provider Integration Cards

Depending on the mode, different provider cards are shown:

**Manual (Self-Fulfillment):**

- **Shippo** – Env var: `SHIPPO_API_TOKEN`
- **EasyPost** – Env var: `EASYPOST_API_KEY`
- **None** – Manual workflow; no API integration

**POD (Print-on-Demand):**

- **Printful** – Env var: `PRINTFUL_API_KEY`
- **Printify** – Env var: `PRINTIFY_API_KEY`
- **Gelato** – Env var: `GELATO_API_KEY`
- **None** – Manual production workflow

Each card shows:

- **Configured / Not configured** status
- When **Use env secrets** is off: masked input for API key, Save button, Test connection button
- Warning when using DB-stored keys (local dev only)

### Webhooks

Lists webhook URLs to configure in provider dashboards:

- **Stripe:** `https://your-domain/webhooks/stripe/`
- **Fulfillment:** `https://your-domain/webhooks/fulfillment/<provider>/`

### Order Lifecycle Reference

Status flow: DRAFT → PENDING_PAYMENT → PAID → FULFILLMENT_PENDING → IN_PRODUCTION → SHIPPED → DELIVERED

Provider selection is determined by admin configuration. Customers cannot choose providers.

---

## Security Notes

- **Production:** Use environment variables for all API keys. Never store raw keys in the database.
- **Local demos:** DB-stored secrets are available when "Use env vars" is unchecked. Marked as not recommended for production.
- Provider secrets are masked in the UI.
