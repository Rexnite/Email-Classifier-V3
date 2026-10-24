export default function EmptyState({ title, message, loading = false, variant = 'default' }) {
  const tone = variant === 'error' ? 'from-rose-400/20 to-orange-400/10 text-rose-200' : 'from-cyan-300/20 to-violet-400/10 text-cyan-100'

  return (
    <div className="rounded-[2rem] border border-white/10 bg-white/[0.045] p-10 text-center shadow-soft backdrop-blur-xl">
      <div className={`mx-auto mb-5 grid h-14 w-14 place-items-center rounded-3xl bg-gradient-to-br ${tone} ring-1 ring-white/10`}>
        {loading ? <span className="h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" /> : <span className="text-2xl">✦</span>}
      </div>
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-400">{message}</p>
    </div>
  )
}
