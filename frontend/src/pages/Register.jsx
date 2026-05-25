import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

console.log('[Register] Component rendering')

export default function Register() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  console.log('[Register] Rendered, name:', name, 'email:', email, 'loading:', loading)

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log('[Register] Form submitted with name:', name, 'email:', email)
    setError('')
    if (password !== confirmPassword) {
      console.log('[Register] Passwords do not match')
      setError('Passwords do not match')
      return
    }
    if (password.length < 6) {
      console.log('[Register] Password too short')
      setError('Password must be at least 6 characters')
      return
    }
    setLoading(true)
    try {
      console.log('[Register] Calling register API...')
      await register(name, email, password)
      console.log('[Register] Registration successful, navigating to dashboard')
      navigate('/dashboard')
    } catch (err) {
      console.log('[Register] Registration failed:', err.response?.data?.error)
      setError(err.response?.data?.error || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="card auth-card">
        <h2>Create Account</h2>
        <p style={{ textAlign: 'center', color: '#64748b', marginBottom: '24px' }}>
          Join us to start managing your tasks
        </p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="John Doe"
              required
            />
          </div>
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
              placeholder="Min. 6 characters"
              required
              minLength={6}
            />
          </div>
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              placeholder="Re-enter your password"
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%' }}>
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        <p style={{ marginTop: '20px' }}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  )
}