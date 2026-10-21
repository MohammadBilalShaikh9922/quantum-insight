"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import Logo from "./Logo";
import { Icon } from "./Icons";
import { useAuth } from "../lib/auth";

const nav = [
  ["/dashboard", "Dashboard", "grid"],
  ["/analyzer", "Analyzer", "analyze"],
  ["/debugger", "AI Debugger", "bug"],
  ["/optimizer", "Optimizer", "zap"],
  ["/history", "History", "history"],
  ["/settings", "Settings", "settings"],
];

export default function AppShell({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { user, loading, logout } = useAuth();

  const [open, setOpen] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [themeReady, setThemeReady] = useState(false);

  useEffect(() => {
    const savedTheme = window.localStorage.getItem("qi_theme");
  
    if (savedTheme === "light" || savedTheme === "dark") {
      setTheme(savedTheme);
    }
  
    setThemeReady(true);
  }, []);
  
  useEffect(() => {
    if (!themeReady) return;
  
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
  
    window.localStorage.setItem("qi_theme", theme);
  }, [theme, themeReady]);
  
  useEffect(() => {
  async function checkAdmin() {
    try {
      const token = window.localStorage.getItem("qi_token");

      if (!token) {
        return;
      }

      const API_URL =
        process.env.NEXT_PUBLIC_API_URL ||
        "https://quantuminsight-backend.onrender.com";

      const response = await fetch(
        `${API_URL}/api/admin/users`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        setIsAdmin(true);
      }
    } catch {
      setIsAdmin(false);
    }
  }

  checkAdmin();
}, []);

  const authPage =
    pathname === "/login" ||
    pathname === "/register";

  if (authPage) return <>{children}</>;

  return (
    <div className="app-bg min-h-screen">
      {/* Sidebar */}
      <aside
        className={`sidebar ${
          open ? "sidebar-open" : ""
        } flex flex-col overflow-y-auto`}
      >
        {/* Brand */}
        <div className="flex shrink-0 items-center justify-between border-b border-white/5 px-5 py-5">
          <Link
            href="/dashboard"
            onClick={() => setOpen(false)}
            className="transition-opacity hover:opacity-90"
          >
            <Logo compact />
          </Link>

          <button
            type="button"
            aria-label="Close navigation"
            className="icon-btn lg:hidden"
            onClick={() => setOpen(false)}
          >
            <Icon name="close" />
          </button>
        </div>

        {/* Navigation */}
        <div className="shrink-0 px-4 py-5">
          <div className="mb-3 flex items-center justify-between px-2">
            <div className="side-label">
              Workspace
            </div>

            <span className="text-[9px] font-bold uppercase tracking-widest text-slate-700">
              6 tools
            </span>
          </div>

          <nav className="space-y-1">
            {nav.map(([href, label, icon]) => {
              const active =
                pathname === href ||
                (href !== "/dashboard" &&
                  pathname.startsWith(`${href}/`));

              return (
                <Link
                  key={href}
                  href={href}
                  onClick={() => setOpen(false)}
                  className={`side-link group ${
                    active ? "active" : ""
                  }`}
                >
                  <span
                    className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg transition ${
                      active
                        ? "bg-cyan-400/10 text-cyan-300"
                        : "bg-transparent text-slate-500 group-hover:bg-white/[0.04] group-hover:text-slate-300"
                    }`}
                  >
                    <Icon name={icon} size={17} />
                  </span>

                  <span className="flex-1">
                    {label}
                  </span>

                  {active && (
                    <span className="h-1.5 w-1.5 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(34,211,238,.7)]" />
                  )}
                </Link>
              );
            })}
          </nav>
          {isAdmin && (
            <div className="mt-5">
              <div className="mb-3 px-2 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">
                Administration
              </div>
          
              <Link
                href="/admin/users"
                onClick={() => setOpen(false)}
                className={`side-link group ${
                  pathname === "/admin/users"
                    ? "active"
                    : ""
                }`}
              >
                <span
                  className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg transition ${
                    pathname === "/admin/users"
                      ? "bg-cyan-400/10 text-cyan-300"
                      : "bg-transparent text-slate-500 group-hover:bg-white/[0.04] group-hover:text-slate-300"
                  }`}
                >
                  <Icon name="settings" size={17} />
                </span>
          
                <span className="flex-1">
                  User Management
                </span>
          
                {pathname === "/admin/users" && (
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(34,211,238,.7)]" />
                )}
              </Link>
            </div>
          )}
        </div>

        {/* Spacer */}
        <div className="min-h-4 flex-1" />

        {/* Lab Card */}
        <div className="shrink-0 px-4 pb-4">
          <div className="upgrade-card relative overflow-hidden">
            <div className="absolute -right-8 -top-8 h-20 w-20 rounded-full bg-cyan-400/10 blur-2xl" />

            <div className="relative">
              <div className="flex items-center gap-2 text-cyan-300">
                <div className="grid h-7 w-7 place-items-center rounded-lg bg-cyan-400/10">
                  <Icon name="spark" size={15} />
                </div>

                <span className="text-[10px] font-bold uppercase tracking-[0.18em]">
                  Quantum Lab
                </span>
              </div>

              <p className="mt-3 text-xs leading-5 text-slate-400">
                Analyze, debug and optimize your quantum
                circuits from one workspace.
              </p>

              <Link
                href="/analyzer"
                onClick={() => setOpen(false)}
                className="mt-4 flex items-center justify-center gap-2 rounded-xl border border-cyan-400/10 bg-white/[0.04] px-3 py-2.5 text-xs font-bold text-slate-200 transition hover:border-cyan-400/20 hover:bg-cyan-400/10 hover:text-cyan-200"
              >
                Start analysis
                <Icon name="arrow" size={13} />
              </Link>
            </div>
          </div>
        </div>

        {/* Account */}
        <div className="sticky bottom-0 z-10 shrink-0 border-t border-white/5 bg-slate-950/95 p-4 backdrop-blur-xl">
          <Link
            href="/settings"
            onClick={() => setOpen(false)}
            className="mb-3 flex items-center gap-3 rounded-xl border border-white/5 bg-white/[0.02] px-3 py-3 transition hover:border-cyan-400/10 hover:bg-white/[0.04]"
          >
            <div className="grid h-9 w-9 shrink-0 place-items-center rounded-full border border-cyan-400/20 bg-cyan-400/10 text-sm font-black text-cyan-300">
              {user?.name?.slice(0, 1).toUpperCase() ||
                "Q"}
            </div>

            <div className="min-w-0">
              <p className="truncate text-xs font-bold text-slate-200">
                {user?.name || "Quantum User"}
              </p>

              <p className="truncate text-[10px] text-slate-600">
                {user?.email || "Authenticated"}
              </p>
            </div>

            <Icon
              name="arrow"
              size={13}
              className="ml-auto rotate-[-45deg] text-slate-600"
            />
          </Link>

          <button
            type="button"
            onClick={logout}
            className="side-link w-full text-rose-300 hover:bg-rose-400/[0.06] hover:text-rose-200"
          >
            <span className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-rose-400/5">
              <Icon name="logout" size={17} />
            </span>

            <span>Log out</span>
          </button>
        </div>
      </aside>

      {/* Main */}
      <div className="lg:pl-[248px]">
        {/* Topbar */}
        <header className="topbar">
          <div className="flex items-center gap-3">
            <button
              type="button"
              aria-label="Open navigation"
              className="icon-btn lg:hidden"
              onClick={() => setOpen(true)}
            >
              <Icon name="menu" />
            </button>

            <div className="hidden sm:block">
              <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">
                QuantumInsight
              </p>

              <p className="mt-0.5 text-xs text-slate-500">
                Quantum circuit intelligence
              </p>
            </div>
          </div>

          <div className="ml-auto flex items-center gap-3">
            <Link
              href="/analyzer"
              className="top-action hidden sm:flex"
            >
              <Icon name="zap" size={15} />
              <button
                type="button"
                onClick={() =>
                  setTheme((current) =>
                    current === "dark" ? "light" : "dark"
                  )
                }
                className="top-action"
                aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
                title="Change color theme"
              >
                <span aria-hidden="true">
                  {theme === "dark" ? "☀" : "☾"}
                </span>
                <span className="hidden sm:inline">
                  {theme === "dark" ? "Light mode" : "Dark mode"}
                </span>
              </button>
              New analysis
            </Link>

            <Link
              href="/settings"
              className="group flex items-center gap-2 rounded-xl border border-white/5 bg-white/[0.02] px-2 py-1.5 transition hover:border-cyan-400/10 hover:bg-white/[0.04]"
              title={user?.name || "Settings"}
            >
              <span className="avatar">
                {user?.name?.slice(0, 1).toUpperCase() ||
                  "Q"}
              </span>

              <span className="hidden max-w-[120px] truncate text-xs font-semibold text-slate-400 transition group-hover:text-slate-200 md:block">
                {user?.name || "Settings"}
              </span>
            </Link>
          </div>
        </header>

        {/* Content */}
        <main className="mx-auto min-h-screen max-w-[1500px] px-4 pb-14 pt-7 sm:px-6 lg:px-8">
          {children}

          {/* Footer */}
          <footer className="mt-16 border-t border-white/5 pt-6">
            <div className="flex flex-col items-center justify-between gap-3 text-center sm:flex-row sm:text-left">
              <p className="text-xs text-slate-500">
                © 2026 QuantumInsight. All rights reserved.
              </p>

              <p className="text-xs text-slate-600">
                Designed &amp; Developed by{" "}
                <span className="text-slate-400">
                  Mohammad Bilal Irfan Shaikh
                </span>
              </p>
            </div>
          </footer>
        </main>
      </div>

      {/* Mobile overlay */}
      {open && (
        <button
          type="button"
          aria-label="Close menu"
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-[2px] lg:hidden"
        />
      )}

      {/* Session restore indicator */}
      {loading && (
        <div className="fixed bottom-4 right-4 z-50 flex items-center gap-2 rounded-xl border border-white/10 bg-slate-950/95 px-4 py-3 text-xs text-slate-300 shadow-2xl">
          <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-cyan-300" />
          Restoring session…
        </div>
      )}
    </div>
  );
}
