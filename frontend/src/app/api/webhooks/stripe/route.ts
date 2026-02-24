import { NextRequest, NextResponse } from "next/server";
import Stripe from "stripe";
import { createClient } from "@supabase/supabase-js";

const stripe =
  process.env.STRIPE_SECRET_KEY ?
    new Stripe(process.env.STRIPE_SECRET_KEY, { typescript: true })
  : null;
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

export async function POST(req: NextRequest) {
  if (!stripe || !webhookSecret) {
    return NextResponse.json(
      { error: "Webhook not configured" },
      { status: 500 }
    );
  }

  const sig = req.headers.get("stripe-signature");
  if (!sig) {
    return NextResponse.json({ error: "No signature" }, { status: 400 });
  }

  let event: Stripe.Event;
  try {
    const body = await req.text();
    event = stripe.webhooks.constructEvent(body, sig, webhookSecret);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json(
      { error: `Webhook signature verification failed: ${message}` },
      { status: 400 }
    );
  }

  if (event.type !== "checkout.session.completed") {
    return NextResponse.json({ received: true });
  }

  const session = event.data.object as Stripe.Checkout.Session;
  const sessionId = session.id;
  const customerEmail = session.customer_email || session.customer_details?.email;

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  if (!supabaseUrl || !supabaseServiceKey) {
    console.error("Supabase not configured for webhook");
    return NextResponse.json({ received: true });
  }

  const supabase = createClient(supabaseUrl, supabaseServiceKey);

  // Check if order already exists (idempotency)
  const { data: existing } = await supabase
    .from("orders")
    .select("id")
    .eq("stripe_session_id", sessionId)
    .single();

  if (existing) {
    return NextResponse.json({ received: true });
  }

  const lineItems = await stripe.checkout.sessions.listLineItems(sessionId);
  let totalAmount = 0;
  const orderItems: {
    order_id: string;
    product_id: string | null;
    title_snapshot: string;
    unit_price: number;
    quantity: number;
  }[] = [];

  for (const item of lineItems.data) {
    const qty = item.quantity ?? 1;
    const unitPrice = (item.price?.unit_amount ?? 0) / 100;
    totalAmount += unitPrice * qty;
    const productId =
      (item.price?.product as Stripe.Product)?.metadata?.product_id ?? null;
    orderItems.push({
      order_id: "", // set after order created
      product_id: productId,
      title_snapshot: item.description ?? "Product",
      unit_price: unitPrice,
      quantity: qty,
    });
  }

  const { data: order, error: orderErr } = await supabase
    .from("orders")
    .insert({
      email: customerEmail ?? "unknown",
      status: "paid",
      total_amount: totalAmount,
      currency: "USD",
      stripe_session_id: sessionId,
    })
    .select("id")
    .single();

  if (orderErr || !order) {
    console.error("Failed to create order:", orderErr);
    return NextResponse.json({ error: "Order creation failed" }, { status: 500 });
  }

  for (const oi of orderItems) {
    oi.order_id = order.id;
  }
  const { error: itemsErr } = await supabase.from("order_items").insert(orderItems);
  if (itemsErr) {
    console.error("Failed to create order items:", itemsErr);
  }

  return NextResponse.json({ received: true });
}
