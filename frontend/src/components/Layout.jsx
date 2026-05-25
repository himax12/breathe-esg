import { Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

console.log('[Layout] Component rendering')

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  console.log('[Layout] user:', user)

  const handleLogout = () => {
    console.log('[Layout] Logout clicked')
    logout()
    navigate('/login')
  }

  return (
    <div>
      <header>
        <h1>TaskFlow</h1>
        {user && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <span style={{ color: '#64748b', fontSize: '0.875rem' }}>
              {user.name}
            </span>
            <button onClick={handleLogout}>Logout</button>
          </div>
        )}
      </header>
      <main className="container">
        <Outlet />
      </main>
    </div>
  )
}