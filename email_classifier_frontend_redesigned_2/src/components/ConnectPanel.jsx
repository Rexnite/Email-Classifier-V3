import { getLoginUrl } from '../lib/api.js'

export default function ConnectPanel() {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-950 px-6 text-white">
      <div className="absolute left-1/2 top-[-10%] h-96 w-96 -translate-x-1/2 rounded-full bg-cyan-400/20 blur-3xl" />
      <div className="absolute bottom-[-12%] right-[-8%] h-[32rem] w-[32rem] rounded-full bg-violet-500/20 blur-3xl" />
      <div className="absolute inset-0 bg-grid opacity-30" />

      <section className="relative z-10 w-full max-w-2xl rounded-[2rem] border border-white/10 bg-white/[0.06] p-8 shadow-2xl backdrop-blur-2xl sm:p-10">
        <div className="mx-auto mb-7 grid h-16 w-16 place-items-center rounded-3xl bg-gradient-to-br from-cyan-300 via-blue-500 to-violet-500 shadow-glow">
          <span className="text-2xl font-black">AI</span>
        </div>
        <p className="text-center text-xs font-semibold uppercase tracking-[0.32em] text-cyan-200/80">Read-only Gmail OAuth</p>
        <h1 className="mt-4 text-center text-4xl font-semibold tracking-tight sm:text-5xl">
          Gmail AI Classifier
        </h1>
        <p className="mx-auto mt-5 max-w-xl text-center text-base leading-7 text-slate-300">
          Intelligent inbox prioritization powered by local AI agents. Connect Gmail securely and let the app organize unread mail into Eisenhower priorities.
        </p>

        <div className="mt-8 flex justify-center">
          <button
            onClick={() => { window.location.href = getLoginUrl() }}
            className="group rounded-full bg-white px-7 py-3.5 text-sm font-bold text-slate-950 shadow-glow transition hover:scale-[1.03] hover:bg-cyan-50"
          >
            Connect Gmail Account
            <span className="ml-2 inline-block transition group-hover:translate-x-1">→</span>
          </button>
        </div>

        <div className="mt-8 grid gap-3 sm:grid-cols-3">
          {['No passwords stored', 'Read-only access', 'Local AI processing'].map((item) => (
            <div key={item} className="rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3 text-center text-xs text-slate-300">
              {item}
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
