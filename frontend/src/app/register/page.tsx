"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Eye, EyeOff, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { useAuthStore } from "@/stores/auth-store";

export default function RegisterPage() {
  const [form, setForm] = useState({ full_name: "", username: "", email: "", password: "" });
  const [showPw, setShowPw] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuthStore();
  const router = useRouter();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.signup(form);
      await login(form.username, form.password);
      router.push("/");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  const fields = [
    { id: "full_name", label: "Full Name", type: "text", placeholder: "Jane Doe", autoComplete: "name" },
    { id: "username", label: "Username", type: "text", placeholder: "janedoe", autoComplete: "username" },
    { id: "email", label: "Email", type: "email", placeholder: "jane@example.com", autoComplete: "email" },
  ] as const;

  return (
    <div className="flex min-h-[calc(100vh-8rem)] items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm animate-scale-in">

        {/* Logo mark */}
        <div className="mb-8 flex flex-col items-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary shadow-lg mb-4">
            <span className="text-xl font-extrabold text-primary-foreground">E</span>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight">Create your account</h1>
          <p className="mt-1 text-sm text-muted-foreground">Join thousands of happy customers</p>
        </div>

        {/* Card */}
        <div className="rounded-2xl border bg-card p-8 shadow-card">
          <form onSubmit={handleSubmit} className="space-y-4">

            {fields.map(({ id, label, type, placeholder, autoComplete }) => (
              <div key={id} className="space-y-1.5">
                <label htmlFor={id} className="text-sm font-semibold">{label}</label>
                <input
                  id={id}
                  name={id}
                  type={type}
                  placeholder={placeholder}
                  value={form[id]}
                  onChange={handleChange}
                  required
                  autoComplete={autoComplete}
                  className="h-10 w-full rounded-lg border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring transition placeholder:text-muted-foreground"
                />
              </div>
            ))}

            {/* Password */}
            <div className="space-y-1.5">
              <label htmlFor="password" className="text-sm font-semibold">Password</label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPw ? "text" : "password"}
                  placeholder="Min. 8 characters"
                  value={form.password}
                  onChange={handleChange}
                  required
                  autoComplete="new-password"
                  className="h-10 w-full rounded-lg border bg-background px-3 pr-10 text-sm outline-none focus:ring-2 focus:ring-ring transition placeholder:text-muted-foreground"
                />
                <button
                  type="button"
                  onClick={() => setShowPw(!showPw)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {showPw ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="rounded-lg bg-destructive/10 border border-destructive/20 px-3 py-2 text-sm text-destructive">
                {error}
              </div>
            )}

            <Button type="submit" className="w-full gap-2 rounded-lg" disabled={loading}>
              {loading ? (
                <span className="h-4 w-4 rounded-full border-2 border-primary-foreground/30 border-t-primary-foreground animate-spin" />
              ) : (
                <UserPlus className="h-4 w-4" />
              )}
              {loading ? "Creating account…" : "Create account"}
            </Button>
          </form>
        </div>

        <p className="mt-5 text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/login" className="font-semibold text-foreground underline underline-offset-4 hover:text-primary/70 transition-colors">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
