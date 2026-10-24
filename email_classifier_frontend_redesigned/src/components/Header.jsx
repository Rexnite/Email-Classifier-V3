import { logout } from '../lib/api.js'

function formatSyncTime(value) {
  if (!value) return 'Not synced yet'

  return new Intl.DateTimeFormat('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(new Date(value))
}

export default function Header({
  authenticated,
  lastSyncedAt,
  loading,
  onRefresh,
  geminiConfigured,
  onOpenGeminiSettings,
}) {
  const handleLogout = async () => {
    try {
      await logout()
      window.location.reload()
    } catch (error) {
      console.error(error)
      alert('Logout failed. Please try again.')
    }
  }

  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-slate-950/70 px-5 py-4 backdrop-blur-xl lg:px-8">
      <div className="flex flex-col justify-between gap-4 xl:flex-row xl:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-cyan-300/80">
            Email Classifier V3
          </p>

          <h1 className="mt-2 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
            Gmail AI Priority Dashboard
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            OAuth-powered Gmail ingestion with local Ollama classification.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs text-slate-400">
            Last sync:{' '}
            <span className="font-medium text-slate-200">
              {formatSyncTime(lastSyncedAt)}
            </span>
          </div>

          <div
            className={`rounded-full border px-4 py-2 text-xs font-semibold ${
              authenticated
                ? 'border-emerald-300/20 bg-emerald-300/10 text-emerald-200'
                : 'border-rose-300/20 bg-rose-300/10 text-rose-200'
            }`}
          >
            {authenticated ? 'Gmail Connected' : 'Gmail Disconnected'}
          </div>

          <button
            onClick={onOpenGeminiSettings}
            className={`rounded-full border px-4 py-2 text-xs font-semibold transition ${
              geminiConfigured
                ? 'border-violet-300/20 bg-violet-300/10 text-violet-200 hover:border-violet-300/40 hover:bg-violet-300/15'
                : 'border-white/10 bg-white/[0.04] text-slate-400 hover:bg-white/[0.08]'
            }`}
          >
            {geminiConfigured ? 'Gemini configured' : 'Configure Gemini'}
          </button>

          <button
            onClick={onRefresh}
            disabled={loading || authenticated === false}
            className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-semibold text-cyan-200 transition hover:border-cyan-300/40 hover:bg-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Syncing...' : 'Refresh'}
          </button>

          {authenticated && (
            <button
              onClick={handleLogout}
              className="rounded-full border border-rose-300/20 bg-rose-300/10 px-4 py-2 text-xs font-semibold text-rose-200 transition hover:border-rose-300/40 hover:bg-rose-300/15"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </header>
  )
}