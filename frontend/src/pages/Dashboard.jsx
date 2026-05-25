import { useState, useEffect } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

console.log('[Dashboard] Component rendering')

export default function Dashboard() {
  const { user } = useAuth()
  const [tasks, setTasks] = useState([])
  const [message, setMessage] = useState({ type: '', text: '' })
  const [form, setForm] = useState({ title: '', description: '', priority: 'medium', status: 'pending' })
  const [editingId, setEditingId] = useState(null)

  console.log('[Dashboard] Rendered, user:', user)
  console.log('[Dashboard] tasks:', tasks, 'message:', message)

  const fetchTasks = async () => {
    console.log('[Dashboard] Fetching tasks...')
    try {
      const res = await axios.get('/api/v1/tasks')
      console.log('[Dashboard] Tasks fetched:', res.data.data)
      setTasks(res.data.data)
    } catch (err) {
      console.log('[Dashboard] Failed to fetch tasks:', err.response?.data?.error || err.message)
      showMessage('error', 'Failed to load tasks')
    }
  }

  useEffect(() => {
    console.log('[Dashboard] useEffect triggered, calling fetchTasks')
    fetchTasks()
  }, [])

  const showMessage = (type, text) => {
    console.log('[Dashboard] showMessage called:', type, text)
    setMessage({ type, text })
    setTimeout(() => {
      console.log('[Dashboard] Clearing message')
      setMessage({ type: '', text: '' })
    }, 4000)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log('[Dashboard] Form submitted, form:', form, 'editingId:', editingId)
    try {
      if (editingId) {
        console.log('[Dashboard] Updating task:', editingId)
        await axios.put(`/api/v1/tasks/${editingId}`, form)
        showMessage('success', 'Task updated successfully!')
        setEditingId(null)
      } else {
        console.log('[Dashboard] Creating task')
        await axios.post('/api/v1/tasks', form)
        showMessage('success', 'Task created successfully!')
      }
      setForm({ title: '', description: '', priority: 'medium', status: 'pending' })
      fetchTasks()
    } catch (err) {
      console.log('[Dashboard] Operation failed:', err.response?.data?.error)
      showMessage('error', err.response?.data?.error || 'Operation failed')
    }
  }

  const handleEdit = (task) => {
    console.log('[Dashboard] Edit clicked for task:', task)
    setForm({ title: task.title, description: task.description || '', priority: task.priority, status: task.status })
    setEditingId(task._id)
  }

  const handleDelete = async (id) => {
    console.log('[Dashboard] Delete clicked for id:', id)
    if (!confirm('Are you sure you want to delete this task?')) return
    try {
      await axios.delete(`/api/v1/tasks/${id}`)
      console.log('[Dashboard] Task deleted successfully')
      showMessage('success', 'Task deleted successfully!')
      fetchTasks()
    } catch (err) {
      console.log('[Dashboard] Delete failed:', err.response?.data?.error)
      showMessage('error', 'Failed to delete task')
    }
  }

  const cancelEdit = () => {
    console.log('[Dashboard] Cancel edit')
    setEditingId(null)
    setForm({ title: '', description: '', priority: 'medium', status: 'pending' })
  }

  const stats = {
    total: tasks.length,
    pending: tasks.filter(t => t.status === 'pending').length,
    completed: tasks.filter(t => t.status === 'completed').length
  }

  console.log('[Dashboard] Stats:', stats)

  return (
    <div>
      <div className="dashboard-header">
        <h2>Welcome, {user?.name}</h2>
      </div>

      {message.text && (
        <div className={message.type === 'error' ? 'error' : 'success'}>
          {message.text}
        </div>
      )}

      <div className="stats-row">
        <div className="stat-card">
          <div className="count">{stats.total}</div>
          <div className="label">Total Tasks</div>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
          <div className="count">{stats.pending}</div>
          <div className="label">Pending</div>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
          <div className="count">{stats.completed}</div>
          <div className="label">Completed</div>
        </div>
      </div>

      <div className="card">
        <h3>{editingId ? 'Edit Task' : 'Create New Task'}</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Title</label>
            <input
              value={form.title}
              onChange={e => setForm({ ...form, title: e.target.value })}
              placeholder="Enter task title"
              required
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={form.description}
              onChange={e => setForm({ ...form, description: e.target.value })}
              placeholder="Enter task description (optional)"
              rows={3}
            />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Priority</label>
              <select value={form.priority} onChange={e => setForm({ ...form, priority: e.target.value })}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="form-group">
              <label>Status</label>
              <select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="submit" className="btn-primary">
              {editingId ? 'Update Task' : 'Create Task'}
            </button>
            {editingId && (
              <button type="button" onClick={cancelEdit} className="btn-secondary">
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="card">
        <h3>Your Tasks ({tasks.length})</h3>
        {tasks.length === 0 ? (
          <div className="empty-state">
            <p>No tasks yet. Create your first task above!</p>
          </div>
        ) : tasks.map(task => (
          <div key={task._id} className="task-item">
            <div className="task-info">
              <h3>{task.title}</h3>
              {task.description && <p>{task.description}</p>}
              <div className="task-meta">
                <span className={`badge status-${task.status}`}>
                  {task.status.replace('_', ' ')}
                </span>
                <span className={`badge priority-${task.priority}`}>
                  {task.priority}
                </span>
              </div>
            </div>
            <div className="task-actions">
              <button onClick={() => handleEdit(task)} className="btn-secondary">Edit</button>
              <button onClick={() => handleDelete(task._id)} className="btn-danger">Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}