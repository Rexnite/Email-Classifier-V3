import { useEffect, useRef, useState, useCallback } from 'react'
import { fetchAuthStatus, fetchUnreadEmails } from '../lib/api.js'

const POLL_INTERVAL_MS = 30000

export function useInboxPolling() {
  const [authenticated, setAuthenticated] = useState(null)
  const [emails, setEmails] = useState([])
  const [lastSyncedAt, setLastSyncedAt] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const intervalRef = useRef(null)

  const poll = useCallback(async () => {
    try {
      const status = await fetchAuthStatus()
      setAuthenticated(status.authenticated)

      if (status.authenticated) {
        const data = await fetchUnreadEmails()
        setEmails(data.emails || [])
        setLastSyncedAt(new Date())
      }
      setError(null)
    } catch (err) {
      if (err.code === 'UNAUTHENTICATED') {
        setAuthenticated(false)
      } else {
        setError(err.message)
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    poll()
    intervalRef.current = setInterval(poll, POLL_INTERVAL_MS)
    return () => clearInterval(intervalRef.current)
  }, [poll])

  return { authenticated, emails, lastSyncedAt, loading, error, refresh: poll }
}
