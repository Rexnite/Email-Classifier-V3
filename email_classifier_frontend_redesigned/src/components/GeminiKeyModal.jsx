import { useState } from 'react'
import { saveGeminiKey } from '../lib/api.js'

export default function GeminiKeyModal({ onClose, onSaved }) {
  const [apiKey, setApiKey] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const handleSave = async (event) => {
    event.preventDefault()

    if (!apiKey.trim()) {
      setError('Enter a Gemini API key.')
      return
    }

    setSaving(true)
    setError(null)

    try {
      await saveGeminiKey(apiKey.trim())
      onSaved?.()
      onClose?.()
    } catch (err) {
      setError(err.message || 'Failed to save Gemini API key.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-[2rem] border border-white/10 bg-slate-950/95 p-6 shadow-2xl">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-violet-300/80">
          Validator setup
        </p>
        <h3 className="mt-2 text-xl font-semibold text-white">Connect Gemini API</h3>
        <p className="mt-2 text-sm leading-6 text-slate-400">
          The Gemini validator double-checks the local Ollama classification on demand. Paste
          your Gemini API key below — it is stored locally and only used to call Gemini when you
          click Validate. It is never shown again after saving.
        </p>

        <form onSubmit={handleSave} className="mt-5 space-y-3">
          <input
            type="password"
            autoFocus
            value={apiKey}
            onChange={(event) => setApiKey(event.target.value)}
            placeholder="Gemini API key"
            className="w-full rounded-2xl border border-white/10 bg-white/[0.05] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/40 focus:outline-none"
          />

          {error && (
            <p className="rounded-2xl border border-rose-400/20 bg-rose-400/10 px-3 py-2 text-xs text-rose-200">
              {error}
            </p>
          )}

          <div className="flex justify-end gap-2 pt-1">
            <button
              type="button"
              onClick={onClose}
              className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/[0.08]"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={saving}
              className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-semibold text-cyan-200 transition hover:border-cyan-300/40 hover:bg-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {saving ? 'Saving…' : 'Save key'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
