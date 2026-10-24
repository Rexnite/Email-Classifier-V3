function initialsFromSender(sender = '') {
  const clean = sender.replace(/<.*>/, '').trim()
  const parts = clean.split(/\s+/).filter(Boolean)
  if (!parts.length) return 'M'
  return parts.slice(0, 2).map((part) => part[0]).join('').toUpperCase()
}

function senderName(sender = '') {
  return sender.replace(/<.*>/, '').replaceAll('"', '').trim() || 'Unknown Sender'
}

function badgeText(value, fallback = 'Pending') {
  if (!value) return fallback
  return value
}

function categoryLabel(email) {
  if (email.classification_label) return email.classification_label

  const labels = {
    'urgent-important': 'Urgent + Important',
    'important-not-urgent': 'Important, Not Urgent',
    'urgent-not-important': 'Urgent, Not Important',
    neither: 'Neither',
    unclassified: 'Unclassified',
  }

  return labels[email.classification] || 'Pending'
}

export default function EmailCard({ email }) {
  const initials = initialsFromSender(email.sender)
  const subject = email.subject || '(No subject)'
  const snippet = email.snippet || email.body || 'No preview available.'
  const summary = email.summary

  return (
    <article className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.045] p-5 shadow-soft backdrop-blur-xl transition duration-200 hover:-translate-y-0.5 hover:border-cyan-300/30 hover:bg-white/[0.075] hover:shadow-glow">
      <div className="absolute left-0 top-0 h-full w-1 bg-gradient-to-b from-cyan-300 via-blue-500 to-violet-500 opacity-70" />

      <div className="flex gap-4 pl-2">
        <div className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-slate-700 to-slate-900 text-sm font-bold text-cyan-100 ring-1 ring-white/10">
          {initials}
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-slate-200">
                {senderName(email.sender)}
              </p>

              <h3 className="mt-1 truncate text-base font-semibold tracking-tight text-white">
                {subject}
              </h3>
            </div>

            <span className="shrink-0 rounded-full border border-white/10 bg-slate-950/60 px-2.5 py-1 font-mono text-[10px] text-slate-500">
              {email.id?.slice(0, 8) || 'new'}
            </span>
          </div>

          {summary ? (
            <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-300">
              {summary}
            </p>
          ) : (
            <p className="mt-3 line-clamp-2 text-sm leading-6 text-slate-400">
              {snippet}
            </p>
          )}

          {email.classification_error && (
            <p className="mt-3 rounded-2xl border border-rose-400/20 bg-rose-400/10 px-3 py-2 text-xs text-rose-200">
              Classification error: {email.classification_error}
            </p>
          )}

          <div className="mt-4 flex flex-wrap gap-2">
            <span className="rounded-full bg-cyan-300/10 px-3 py-1 text-[11px] font-semibold text-cyan-200 ring-1 ring-cyan-300/20">
              Urgency: {badgeText(email.urgency)}
            </span>

            <span className="rounded-full bg-violet-300/10 px-3 py-1 text-[11px] font-semibold text-violet-200 ring-1 ring-violet-300/20">
              Importance: {badgeText(email.importance)}
            </span>

            <span className="rounded-full bg-white/[0.06] px-3 py-1 text-[11px] font-semibold text-slate-300 ring-1 ring-white/10">
              Category: {categoryLabel(email)}
            </span>
          </div>
        </div>
      </div>
    </article>
  )
}