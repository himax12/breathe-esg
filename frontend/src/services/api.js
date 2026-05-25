const API_BASE = 'http://localhost:8000/api'

export async function getBatches() {
  const res = await fetch(`${API_BASE}/batches/`)
  return res.json()
}

export async function getBatch(id) {
  const res = await fetch(`${API_BASE}/batches/${id}/`)
  return res.json()
}

export async function getBatchRecords(id, status) {
  const url = status 
    ? `${API_BASE}/batches/${id}/records/?status=${status}`
    : `${API_BASE}/batches/${id}/records/`
  const res = await fetch(url)
  return res.json()
}

export async function uploadCSV(sourceType, file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/upload-${sourceType}/`, {
    method: 'POST',
    body: formData,
  })
  return res.json()
}

export async function approveRecord(id, performedBy = 'analyst', note = '') {
  const res = await fetch(`${API_BASE}/records/${id}/approve/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ performed_by: performedBy, note }),
  })
  return res.json()
}

export async function flagRecord(id, flagType, flagReason, performedBy = 'analyst') {
  const res = await fetch(`${API_BASE}/records/${id}/flag/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ flag_type: flagType, flag_reason: flagReason, performed_by: performedBy }),
  })
  return res.json()
}

export async function rejectRecord(id, performedBy = 'analyst', note = '') {
  const res = await fetch(`${API_BASE}/records/${id}/reject/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ performed_by: performedBy, note }),
  })
  return res.json()
}

export async function approveBatch(id, performedBy = 'analyst', note = '') {
  const res = await fetch(`${API_BASE}/batches/${id}/approve_batch/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ performed_by: performedBy, note }),
  })
  return res.json()
}