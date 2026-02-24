# Stripe Setup & Integration

[← Back to Wiki](README.md)

This guide covers connecting Stripe for checkout on both the **Django backend** and **Next.js frontend**.

---

## 1. Create a Stripe Account

1. Sign up at [stripe.com](https://stripe.com)
2. Use **test mode** (top-right toggle) during development
3. Get your keys from [Dashboard → Developers → API keys](https://dashboard.stripe.com/apikeys)

---

## 2. Django Backend (store root)

### Environment variables

Add to `.env`:

```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Admin panel

1. Log in as staff
2. Go to **Admin Panel** → **Stripe Integration**
3. Enter **Publishable key** and **Secret key**
4. Save

Keys stored in the database override env vars.

### Webhook

1. [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks)
2. Add endpoint: `https://your-domain.com/webhooks/stripe/`
3. Select event: `checkout.session.completed`
4. Copy the **Signing secret** (starts with `whsec_`)
5. Add to `.env` as `STRIPE_WEBHOOK_SECRET`

### Flow

- User adds to cart → checkout → `checkout_create` creates Stripe Checkout session
- User pays on Stripe-hosted page → redirect to success URL
- Stripe sends `checkout.session.completed` to webhook → order created in Django
- Without Stripe keys, checkout runs in **demo mode** (order created without payment)

---

## 3. Next.js Frontend (`/frontend`)

### Environment variables

Add to `frontend/.env.local`:

```
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

`STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` are server-only; never expose them to the client.

### Webhook (local development)

Use [Stripe CLI](https://stripe.com/docs/stripe-cli):

```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

Copy the webhook signing secret from the CLI output and add to `.env.local` as `STRIPE_WEBHOOK_SECRET`.

### Webhook (production)

1. [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks)
2. Add endpoint: `https://your-vercel-domain.com/api/webhooks/stripe`
3. Select event: `checkout.session.completed`
4. Copy the signing secret → add to Vercel env vars as `STRIPE_WEBHOOK_SECRET`

### Flow

1. User adds products to cart (localStorage)
2. **Checkout** → `POST /api/checkout` creates Stripe Checkout session
3. User is redirected to Stripe-hosted payment page
4. After payment, Stripe sends `checkout.session.completed` to webhook
5. Webhook creates `orders` and `order_items` in Supabase

---

## 4. Testing

### Test cards (Stripe test mode)

| Card number           | Scenario                    |
|-----------------------|-----------------------------|
| `4242 4242 4242 4242` | Successful payment          |
| `4000 0000 0000 0002` | Card declined               |

Use any future expiry, any CVC, any postal code.

---

## 5. Going Live

1. Switch Stripe to **live mode**
2. Replace test keys with live keys
3. Create a **live** webhook endpoint with the same events
4. Update env vars in production
5. Ensure your domain is verified in Stripe (if required)
