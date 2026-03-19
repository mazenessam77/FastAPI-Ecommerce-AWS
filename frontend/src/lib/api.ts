import type {
  Product,
  Category,
  AuthTokens,
  User,
  Order,
  ApiResponse,
  PaginatedResponse,
  ProductFilters,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (this.token) {
      (headers as Record<string, string>)["Authorization"] =
        `Bearer ${this.token}`;
    }

    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(error.detail || `API error: ${res.status}`);
    }

    return res.json();
  }

  // ── Auth ──
  async login(
    username: string,
    password: string
  ): Promise<AuthTokens> {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    return this.request("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData.toString(),
    });
  }

  async signup(data: {
    username: string;
    email: string;
    password: string;
    full_name: string;
  }): Promise<ApiResponse<User>> {
    return this.request("/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // ── Products ──
  async getProducts(
    filters?: ProductFilters
  ): Promise<PaginatedResponse<Product>> {
    const params = new URLSearchParams();
    if (filters?.page) params.set("page", String(filters.page));
    if (filters?.limit) params.set("limit", String(filters.limit));
    if (filters?.search) params.set("search", filters.search);
    const qs = params.toString();
    return this.request(`/products/${qs ? `?${qs}` : ""}`);
  }

  async getProduct(id: number): Promise<ApiResponse<Product>> {
    return this.request(`/products/${id}`);
  }

  // ── Categories ──
  async getCategories(): Promise<PaginatedResponse<Category>> {
    return this.request("/categories/");
  }

  // ── Account ──
  async getMe(): Promise<ApiResponse<User>> {
    return this.request("/me/");
  }

  // ── Cart ──
  async addToCart(
    productId: number,
    quantity: number
  ): Promise<ApiResponse<unknown>> {
    return this.request("/carts/", {
      method: "POST",
      body: JSON.stringify({
        items: [{ product_id: productId, quantity }],
      }),
    });
  }

  // ── Orders ──
  async checkout(
    items: { product_id: number; quantity: number }[]
  ): Promise<ApiResponse<Order>> {
    return this.request("/orders/checkout", {
      method: "POST",
      body: JSON.stringify({ items }),
    });
  }

  async getOrders(page = 1, limit = 20): Promise<PaginatedResponse<Order>> {
    return this.request(`/orders/?page=${page}&limit=${limit}`);
  }

  async getOrder(id: number): Promise<ApiResponse<Order>> {
    return this.request(`/orders/${id}`);
  }
}

export const api = new ApiClient(API_URL);
export { API_URL };
