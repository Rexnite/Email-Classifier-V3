import EmailCard from './EmailCard.jsx'
import EmptyState from './EmptyState.jsx'

export default function EmailList({
  emails,
  loading,
  authenticated,
  error,
  onPatch,
  onReadFullBody,
  geminiConfigured,
  onRequestGeminiKey,
}) {
  if (!authenticated) {
    return <EmptyState title="Gmail not connected" message="Connect Gmail to stream unread mail into the AI triage dashboard." />
  }

  if (loading) {
    return <EmptyState title="Scanning inbox" message="Checking Gmail for unread messages and preparing the triage feed…" loading />
  }

  if (error) {
    return <EmptyState title="Inbox sync failed" message={error} variant="error" />
  }

  if (emails.length === 0) {
    return <EmptyState title="Inbox clear" message="No unread messages found in the current Gmail search window." />
  }

  return (
    <div className="space-y-3">
      {emails.map((email) => (
        <EmailCard
          key={email.id || `${email.subject}-${email.sender}`}
          email={email}
          onPatch={onPatch}
          onReadFullBody={onReadFullBody}
          geminiConfigured={geminiConfigured}
          onRequestGeminiKey={onRequestGeminiKey}
        />
      ))}
    </div>
  )
}
