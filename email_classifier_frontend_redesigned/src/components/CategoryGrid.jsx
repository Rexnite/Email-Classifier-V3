const CATEGORIES = [
  {
    key: 'urgent-important',
    label: 'Urgent + Important',
    description: 'Critical work, security alerts, hard deadlines and high-value messages requiring immediate attention.',
    accent: 'from-rose-400 to-orange-400',
    ring: 'ring-rose-300/20',
  },
  {
    key: 'important-not-urgent',
    label: 'Important, Not Urgent',
    description: 'Strategic or valuable messages that should be scheduled instead of handled immediately.',
    accent: 'from-blue-400 to-cyan-300',
    ring: 'ring-blue-300/20',
  },
  {
    key: 'urgent-not-important',
    label: 'Urgent, Not Important',
    description: 'Time-sensitive interruptions that need quick action but have lower long-term value.',
    accent: 'from-amber-300 to-yellow-500',
    ring: 'ring-amber-300/20',
  },
  {
    key: 'neither',
    label: 'Neither',
    description: 'Low-signal messages, newsletters, promotions and non-critical inbox noise.',
    accent: 'from-slate-400 to-slate-600',
    ring: 'ring-slate-300/10',
  },
]

export default function CategoryGrid({ emails = [] }) {
  return (
    <div className="grid grid-cols-1 gap-4">
      {CATEGORIES.map((cat) => {
        const count = emails.filter((email) => email.classification === cat.key).length

        return (
          <div
            key={cat.key}
            className={`group rounded-[1.75rem] border border-white/10 bg-white/[0.045] p-5 shadow-soft ring-1 ${cat.ring} backdrop-blur-xl transition hover:-translate-y-0.5 hover:bg-white/[0.07]`}
          >
            <div className="flex items-center justify-between gap-5">
              <div className="min-w-0 flex-1">
                <div className={`mb-4 h-1.5 w-20 rounded-full bg-gradient-to-r ${cat.accent}`} />

                <h3 className="text-base font-semibold leading-snug text-white">
                  {cat.label}
                </h3>

                <p className="mt-2 max-w-sm text-sm leading-6 text-slate-400">
                  {cat.description}
                </p>
              </div>

              <div className="shrink-0 rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-right">
                <p className="text-3xl font-semibold text-white">{count}</p>
                <p className="mt-1 text-[10px] uppercase tracking-[0.18em] text-slate-500">
                  classified
                </p>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}