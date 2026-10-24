const navItems = [
  { label: 'Inbox', count: null, active: true },
  { label: 'Urgent + Important', count: 0, accent: 'bg-rose-400' },
  { label: 'Important', count: 0, accent: 'bg-blue-400' },
  { label: 'Low Priority', count: 0, accent: 'bg-slate-400' },
  { label: 'Exports', count: null },
  { label: 'Settings', count: null },
]

export default function Sidebar({ authenticated, emailCount = 0 }) {
  return (
    <aside className="hidden min-h-screen w-72 shrink-0 border-r border-white/10 bg-slate-950/70 px-5 py-6 backdrop-blur-xl lg:block">
      <div className="mb-9 flex items-center gap-3">
        <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-cyan-300 via-blue-500 to-violet-500 shadow-glow">
          <span className="text-lg font-black text-white">AI</span>
        </div>
        <div>
          <h1 className="text-sm font-semibold tracking-wide text-white">Gmail AI Classifier</h1>
          <p className="text-xs text-slate-400">agentic inbox triage</p>
        </div>
      </div>

      <div className="mb-6 rounded-3xl border border-white/10 bg-white/[0.04] p-4 shadow-soft">
        <p className="text-[11px] uppercase tracking-[0.25em] text-slate-500">Connection</p>
        <div className="mt-3 flex items-center justify-between">
          <span className="text-sm text-slate-200">Gmail</span>
          <span className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${authenticated ? 'bg-emerald-400/10 text-emerald-300 ring-1 ring-emerald-300/20' : 'bg-slate-400/10 text-slate-400 ring-1 ring-white/10'}`}>
            {authenticated ? 'Connected' : 'Offline'}
          </span>
        </div>
        <p className="mt-3 text-xs leading-relaxed text-slate-500">Read-only OAuth access. No email is modified or marked as read.</p>
      </div>

      <nav className="space-y-1.5">
        {navItems.map((item) => (
          <button
            key={item.label}
            className={`group flex w-full items-center justify-between rounded-2xl px-3 py-3 text-sm transition ${item.active ? 'bg-white/10 text-white shadow-soft' : 'text-slate-400 hover:bg-white/[0.06] hover:text-slate-100'}`}
          >
            <span className="flex items-center gap-3">
              <span className={`h-2 w-2 rounded-full ${item.accent || (item.active ? 'bg-cyan-300' : 'bg-slate-700')}`} />
              {item.label}
            </span>
            {item.label === 'Inbox' ? (
              <span className="rounded-full bg-white/10 px-2 py-0.5 text-xs text-slate-300">{emailCount}</span>
            ) : item.count !== null ? (
              <span className="rounded-full bg-white/[0.06] px-2 py-0.5 text-xs text-slate-500">{item.count}</span>
            ) : null}
          </button>
        ))}
      </nav>

      <div className="mt-8 rounded-3xl border border-cyan-300/20 bg-cyan-300/[0.06] p-4">
        <p className="text-sm font-semibold text-cyan-100">Local AI Mode</p>
        <p className="mt-2 text-xs leading-relaxed text-cyan-100/60">Ollama agents classify urgency and importance locally for privacy-first triage.</p>
      </div>
    </aside>
  )
}
