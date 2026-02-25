export interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  tags: string[] | null;
  image_url: string | null;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: string;
  email: string;
  status: string;
  total_amount: number;
  currency: string;
  stripe_session_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string | null;
  title_snapshot: string;
  unit_price: number;
  quantity: number;
  created_at: string;
}
