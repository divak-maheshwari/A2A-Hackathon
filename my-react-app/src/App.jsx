import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState('')
  const [jsonResponse, setJsonResponse] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/hello')
      .then((response) => response.json())
      .then((data) => {
        setJsonResponse(data)
        setMessage(data.message) // still show message for convenience
      })
      .catch(() => {
        setMessage('Backend not available')
        setJsonResponse({ error: 'Could not fetch backend response' })
      })
      
  }, [])

  return (
    <>
      
      
      <div className="card">
        
        <p>
          <strong>FastAPI says:</strong> {message}
        </p>
        <p>
          <strong>Full JSON response from FastAPI:</strong>
        </p>
        
      </div>
  
    </>
  )
}

export default App

