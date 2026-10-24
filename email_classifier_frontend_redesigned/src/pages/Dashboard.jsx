import { useEffect, useState, useCallback } from 'react'
import Sidebar from '../components/Sidebar.jsx'
import Header from '../components/Header.jsx'
import ConnectPanel from '../components/ConnectPanel.jsx'
import EmailList from '../components/EmailList.jsx'
import InsightPanel from '../components/InsightPanel.jsx'
import EmailDetailModal from '../components/EmailDetailModal.jsx'
import GeminiKeyModal from '../components/GeminiKeyModal.jsx'
import { useInboxPolling } from '../hooks/useInboxPolling.js'
import { fetchGeminiStatus } from '../lib/api.js'

export default function Dashboard() {
  const { authenticated, emails, lastSyncedAt, loading, error, refresh, patchEmail } = useInboxPolling()

  const [geminiConfigured, setGeminiConfigured] = useState(null)
  const [geminiModalOpen, setGeminiModalOpen] = useState(false)
  const [detailEmailId, setDetailEmailId] = useState(null)

  // Derived (not duplicated) from the live emails array so that once
  // EmailDetailModal patches full_body back in via onBodyLoaded, this
  // always reflects the latest state -- including on a later reopen of
  // the same email, instead of holding onto a stale snapshot.
  const detailEmail = detailEmailId
    ? emails.find((candidate) => candidate.id === detailEmailId) || null
    : null

  const loadGeminiStatus = useCallback(() => {
    fetchGeminiStatus()
      .then((status) => setGeminiConfigured(Boolean(status.configured)))
      .catch(() => setGeminiConfigured(false))
  }, [])

  useEffect(() => {
    loadGeminiStatus()
  }, [loadGeminiStatus])

  if (authenticated === false && !loading) {
    return <ConnectPanel />
  }

  return (
    <div className="min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.16),transparent_30%),radial-gradient(circle_at_80%_10%,rgba(139,92,246,0.18),transparent_30%),radial-gradient(circle_at_50%_100%,rgba(59,130,246,0.10),transparent_30%)]" />
      <div className="relative flex min-h-screen">
        <Sidebar authenticated={authenticated} emailCount={emails.length} />
        <div className="min-w-0 flex-1">
          <Header
            authenticated={authenticated}
            lastSyncedAt={lastSyncedAt}
            loading={loading}
            onRefresh={refresh}
            geminiConfigured={geminiConfigured}
            onOpenGeminiSettings={() => setGeminiModalOpen(true)}
          />

          <main className="grid gap-6 px-5 py-6 lg:px-8 xl:grid-cols-[minmax(0,1fr)_420px]">
            <section className="min-w-0 space-y-5">
              <div className="rounded-[2rem] border border-white/10 bg-white/[0.045] p-6 shadow-soft backdrop-blur-xl">
                <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-cyan-300/80">Live inbox feed</p>
                    <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white">Unread Gmail messages</h2>
                    <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">New mail detected while the app is running will appear here first, then flow into the AI classification pipeline.</p>
                  </div>
                  <div className="rounded-full border border-white/10 bg-slate-950/70 px-4 py-2 text-xs font-medium text-slate-400">
                    Polling every 30s
                  </div>
                </div>
              </div>

              <EmailList
                emails={emails}
                loading={loading}
                authenticated={authenticated}
                error={error}
                onPatch={patchEmail}
                onReadFullBody={(emailToOpen) => setDetailEmailId(emailToOpen.id)}
                geminiConfigured={geminiConfigured}
                onRequestGeminiKey={() => setGeminiModalOpen(true)}
              />
            </section>

            <InsightPanel emails={emails} />
          </main>
        </div>
      </div>

      {detailEmail && (
        <EmailDetailModal
          email={detailEmail}
          onClose={() => setDetailEmailId(null)}
          onBodyLoaded={(emailId, fullBody) => patchEmail(emailId, { full_body: fullBody })}
        />
      )}

      {geminiModalOpen && (
        <GeminiKeyModal
          onClose={() => setGeminiModalOpen(false)}
          onSaved={loadGeminiStatus}
        />
      )}
    </div>
  )
}
