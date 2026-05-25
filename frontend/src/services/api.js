const API_BASE = (import.meta.env.VITE_API_BASE || '/api').replace(/\/+$/, '')

async function requestJson(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options)
  let payload = null
  try {
    payload = await res.json()
  } catch {
    payload = null
  }

  if (!res.ok) {
    const message = payload?.error || payload?.detail || `Request failed (${res.status})`
    const error = new Error(message)
    error.status = res.status
    error.payload = payload
    throw error
  }

  return payload
}

export async function getBatches(page = 1) {
  return requestJson(`/batches/?page=${page}`)
}

export async function getBatch(id) {
  return requestJson(`/batches/${id}/`)
}

export async function getBatchRecords(id, status, page = 1) {
  const params = new URLSearchParams({ page: String(page) })
  if (status) params.set('status', status)
  return requestJson(`/batches/${id}/records/?${params.toString()}`)
}

export async function uploadCSV(sourceType, file) {
  const formData = new FormData()
  formData.append('file', file)
  return requestJson(`/upload/${sourceType}/`, {
    method: 'POST',
    body: formData,
  })
}

export async function approveRecord(id, performedBy = 'analyst', note = '') {
  return requestJson(`/records/${id}/approve/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ performed_by: performedBy, note }),
  })
}

export async function flagRecord(id, flagType, flagReason, performedBy = 'analyst') {
  return requestJson(`/records/${id}/flag/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ flag_type: flagType, flag_reason: flagReason, performed_by: performedBy }),
  })
}

export async function rejectRecord(id, performedBy = 'analyst', note = '') {
  return requestJson(`/records/${id}/reject/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ performed_by: performedBy, note }),
  })
}

export async function approveBatch(id, performedBy = 'analyst', note = '') {
  return requestJson(`/batches/${id}/approve-batch/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ performed_by: performedBy, note }),
  })
}
