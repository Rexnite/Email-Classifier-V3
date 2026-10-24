const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export function getLoginUrl() {
  return `${API_BASE}/auth/login`
}

export function getCsvExportUrl() {
  return `${API_BASE}/emails/export/csv`
}

export function getMarkdownExportUrl() {
  return `${API_BASE}/emails/export/md`
}

export async function fetchAuthStatus() {
  const res = await fetch(`${API_BASE}/auth/status`)

  if (!res.ok) {
    throw new Error('Failed to fetch auth status')
  }

  return res.json()
}

export async function fetchUnreadEmails() {
  const res = await fetch(`${API_BASE}/emails/fetch`)

  if (!res.ok) {
    if (res.status === 401) {
      const err = new Error('Not authenticated')
      err.code = 'UNAUTHENTICATED'
      throw err
    }

    throw new Error('Failed to fetch emails')
  }

  return res.json()
}

export async function logout() {
  const res = await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
  })

  if (!res.ok) {
    throw new Error('Failed to logout')
  }

  return res.json()
}

export async function fetchEmailBody(messageId) {
  const res = await fetch(`${API_BASE}/emails/${messageId}/body`)

  if (!res.ok) {
    if (res.status === 401) {
      const err = new Error('Not authenticated')
      err.code = 'UNAUTHENTICATED'
      throw err
    }

    throw new Error('Failed to fetch full email body')
  }

  return res.json()
}

export async function summarizeEmail(messageId, force = false) {
  const res = await fetch(
    `${API_BASE}/emails/${messageId}/summarize?force=${force ? 'true' : 'false'}`,
    { method: 'POST' },
  )

  if (!res.ok) {
    throw new Error('Failed to summarize email')
  }

  return res.json()
}

export async function validateEmail(messageId) {
  const res = await fetch(`${API_BASE}/emails/${messageId}/validate`, {
    method: 'POST',
  })

  if (!res.ok) {
    throw new Error('Failed to validate email')
  }

  return res.json()
}

export async function fetchGeminiStatus() {
  const res = await fetch(`${API_BASE}/settings/gemini/status`)

  if (!res.ok) {
    throw new Error('Failed to fetch Gemini status')
  }

  return res.json()
}

export async function saveGeminiKey(apiKey) {
  const res = await fetch(`${API_BASE}/settings/gemini/key`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: apiKey }),
  })

  if (!res.ok) {
    throw new Error('Failed to save Gemini API key')
  }

  return res.json()
}

export async function deleteGeminiKey() {
  const res = await fetch(`${API_BASE}/settings/gemini/key`, {
    method: 'DELETE',
  })

  if (!res.ok) {
    throw new Error('Failed to delete Gemini API key')
  }

  return res.json()
}