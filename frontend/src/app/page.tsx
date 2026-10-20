import Link from "next/link";
import Image from "next/image";
import { Icon } from "../components/Icons";

const features = [
  {
    title: "Quantum Circuit Analysis",
    description:
      "Extract qubits, gates, circuit depth and two-qubit operations from Qiskit source code.",
    icon: "analyze",
  },
  {
    title: "Quantum Debugger",
    description:
      "Inspect common Qiskit construction and runtime errors and understand the reported issue.",
    icon: "bug",
  },
  {
    title: "Circuit Optimization",
    description:
      "Identify optimization opportunities and compare circuit characteristics before and after optimization.",
    icon: "zap",
  },
  {
    title: "Anomaly Detection",
    description:
      "Use circuit features to identify unusual patterns that may require further inspection.",
    icon: "spark",
  },
];

const metrics = [
  ["Qubits", "3"],
  ["Gates", "4"],
  ["Depth", "3"],
  ["2Q Gates", "2"],
];

export default function Home() {
  return (
    <div className="relative overflow-hidden rounded-[24px] border border-white/10 bg-slate-950">
      {/* Subtle background accents */}
      <div className="pointer-events-none absolute left-[-180px] top-20 h-80 w-80 rounded-full bg-cyan-500/10 blur-3xl" />
      <div className="pointer-events-none absolute right-[-180px] top-40 h-80 w-80 rounded-full bg-blue-500/10 blur-3xl" />

      {/* Header */}
      <header className="relative flex items-center justify-between border-b border-white/10 px-6 py-5 sm:px-10 lg:px-12">
        <Link href="/" className="flex items-center">
          <Image
            src="/logo.svg"
            alt="QuantumInsight logo"
            width={180}
            height={85}
            className="h-auto w-[145px] object-contain sm:w-[165px]"
          />
        </Link>

        <div className="flex items-center gap-3">
          <Link href="/login" className="btn btn-secondary">
            Sign in
            <Icon name="arrow" size={15} />
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative px-6 pb-16 pt-14 sm:px-10 sm:pt-20 lg:px-16 lg:pb-20">
        <div className="mx-auto grid max-w-6xl items-center gap-14 lg:grid-cols-[1.05fr_.95fr]">
          {/* Hero text */}
          <div>
            <div className="inline-flex items-center gap-2 rounded-lg border border-cyan-400/20 bg-cyan-400/5 px-3 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-300">
              Quantum circuit analysis
            </div>

            <h1 className="mt-6 max-w-3xl text-4xl font-bold leading-[1.05] tracking-[-0.035em] text-white sm:text-6xl">
              Analyze and improve
              <span className="block text-cyan-300">
                Qiskit circuits.
              </span>
            </h1>

            <p className="mt-6 max-w-2xl text-base leading-7 text-slate-400 sm:text-lg">
              QuantumInsight is a quantum circuit analysis and optimization
              workspace for inspecting circuit structure, measuring health,
              finding anomalies and understanding optimization opportunities.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/register"
                className="btn btn-primary px-6 py-3"
              >
                Create account
                <Icon name="arrow" size={16} />
              </Link>

              <Link
                href="/login"
                className="btn btn-secondary px-6 py-3"
              >
                Open workspace
              </Link>
            </div>

            <div className="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-xs text-slate-500">
              <span>Qiskit-compatible analysis</span>
              <span>Static-safe parsing</span>
              <span>QHI + QMI metrics</span>
            </div>
          </div>

          {/* Technical preview */}
          <div className="relative">
            <div className="rounded-2xl border border-white/10 bg-slate-900/80 shadow-2xl">
              {/* Preview header */}
              <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
                <div>
                  <p className="text-sm font-semibold text-white">
                    Circuit Analysis
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    sample_circuit.py
                  </p>
                </div>

                <span className="rounded-md border border-emerald-400/20 bg-emerald-400/5 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-emerald-300">
                  analyzed
                </span>
              </div>

              {/* Circuit */}
              <div className="border-b border-white/10 px-5 py-6">
                <div className="space-y-5 font-mono text-xs text-slate-300">
                  <div className="flex items-center gap-2">
                    <span className="w-6 text-slate-500">q0</span>
                    <span>──</span>
                    <span className="rounded border border-cyan-400/30 bg-cyan-400/10 px-2 py-1 text-cyan-300">
                      H
                    </span>
                    <span>────●────────</span>
                    <span className="rounded border border-slate-600 px-2 py-1 text-slate-400">
                      M
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="w-6 text-slate-500">q1</span>
                    <span>───────</span>
                    <span className="rounded border border-blue-400/30 bg-blue-400/10 px-2 py-1 text-blue-300">
                      X
                    </span>
                    <span>────┼───────</span>
                    <span className="rounded border border-slate-600 px-2 py-1 text-slate-400">
                      M
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="w-6 text-slate-500">q2</span>
                    <span>────────────●───</span>
                    <span className="rounded border border-slate-600 px-2 py-1 text-slate-400">
                      M
                    </span>
                  </div>
                </div>
              </div>

              {/* Metrics */}
              <div className="grid grid-cols-2 gap-px bg-white/5 sm:grid-cols-4">
                {metrics.map(([label, value]) => (
                  <div
                    key={label}
                    className="bg-slate-900 px-4 py-4"
                  >
                    <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                      {label}
                    </p>
                    <p className="mt-1 text-xl font-semibold text-white">
                      {value}
                    </p>
                  </div>
                ))}
              </div>

              {/* Health */}
              <div className="border-t border-white/10 px-5 py-5">
                <div className="flex items-end justify-between">
                  <div>
                    <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                      Quantum Health Index
                    </p>

                    <p className="mt-1 text-3xl font-bold text-cyan-300">
                      86.4
                      <span className="ml-1 text-sm font-normal text-slate-500">
                        / 100
                      </span>
                    </p>
                  </div>

                  <span className="rounded-md border border-emerald-400/20 bg-emerald-400/5 px-2.5 py-1 text-xs font-medium text-emerald-300">
                    Healthy
                  </span>
                </div>

                <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-800">
                  <div className="h-full w-[86.4%] rounded-full bg-cyan-400" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* What it does */}
      <section className="relative border-t border-white/10 px-6 py-16 sm:px-10 lg:px-16">
        <div className="mx-auto max-w-6xl">
          <div className="max-w-2xl">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">
              Analysis workflow
            </p>

            <h2 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              From circuit source to measurable engineering insights.
            </h2>

            <p className="mt-4 text-sm leading-6 text-slate-400 sm:text-base">
              QuantumInsight combines static circuit analysis, measurable
              health indicators and optimization tools in a single workspace.
            </p>
          </div>

          <div className="mt-10 grid gap-4 md:grid-cols-2">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="rounded-2xl border border-white/10 bg-slate-900/50 p-6 transition-colors hover:border-cyan-400/20"
              >
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-cyan-400/15 bg-cyan-400/5 text-cyan-300">
                    <Icon name={feature.icon} />
                  </div>

                  <div>
                    <h3 className="text-base font-semibold text-white">
                      {feature.title}
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-400">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Methodology */}
      <section className="relative border-t border-white/10 bg-slate-900/30 px-6 py-16 sm:px-10 lg:px-16">
        <div className="mx-auto max-w-6xl">
          <div className="grid gap-10 lg:grid-cols-[.8fr_1.2fr] lg:items-start">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">
                How analysis works
              </p>

              <h2 className="mt-3 text-3xl font-bold tracking-tight text-white">
                Transparent circuit analysis.
              </h2>

              <p className="mt-4 text-sm leading-6 text-slate-400">
                Circuit source is parsed into measurable features before
                health, anomaly and optimization results are produced.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-4">
              {[
                ["01", "Parse", "Read circuit structure"],
                ["02", "Measure", "Extract circuit metrics"],
                ["03", "Evaluate", "Calculate health indicators"],
                ["04", "Recommend", "Identify improvements"],
              ].map(([number, title, description]) => (
                <div
                  key={number}
                  className="rounded-xl border border-white/10 bg-slate-950/60 p-4"
                >
                  <span className="text-[10px] font-bold tracking-wider text-cyan-400">
                    {number}
                  </span>

                  <h3 className="mt-3 text-sm font-semibold text-white">
                    {title}
                  </h3>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Technology */}
      <section className="relative border-t border-white/10 px-6 py-12 sm:px-10 lg:px-16">
        <div className="mx-auto flex max-w-6xl flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
              Project stack
            </p>

            <p className="mt-2 text-sm text-slate-400">
              Next.js · React · FastAPI · Qiskit · Supabase · Scikit-learn
            </p>
          </div>

          <p className="text-xs text-slate-600">
            QuantumInsight — quantum circuit engineering workspace
          </p>
        </div>
      </section>
    </div>
  );
}
