export interface Product {
  id: number;
  title: string;
  description: string;
  price: number;
  discount_percentage: number;
  rating: number;
  stock: number;
  brand: string;
  thumbnail: string;
  images: string[];
  is_published: boolean;
  created_at: string;
  category_id: number;
  category?: Category;
}

export interface Category {
  id: number;
  name: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: "admin" | "user";
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiResponse<T> {
  message: string;
  data: T;
}

export interface PaginatedResponse<T> {
  message: string;
  data: T[];
}

export interface ProductFilters {
  category_id?: number;
  min_price?: number;
  max_price?: number;
  search?: string;
  sort_by?: "price_asc" | "price_desc" | "newest" | "rating";
  page?: number;
  limit?: number;
}
