function statusTone(status) {
  switch (status) {
    case 'valid':
      return 'border-emerald-300/20 bg-emerald-300/10 text-emerald-200'
    case 'corrected':
      return 'border-violet-300/20 bg-violet-300/10 text-violet-200'
    case 'needs_review':
      return 'border-amber-300/20 bg-amber-300/10 text-amber-200'
    case 'error':
      return 'border-rose-300/20 bg-rose-300/10 text-rose-200'
    default:
      return 'border-white/10 bg-white/[0.04] text-slate-300'
  }
}

function statusLabel(status) {
  switch (status) {
    case 'valid':
      return 'Validated'
    case 'corrected':
      return 'Corrected by Gemini'
    case 'needs_review':
      return 'Needs review'
    case 'error':
      return 'Validation unavailable'
    default:
      return 'Validation'
  }
}

export default function ValidationBadge({ result }) {
  if (!result) return null

  let status = 'error'

  if (result.corrected_by_validator) {
    status = 'corrected'
  } else if (result.validator_used) {
    status = result.valid ? 'valid' : 'needs_review'
  }

  return (
    <div className={`mt-3 rounded-2xl border px-3 py-2 text-xs ${statusTone(status)}`}>
      <p className="font-semibold">{statusLabel(status)}</p>

      {!result.validator_used && result.validation_error && (
        <p className="mt-1 text-[11px] opacity-80">{result.validation_error}</p>
      )}

      {result.validator_used && result.reason && (
        <p className="mt-1 text-[11px] leading-5 opacity-90">{result.reason}</p>
      )}

      {result.validator_used && !result.valid && result.suggested && (
        <p className="mt-1 text-[11px] opacity-90">
          Suggested: {result.suggested.classification} (confidence: {result.confidence})
        </p>
      )}
    </div>
  )
}
