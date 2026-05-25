import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

console.log('[Login] Component rendering')

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  console.log('[Login] Rendered, email:', email, 'loading:', loading)

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log('[Login] Form submitted with email:', email)
    setError('')
    setLoading(true)
    try {
      console.log('[Login] Calling login API...')
      await login(email, password)
      console.log('[Login] Login successful, navigating to dashboard')
      navigate('/dashboard')
    } catch (err) {
      console.log('[Login] Login failed:', err.response?.data?.error)
      setError(err.response?.data?.error || 'Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="card auth-card">
        <h2>Welcome Back</h2>
        <p style={{ textAlign: 'center', color: '#64748b', marginBottom: '24px' }}>
          Sign in to manage your tasks
        </p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%' }}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <p style={{ marginTop: '20px' }}>
          Don't have an account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  )
}