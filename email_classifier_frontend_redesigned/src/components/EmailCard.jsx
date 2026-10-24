import { useState } from 'react'
import { summarizeEmail, validateEmail } from '../lib/api.js'
import ValidationBadge from './ValidationBadge.jsx'

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

export default function EmailCard({ email, onPatch, onReadFullBody, geminiConfigured, onRequestGeminiKey }) {
  const [summarizing, setSummarizing] = useState(false)
  const [summarizeError, setSummarizeError] = useState(null)
  const [validating, setValidating] = useState(false)
  const [validateError, setValidateError] = useState(null)

  const initials = initialsFromSender(email.sender)
  const subject = email.subject || '(No subject)'
  const snippet = email.snippet || email.body || 'No preview available.'
  const summary = email.summary

  const handleSummarize = async () => {
    setSummarizing(true)
    setSummarizeError(null)

    // If a summary already exists, the button reads "Re-summarize" -- so
    // this click must actually force regeneration, otherwise the backend
    // just returns the cached summary unchanged and the button is a lie.
    const force = Boolean(summary)

    try {
      const result = await summarizeEmail(email.id, force)
      onPatch?.(email.id, {
        summary: result.summary,
        summary_error: result.summary_error,
      })
    } catch (err) {
      setSummarizeError(err.message || 'Failed to generate summary.')
    } finally {
      setSummarizing(false)
    }
  }

  const handleValidate = async () => {
    if (geminiConfigured === false) {
      onRequestGeminiKey?.()
      return
    }

    setValidating(true)
    setValidateError(null)

    try {
      const result = await validateEmail(email.id)

      if (!result.validator_used && result.configured === false) {
        // Key was removed/never configured between page load and click --
        // prompt for it instead of showing a raw error.
        onRequestGeminiKey?.()
        return
      }

      onPatch?.(email.id, {
        validation_result: result,
        ...(result.corrected_by_validator
          ? {
              urgency: result.suggested.urgency,
              importance: result.suggested.importance,
              classification: result.suggested.classification,
              classification_label: result.suggested.classification_label,
              corrected_by_validator: true,
            }
          : {}),
      })
    } catch (err) {
      setValidateError(err.message || 'Failed to validate email.')
    } finally {
      setValidating(false)
    }
  }

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

          {summarizeError && (
            <p className="mt-3 rounded-2xl border border-rose-400/20 bg-rose-400/10 px-3 py-2 text-xs text-rose-200">
              {summarizeError}
            </p>
          )}

          {validateError && (
            <p className="mt-3 rounded-2xl border border-rose-400/20 bg-rose-400/10 px-3 py-2 text-xs text-rose-200">
              {validateError}
            </p>
          )}

          <ValidationBadge result={email.validation_result} />

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

          <div className="mt-4 flex flex-wrap gap-2 border-t border-white/5 pt-4">
            <button
              onClick={() => onReadFullBody?.(email)}
              className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-[11px] font-semibold text-slate-300 transition hover:bg-white/[0.09]"
            >
              Read full email
            </button>

            <button
              onClick={handleSummarize}
              disabled={summarizing}
              className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1.5 text-[11px] font-semibold text-cyan-200 transition hover:border-cyan-300/40 hover:bg-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {summarizing ? 'Summarizing…' : summary ? 'Re-summarize' : 'Summarize'}
            </button>

            <button
              onClick={handleValidate}
              disabled={validating}
              className="rounded-full border border-violet-300/20 bg-violet-300/10 px-3 py-1.5 text-[11px] font-semibold text-violet-200 transition hover:border-violet-300/40 hover:bg-violet-300/15 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {validating ? 'Validating…' : 'Validate'}
            </button>
          </div>
        </div>
      </div>
    </article>
  )
}
