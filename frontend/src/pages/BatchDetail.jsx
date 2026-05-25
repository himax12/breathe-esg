import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getBatch, getBatchRecords, approveRecord, flagRecord, rejectRecord, approveBatch } from '../services/api'

const STATUS_CONFIG = {
  PENDING: { label: 'Pending', color: '#f59e0b', bg: '#fef3c7' },
  APPROVED: { label: 'Approved', color: '#10b981', bg: '#d1fae5' },
  FLAGGED: { label: 'Flagged', color: '#ef4444', bg: '#fee2e2' },
  REJECTED: { label: 'Rejected', color: '#6b7280', bg: '#f3f4f6' },
}

const FLAG_TYPE_CONFIG = {
  MISSING_FIELD: 'Missing Field',
  VALUE_OUT_OF_RANGE: 'Out of Range',
  OTHER: 'Other',
}

export default function BatchDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [batch, setBatch] = useState(null)
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const [showFlagModal, setShowFlagModal] = useState(false)
  const [flaggingRecord, setFlaggingRecord] = useState(null)
  const [flagReason, setFlagReason] = useState('')
  const [flagType, setFlagType] = useState('OTHER')
  const [actionLoading, setActionLoading] = useState(false)

  const fetchData = async () => {
    try {
      const [batchData, recordsData] = await Promise.all([
        getBatch(id),
        getBatchRecords(id, statusFilter)
      ])
      setBatch(batchData)
      setRecords(Array.isArray(recordsData) ? recordsData : recordsData.results || [])
    } catch (err) {
      console.error('Failed to fetch:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [id, statusFilter])

  const handleApproveRecord = async (recordId) => {
    setActionLoading(true)
    try {
      await approveRecord(recordId)
      fetchData()
    } catch (err) {
      console.error('Failed to approve:', err)
    } finally {
      setActionLoading(false)
    }
  }

  const handleRejectRecord = async (recordId) => {
    setActionLoading(true)
    try {
      await rejectRecord(recordId)
      fetchData()
    } catch (err) {
      console.error('Failed to reject:', err)
    } finally {
      setActionLoading(false)
    }
  }

  const handleFlagClick = (record) => {
    setFlaggingRecord(record)
    setFlagReason('')
    setFlagType('OTHER')
    setShowFlagModal(true)
  }

  const handleFlagSubmit = async () => {
    if (!flaggingRecord) return
    setActionLoading(true)
    try {
      await flagRecord(flaggingRecord.id, flagType, flagReason)
      setShowFlagModal(false)
      fetchData()
    } catch (err) {
      console.error('Failed to flag:', err)
    } finally {
      setActionLoading(false)
    }
  }

  const handleApproveBatch = async () => {
    if (!confirm(`Approve all pending records in this batch?`)) return
    setActionLoading(true)
    try {
      await approveBatch(id)
      fetchData()
    } catch (err) {
      console.error('Failed to approve batch:', err)
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading...</div>
  if (!batch) return <div className="error">Batch not found</div>

  const pendingCount = records.filter(r => r.status === 'PENDING').length

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      <header style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <button 
            onClick={() => navigate('/')}
            style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', marginBottom: '8px', fontSize: '0.875rem' }}
          >
            ← Back to Imports
          </button>
          <h1 style={{ fontSize: '1.5rem', fontWeight: '600' }}>{batch.file_name}</h1>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
            {batch.source_type} • {batch.rows_total} total rows
          </p>
        </div>
        {pendingCount > 0 && (
          <button
            onClick={handleApproveBatch}
            disabled={actionLoading}
            style={{
              padding: '10px 20px',
              background: '#10b981',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: actionLoading ? 'not-allowed' : 'pointer',
              fontSize: '0.875rem',
              fontWeight: '500'
            }}
          >
            {actionLoading ? 'Processing...' : `Approve All Pending (${pendingCount})`}
          </button>
        )}
      </header>

      {/* Stats Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ fontSize: '2rem', fontWeight: '600', color: '#1e293b' }}>{records.length}</div>
          <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Total Records</div>
        </div>
        <div style={{ background: '#fef3c7', padding: '20px', borderRadius: '12px' }}>
          <div style={{ fontSize: '2rem', fontWeight: '600', color: '#f59e0b' }}>{records.filter(r => r.status === 'PENDING').length}</div>
          <div style={{ color: '#92400e', fontSize: '0.875rem' }}>Pending</div>
        </div>
        <div style={{ background: '#fee2e2', padding: '20px', borderRadius: '12px' }}>
          <div style={{ fontSize: '2rem', fontWeight: '600', color: '#ef4444' }}>{records.filter(r => r.status === 'FLAGGED').length}</div>
          <div style={{ color: '#991b1b', fontSize: '0.875rem' }}>Flagged</div>
        </div>
        <div style={{ background: '#d1fae5', padding: '20px', borderRadius: '12px' }}>
          <div style={{ fontSize: '2rem', fontWeight: '600', color: '#10b981' }}>{records.filter(r => r.status === 'APPROVED').length}</div>
          <div style={{ color: '#065f46', fontSize: '0.875rem' }}>Approved</div>
        </div>
      </div>

      {/* Filters */}
      <div style={{ marginBottom: '16px', display: 'flex', gap: '8px' }}>
        {['', 'PENDING', 'FLAGGED', 'APPROVED', 'REJECTED'].map(filter => (
          <button
            key={filter || 'ALL'}
            onClick={() => setStatusFilter(filter)}
            style={{
              padding: '6px 12px',
              background: statusFilter === filter ? '#3b82f6' : 'white',
              color: statusFilter === filter ? 'white' : '#64748b',
              border: '1px solid #e2e8f0',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '0.75rem',
              fontWeight: '500'
            }}
          >
            {filter || 'ALL'}
          </button>
        ))}
      </div>

      {/* Records Table */}
      <div style={{ background: 'white', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0' }}>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Location</th>
              <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Raw Value</th>
              <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>kg CO2e</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Scope</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Status</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Flag</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {records.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ padding: '48px', textAlign: 'center', color: '#64748b' }}>
                  No records found.
                </td>
              </tr>
            ) : records.map(record => {
              const status = STATUS_CONFIG[record.status] || STATUS_CONFIG.PENDING
              return (
                <tr key={record.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '16px', fontSize: '0.875rem' }}>
                    <div style={{ fontWeight: '500', color: '#1e293b' }}>{record.source_location_code || '—'}</div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{record.source_location_type}</div>
                  </td>
                  <td style={{ padding: '16px', textAlign: 'right', fontSize: '0.875rem' }}>
                    {record.raw_value} {record.raw_unit}
                  </td>
                  <td style={{ padding: '16px', textAlign: 'right', fontSize: '0.875rem', fontWeight: '500' }}>
                    {record.normalized_value ? record.normalized_value.toFixed(2) : '—'}
                  </td>
                  <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.75rem' }}>
                    <span style={{ 
                      background: '#f1f5f9', 
                      color: '#475569', 
                      padding: '4px 8px', 
                      borderRadius: '4px',
                      fontFamily: 'monospace'
                    }}>
                      {record.scope || '—'}
                    </span>
                  </td>
                  <td style={{ padding: '16px', textAlign: 'center' }}>
                    <span style={{ 
                      background: status.bg,
                      color: status.color,
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: '500'
                    }}>
                      {status.label}
                    </span>
                  </td>
                  <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.75rem' }}>
                    {record.flag_type ? (
                      <span style={{ color: '#ef4444' }} title={record.flag_reason}>
                        {FLAG_TYPE_CONFIG[record.flag_type] || record.flag_type}
                      </span>
                    ) : '—'}
                  </td>
                  <td style={{ padding: '16px', textAlign: 'center' }}>
                    <div style={{ display: 'flex', gap: '4px', justifyContent: 'center' }}>
                      {record.status === 'PENDING' && (
                        <>
                          <button 
                            onClick={() => handleApproveRecord(record.id)}
                            disabled={actionLoading}
                            style={{ padding: '4px 8px', background: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            Approve
                          </button>
                          <button 
                            onClick={() => handleFlagClick(record)}
                            disabled={actionLoading}
                            style={{ padding: '4px 8px', background: '#f59e0b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            Flag
                          </button>
                          <button 
                            onClick={() => handleRejectRecord(record.id)}
                            disabled={actionLoading}
                            style={{ padding: '4px 8px', background: '#6b7280', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            Reject
                          </button>
                        </>
                      )}
                      {record.status === 'FLAGGED' && (
                        <button 
                          onClick={() => handleApproveRecord(record.id)}
                          disabled={actionLoading}
                          style={{ padding: '4px 8px', background: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' }}
                        >
                          Approve
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Flag Modal */}
      {showFlagModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <div style={{ background: 'white', padding: '24px', borderRadius: '12px', width: '400px' }}>
            <h3 style={{ marginBottom: '16px', fontSize: '1.125rem', fontWeight: '600' }}>Flag Record</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', color: '#64748b' }}>Flag Type</label>
              <select 
                value={flagType}
                onChange={e => setFlagType(e.target.value)}
                style={{ width: '100%', padding: '8px', border: '1px solid #e2e8f0', borderRadius: '6px' }}
              >
                <option value="MISSING_FIELD">Missing Field</option>
                <option value="VALUE_OUT_OF_RANGE">Value Out of Range</option>
                <option value="OTHER">Other</option>
              </select>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', color: '#64748b' }}>Reason</label>
              <textarea
                value={flagReason}
                onChange={e => setFlagReason(e.target.value)}
                placeholder="Explain why this record is flagged..."
                rows={3}
                style={{ width: '100%', padding: '8px', border: '1px solid #e2e8f0', borderRadius: '6px' }}
              />
            </div>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <button 
                onClick={() => setShowFlagModal(false)}
                style={{ padding: '8px 16px', background: '#f1f5f9', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
              >
                Cancel
              </button>
              <button 
                onClick={handleFlagSubmit}
                disabled={actionLoading}
                style={{ padding: '8px 16px', background: '#ef4444', color: 'white', border: 'none', borderRadius: '6px', cursor: actionLoading ? 'not-allowed' : 'pointer' }}
              >
                {actionLoading ? 'Submitting...' : 'Submit Flag'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}