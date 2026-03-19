"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/lib/types";
import { api } from "@/lib/api";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  _hasHydrated: boolean;

  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  setHasHydrated: (value: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      _hasHydrated: false,

      login: async (username, password) => {
        const tokens = await api.login(username, password);
        api.setToken(tokens.access_token);
        set({ token: tokens.access_token, isAuthenticated: true });
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
      setHasHydrated: (value) => set({ _hasHydrated: value }),
    }),
    {
      name: "ecommerce-auth",
      // _hasHydrated is runtime-only, never persist it to localStorage
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        // Called after localStorage is read — safe to use token now
        if (state?.token) api.setToken(state.token);
        state?.setHasHydrated(true);
      },
    }
  )
);
