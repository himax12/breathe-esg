import { createContext, useState, useEffect, useContext } from 'react'
import axios from 'axios'

console.log('[AuthContext] Module loaded')

const AuthContext = createContext()

export function AuthProvider({ children }) {
  console.log('[AuthContext] AuthProvider rendering')
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    console.log('[AuthContext] useEffect triggered')
    const token = localStorage.getItem('token')
    console.log('[AuthContext] Token found:', !!token)
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      axios.get('/api/v1/auth/me')
        .then(res => {
          console.log('[AuthContext] /me success:', res.data.data.user)
          setUser(res.data.data.user)
        })
        .catch(err => {
          console.log('[AuthContext] /me failed:', err.response?.data?.error || err.message)
          localStorage.removeItem('token')
        })
        .finally(() => {
          console.log('[AuthContext] Loading complete')
          setLoading(false)
        })
    } else {
      console.log('[AuthContext] No token, setting loading to false')
      setLoading(false)
    }
  }, [])

  const login = async (email, password) => {
    console.log('[AuthContext] login called with email:', email)
    const res = await axios.post('/api/v1/auth/login', { email, password })
    console.log('[AuthContext] login response:', res.data)
    const { token, user: userData } = res.data.data
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    setUser(userData)
    console.log('[AuthContext] User set:', userData)
    return res.data
  }

  const register = async (name, email, password) => {
    console.log('[AuthContext] register called with name:', name, 'email:', email)
    const res = await axios.post('/api/v1/auth/register', { name, email, password })
    console.log('[AuthContext] register response:', res.data)
    const { token, user: userData } = res.data.data
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    setUser(userData)
    console.log('[AuthContext] User set:', userData)
    return res.data
  }

  const logout = () => {
    console.log('[AuthContext] logout called')
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
    console.log('[AuthContext] User cleared')
  }

  console.log('[AuthContext] Provider render, user:', user, 'loading:', loading)

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}