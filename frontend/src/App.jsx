import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ImportList from './pages/ImportList'
import BatchDetail from './pages/BatchDetail'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ImportList />} />
        <Route path="/batches/:id" element={<BatchDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App