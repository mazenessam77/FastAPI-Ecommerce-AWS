"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/lib/types";
import { api } from "@/lib/api";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;

  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username, password) => {
        const tokens = await api.login(username, password);
        api.setToken(tokens.access_token);
        set({ token: tokens.access_token, isAuthenticated: true });
        // Fetch user profile after login
        try {
          const me = await api.getMe();
          set({ user: me.data });
        } catch (_) {
          // Non-blocking — auth still succeeds
        }
      },

      logout: () => {
        api.setToken(null);
        set({ user: null, token: null, isAuthenticated: false });
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: "ecommerce-auth",
      // Restore token to api client when store rehydrates from localStorage
      onRehydrateStorage: () => (state) => {
        if (state?.token) api.setToken(state.token);
      },
    }
  )
);
