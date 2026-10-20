"use client";

import Image from "next/image";
import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Icon } from "../../components/Icons";
import { useAuth } from "../../lib/auth";
import { supabase } from "../../lib/supabase";

export default function LoginPage() {
  const { login, googleLogin, user, loading } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [show, setShow] = useState(false);

  async function signInWithGoogle() {
    setError("");
    setBusy(true);

    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: window.location.origin + "/login",
        queryParams: {
          prompt: "select_account",
        },
      },
    });

    if (error) {
      setError(error.message);
      setBusy(false);
    }
  }

  useEffect(() => {
    async function handleGoogleCallback() {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session?.access_token) {
        return;
      }

      try {
        await googleLogin();
        router.replace("/dashboard");
      } catch (err: any) {
        setError(err.message || "Google sign-in failed.");
        setBusy(false);
      }
    }

    if (!loading) {
      if (user) {
        router.replace("/dashboard");
      } else {
        handleGoogleCallback();
      }
    }
  }, [loading, user, router, googleLogin]);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);

    try {
      await login(email, password);
      router.replace("/dashboard");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-panel">
        {/* Left visual panel */}
        <div className="auth-art">
          <div className="relative z-10 flex items-center justify-between">
            <Link href="/" className="inline-block">
              <Image
                src="/logo.svg"
                alt="QuantumInsight"
                width={210}
                height={100}
                className="h-auto w-[190px] object-contain"
                priority
              />
            </Link>

            <div className="rounded-xl border border-cyan-400/10 bg-cyan-400/5 px-3 py-2">
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-300 shadow-[0_0_10px_rgba(110,231,183,.8)]" />
                <span className="text-[9px] font-bold uppercase tracking-[0.16em] text-cyan-300">
                  Secure workspace
                </span>
              </div>
            </div>
          </div>

          <div className="quantum-ring">
            <div className="relative z-10 text-center">
              <div className="text-5xl font-black gradient-text">
                Q
              </div>

              <p className="mt-2 text-[10px] font-bold uppercase tracking-[.22em] text-slate-400">
                Circuit intelligence
              </p>
            </div>
          </div>

          <div className="relative z-10 max-w-lg">
            <p className="section-kicker">
              Your quantum workspace
            </p>

            <h1 className="mt-3 text-3xl font-black leading-tight sm:text-4xl">
              Turn complex circuits into clear engineering decisions.
            </h1>

            <p className="mt-4 max-w-md text-sm leading-6 text-slate-400">
              Keep your analyses, optimization experiments and
              debugging workflow together in one secure
              QuantumInsight workspace.
            </p>

            <div className="mt-7 grid gap-3 sm:grid-cols-3">
              <Feature
                icon="analyze"
                title="Analyze"
                text="Inspect circuit health"
              />

              <Feature
                icon="zap"
                title="Optimize"
                text="Reduce circuit overhead"
              />

              <Feature
                icon="bug"
                title="Debug"
                text="Understand errors"
              />
            </div>
          </div>
        </div>

        {/* Login panel */}
        <div className="auth-form">
          <div className="mx-auto max-w-md">
            <Link
              href="/"
              className="mb-9 inline-flex items-center gap-2 text-xs font-bold text-slate-500 transition hover:text-white"
            >
              <span>←</span>
              Back to QuantumInsight
            </Link>

            <div className="mb-7">
              <p className="section-kicker">
                Welcome back
              </p>

              <h2 className="mt-2 text-3xl font-black tracking-tight text-white">
                Sign in to your workspace
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Use your QuantumInsight account to continue
                where you left off.
              </p>
            </div>

            {/* Google */}
            <button
              type="button"
              onClick={signInWithGoogle}
              disabled={busy}
              className="group flex w-full items-center justify-center gap-3 rounded-xl border border-white/10 bg-white/[.035] px-4 py-3.5 text-sm font-bold text-slate-200 transition hover:border-cyan-400/20 hover:bg-white/[.06] disabled:cursor-not-allowed disabled:opacity-50"
            >
              <span className="grid h-6 w-6 place-items-center rounded-lg bg-white text-sm font-black text-slate-900 shadow-sm">
                G
              </span>

              <span>
                {busy ? "Connecting…" : "Continue with Google"}
              </span>
            </button>

            {/* Divider */}
            <div className="my-6 flex items-center gap-3 text-[10px] font-bold uppercase tracking-widest text-slate-600">
              <span className="h-px flex-1 bg-white/5" />
              <span>or continue with email</span>
              <span className="h-px flex-1 bg-white/5" />
            </div>

            <form onSubmit={submit} className="space-y-5">
              {/* Email */}
              <label className="block">
                <span className="mb-2 block text-xs font-bold text-slate-300">
                  Email address
                </span>

                <div className="relative">
                  <Icon
                    name="mail"
                    size={17}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"
                  />

                  <input
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    type="email"
                    required
                    autoComplete="email"
                    placeholder="you@example.com"
                    className="w-full pl-10"
                  />
                </div>
              </label>

              {/* Password */}
              <label className="block">
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-300">
                    Password
                  </span>

                  <Link
                    href="/forgot-password"
                    className="text-xs font-semibold text-cyan-400 transition hover:text-cyan-300"
                  >
                    Forgot password?
                  </Link>
                </div>

                <div className="relative">
                  <Icon
                    name="lock"
                    size={17}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"
                  />

                  <input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type={show ? "text" : "password"}
                    required
                    autoComplete="current-password"
                    placeholder="••••••••"
                    className="w-full pl-10 pr-16"
                  />

                  <button
                    type="button"
                    onClick={() => setShow(!show)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 rounded-md px-1 text-[10px] font-bold uppercase tracking-wider text-slate-600 transition hover:text-white"
                  >
                    {show ? "Hide" : "Show"}
                  </button>
                </div>
              </label>

              {/* Error */}
              {error && (
                <div className="flex gap-3 rounded-xl border border-rose-400/20 bg-rose-400/[.07] p-3.5">
                  <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-full bg-rose-400/10 text-[10px] font-black text-rose-300">
                    !
                  </span>

                  <p className="text-sm leading-5 text-rose-200/90">
                    {error}
                  </p>
                </div>
              )}

              {/* Sign in */}
              <button
                type="submit"
                disabled={busy}
                className="btn btn-primary w-full justify-center py-3.5"
              >
                {busy ? (
                  <>
                    <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                    Signing in…
                  </>
                ) : (
                  <>
                    Sign in
                    <Icon name="arrow" size={16} />
                  </>
                )}
              </button>
            </form>

            {/* Register */}
            <div className="my-7 flex items-center gap-3 text-[10px] font-bold uppercase tracking-widest text-slate-600">
              <span className="h-px flex-1 bg-white/5" />
              New here?
              <span className="h-px flex-1 bg-white/5" />
            </div>

            <Link
              href="/register"
              className="btn btn-secondary w-full justify-center"
            >
              Create an account
              <Icon name="arrow" size={15} />
            </Link>

            {/* Security note */}
            <div className="mt-6 flex gap-3 rounded-xl border border-white/5 bg-white/[.015] p-3.5">
              <Icon
                name="shield"
                size={15}
                className="mt-0.5 shrink-0 text-cyan-300"
              />

              <p className="text-[10px] leading-5 text-slate-600">
                Authentication uses password hashing and signed
                session tokens on the QuantumInsight API.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Feature({
  icon,
  title,
  text,
}: {
  icon: string;
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-xl border border-white/5 bg-white/[.025] p-3">
      <div className="flex items-center gap-2">
        <span className="grid h-7 w-7 place-items-center rounded-lg bg-cyan-400/5 text-cyan-300">
          <Icon name={icon} size={13} />
        </span>

        <p className="text-[11px] font-bold text-slate-300">
          {title}
        </p>
      </div>

      <p className="mt-2 text-[10px] leading-4 text-slate-600">
        {text}
      </p>
    </div>
  );
}
