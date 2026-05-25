import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getBatches, uploadCSV } from '../services/api'

const SOURCE_TYPES = {
  SAP_FUEL: 'SAP Fuel',
  SAP_PROCUREMENT: 'SAP Procurement',
  UTILITY_ELECTRICITY: 'Utility Electricity',
  CORPORATE_TRAVEL: 'Corporate Travel',
}

const STATUS_COLORS = {
  UPLOADING: '#6b7280',
  VALIDATING: '#f59e0b',
  IMPORTED: '#3b82f6',
  REVIEW_IN_PROGRESS: '#8b5cf6',
  COMPLETED: '#10b981',
}

export default function ImportList() {
  const [batches, setBatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [uploadSource, setUploadSource] = useState('sap-fuel')
  const [file, setFile] = useState(null)
  const navigate = useNavigate()

  const fetchBatches = async () => {
    try {
      const data = await getBatches()
      setBatches(data.results || [])
    } catch (err) {
      console.error('Failed to fetch batches:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBatches()
  }, [])

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) return
    setUploading(true)
    try {
      await uploadCSV(uploadSource, file)
      setFile(null)
      fetchBatches()
    } catch (err) {
      console.error('Upload failed:', err)
    } finally {
      setUploading(false)
    }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '4px' }}>Breathe ESG</h1>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Emissions Data Review Dashboard</p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <select 
            value={uploadSource} 
            onChange={e => setUploadSource(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid #e2e8f0' }}
          >
            <option value="sap-fuel">SAP Fuel</option>
            <option value="sap-procurement">SAP Procurement</option>
            <option value="utility-electricity">Utility Electricity</option>
            <option value="corporate-travel">Corporate Travel</option>
          </select>
          <form onSubmit={handleUpload} style={{ display: 'flex', gap: '8px' }}>
            <input 
              type="file" 
              accept=".csv"
              onChange={e => setFile(e.target.files[0])}
              style={{ padding: '8px', border: '1px solid #e2e8f0', borderRadius: '6px' }}
            />
            <button 
              type="submit" 
              disabled={!file || uploading}
              style={{
                padding: '8px 16px',
                background: uploading ? '#9ca3af' : '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: uploading ? 'not-allowed' : 'pointer'
              }}
            >
              {uploading ? 'Uploading...' : 'Upload CSV'}
            </button>
          </form>
        </div>
      </header>

      <div style={{ background: 'white', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0' }}>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Source</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>File</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Rows</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Succeeded</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Failed</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Scope 1 (kg)</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Scope 2 (kg)</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Scope 3 (kg)</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Status</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: '0.75rem', fontWeight: '500', color: '#64748b', textTransform: 'uppercase' }}>Date</th>
            </tr>
          </thead>
          <tbody>
            {batches.length === 0 ? (
              <tr>
                <td colSpan="10" style={{ padding: '48px', textAlign: 'center', color: '#64748b' }}>
                  No imports yet. Upload a CSV to get started.
                </td>
              </tr>
            ) : batches.map(batch => (
              <tr 
                key={batch.id} 
                onClick={() => navigate(`/batches/${batch.id}`)}
                style={{ cursor: 'pointer', borderBottom: '1px solid #f1f5f9' }}
              >
                <td style={{ padding: '16px', fontSize: '0.875rem' }}>
                  <span style={{ 
                    background: '#eff6ff', 
                    color: '#1d4ed8', 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    fontSize: '0.75rem',
                    fontWeight: '500'
                  }}>
                    {SOURCE_TYPES[batch.source_type] || batch.source_type}
                  </span>
                </td>
                <td style={{ padding: '16px', fontSize: '0.875rem', color: '#1e293b' }}>{batch.file_name}</td>
                <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.875rem' }}>{batch.rows_total}</td>
                <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.875rem', color: '#10b981' }}>{batch.rows_succeeded}</td>
                <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.875rem', color: batch.rows_failed > 0 ? '#ef4444' : '#64748b' }}>{batch.rows_failed}</td>
                <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.875rem' }}>{batch.total_kgCO2_scope1 || '—'}</td>
                <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.875rem' }}>{batch.total_kgCO2_scope2_location || '—'}</td>
                <td style={{ padding: '16px', textAlign: 'center', fontSize: '0.875rem' }}>{batch.total_kgCO2_scope3 || '—'}</td>
                <td style={{ padding: '16px', textAlign: 'center' }}>
                  <span style={{ 
                    background: STATUS_COLORS[batch.status] + '20',
                    color: STATUS_COLORS[batch.status],
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '0.75rem',
                    fontWeight: '500'
                  }}>
                    {batch.status.replace('_', ' ')}
                  </span>
                </td>
                <td style={{ padding: '16px', fontSize: '0.75rem', color: '#64748b' }}>
                  {new Date(batch.imported_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}