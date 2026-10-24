import CategoryGrid from './CategoryGrid.jsx'
import ExportBar from './ExportBar.jsx'

export default function InsightPanel({ emails = [] }) {
  return (
    <aside className="space-y-5 2xl:sticky 2xl:top-24 2xl:self-start">
      <div className="rounded-[2rem] border border-white/10 bg-white/[0.045] p-5 shadow-soft backdrop-blur-xl">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-cyan-300/80">
          AI Overview
        </p>

        <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="rounded-3xl bg-slate-950/70 p-4 ring-1 ring-white/10">
            <p className="text-3xl font-semibold text-white">{emails.length}</p>
            <p className="mt-1 text-xs text-slate-500">unread fetched</p>
          </div>

          <div className="rounded-3xl bg-slate-950/70 p-4 ring-1 ring-white/10">
            <p className="text-3xl font-semibold text-white">4</p>
            <p className="mt-1 text-xs text-slate-500">matrix lanes</p>
          </div>
        </div>

        <p className="mt-4 text-sm leading-6 text-slate-400">
          Classification agents are ready for the next integration step. Current UI shows Gmail fetch and pending AI triage states.
        </p>
      </div>

      <CategoryGrid emails={emails} />

      <div className="rounded-[2rem] border border-white/10 bg-white/[0.045] p-5 shadow-soft backdrop-blur-xl">
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
          Exports
        </p>
        <ExportBar />
      </div>
    </aside>
  )
}