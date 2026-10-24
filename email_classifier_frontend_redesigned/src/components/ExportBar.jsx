import {
  getCsvExportUrl,
  getMarkdownExportUrl,
} from '../lib/api.js'

export default function ExportBar() {
  const handleCsvExport = () => {
    window.open(getCsvExportUrl(), '_blank')
  }

  const handleMarkdownExport = () => {
    window.open(getMarkdownExportUrl(), '_blank')
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <button
        onClick={handleCsvExport}
        className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-semibold text-cyan-200 transition hover:border-cyan-300/40 hover:bg-cyan-300/15"
      >
        CSV Export
      </button>

      <button
        onClick={handleMarkdownExport}
        className="rounded-full border border-violet-300/20 bg-violet-300/10 px-4 py-2 text-xs font-semibold text-violet-200 transition hover:border-violet-300/40 hover:bg-violet-300/15"
      >
        Markdown Digest
      </button>

      <button
        disabled
        title="Coming soon"
        className="cursor-not-allowed rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs font-semibold text-slate-500 transition"
      >
        HTML Report
        <span className="ml-2 text-[10px] uppercase tracking-wider text-slate-600">
          soon
        </span>
      </button>
    </div>
  )
}