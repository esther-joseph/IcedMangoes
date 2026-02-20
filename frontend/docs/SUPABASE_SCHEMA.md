# Supabase Schema & Storage

## Database Schema

Run the SQL in `supabase/migrations/001_initial_schema.sql` in the Supabase SQL Editor (Dashboard → SQL Editor) or via Supabase CLI.

### Tables

- **products** – Artist listings with title, description, price, currency, tags, image_url, active flag
- **orders** – Orders (Stripe integration in Phase 2)
- **order_items** – Line items with product snapshot

### RLS Policies

- `products`: public read for `active = true`
- `orders` / `order_items`: no public policies (Phase 2+)

---

## Storage: `media` Bucket

### Create the bucket

1. Supabase Dashboard → Storage
2. New bucket: name **`media`**
3. **Public bucket**: yes (for product images served to storefront)
4. Create

### Folder structure

```
media/
  products/
    {product_id}/
      image.jpg
```

### Product image URL

When uploading a product image, store the **public URL**:

```
https://{project-ref}.supabase.co/storage/v1/object/public/media/products/{product_id}/{filename}
```

Save this URL in `products.image_url`.

### Upload flow (Phase 3)

1. Client uploads file to `media/products/{product_id}/`
2. Get public URL from Storage
3. Update `products.image_url` with that URL

### Alternative: Signed URLs

For private media, use signed URLs:

- Store path in `products.image_url` (e.g. `products/abc-123/main.jpg`)
- Server generates signed URL when serving product pages
- Use `supabase.storage.from('media').createSignedUrl(path, expiresIn)`
