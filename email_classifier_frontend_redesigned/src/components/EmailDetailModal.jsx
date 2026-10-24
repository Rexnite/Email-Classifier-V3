import { useEffect, useState } from 'react'
import { fetchEmailBody } from '../lib/api.js'

export default function EmailDetailModal({ email, onClose, onBodyLoaded }) {
  const [body, setBody] = useState(email?.full_body || null)
  const [loading, setLoading] = useState(!email?.full_body)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!email) return

    if (email.full_body) {
      setBody(email.full_body)
      setLoading(false)
      return
    }

    let cancelled = false
    setLoading(true)
    setError(null)

    fetchEmailBody(email.id)
      .then((data) => {
        if (!cancelled) {
          const fullBody = data.body || '(No body found)'
          setBody(fullBody)
          setLoading(false)
          // Persist the fetched body into the shared email list so
          // reopening this modal for the same email (without a full
          // page refresh) reads it straight from state instead of
          // hitting the backend again.
          onBodyLoaded?.(email.id, fullBody)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message || 'Failed to load full email body.')
          setLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [email, onBodyLoaded])

  if (!email) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4 backdrop-blur-sm">
      <div className="max-h-[85vh] w-full max-w-2xl overflow-hidden rounded-[2rem] border border-white/10 bg-slate-950/95 shadow-2xl">
        <div className="flex items-start justify-between gap-4 border-b border-white/10 px-6 py-5">
          <div className="min-w-0">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300/80">
              Full email
            </p>
            <h3 className="mt-1 truncate text-lg font-semibold text-white">
              {email.subject || '(No subject)'}
            </h3>
            <p className="mt-1 truncate text-xs text-slate-400">{email.sender}</p>
          </div>

          <button
            onClick={onClose}
            className="shrink-0 rounded-full border border-white/10 bg-white/[0.06] px-3 py-1.5 text-xs font-semibold text-slate-300 transition hover:bg-white/[0.12]"
          >
            Close
          </button>
        </div>

        <div className="max-h-[65vh] overflow-y-auto px-6 py-5">
          {loading && (
            <div className="flex items-center gap-3 text-sm text-slate-400">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              Loading full message…
            </div>
          )}

          {!loading && error && (
            <p className="rounded-2xl border border-rose-400/20 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">
              {error}
            </p>
          )}

          {!loading && !error && (
            <pre className="whitespace-pre-wrap text-sm leading-6 text-slate-300">{body}</pre>
          )}
        </div>
      </div>
    </div>
  )
}
