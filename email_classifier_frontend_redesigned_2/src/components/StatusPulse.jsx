export default function StatusPulse({ state = 'idle', label }) {
  const palette = {
    live: 'text-emerald-300 bg-emerald-400/15 ring-emerald-300/30',
    idle: 'text-slate-400 bg-slate-400/10 ring-slate-300/10',
    error: 'text-rose-300 bg-rose-400/15 ring-rose-300/30',
    loading: 'text-cyan-300 bg-cyan-400/15 ring-cyan-300/30',
  }

  const color = palette[state] || palette.idle

  return (
    <div className={`inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-medium ring-1 ${color}`}>
      <span className="relative flex h-2.5 w-2.5">
        {(state === 'live' || state === 'loading') && <span className="status-dot absolute inset-0 rounded-full bg-current" />}
        <span className="relative h-2.5 w-2.5 rounded-full bg-current" />
      </span>
      <span>{label}</span>
    </div>
  )
}
