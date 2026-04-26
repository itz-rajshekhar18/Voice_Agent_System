import { useState, useEffect, useRef } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'
import TodoList from './components/TodoList'
import MemoryPanel from './components/MemoryPanel'
import VoiceButton from './components/VoiceButton'
import { API_BASE_URL, VOICE_CONFIG } from './config'

export interface Todo {
  id: string
  title: string
  done: boolean
  priority: 'low' | 'medium' | 'high'
  due?: string
  created: string
}

export interface Memory {
  [key: string]: string
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [todos, setTodos] = useState<Todo[]>([])
  const [memories, setMemories] = useState<Memory>({})
  const [isLoading, setIsLoading] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const recognitionRef = useRef<any>(null)

  // Fetch initial data
  useEffect(() => {
    fetchTodos()
    fetchMemories()
  }, [])

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = VOICE_CONFIG.language

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript
        handleSendMessage(transcript)
        setIsListening(false)
      }

      recognitionRef.current.onerror = () => {
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }
  }, [])

  const fetchTodos = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/todos`)
      const data = await response.json()
      setTodos(data.todos || [])
    } catch (error) {
      console.error('Failed to fetch todos:', error)
    }
  }

  const fetchMemories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/memories`)
      const data = await response.json()
      setMemories(data.memories || {})
    } catch (error) {
      console.error('Failed to fetch memories:', error)
    }
  }

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: text,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text })
      })

      const data = await response.json()

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
      setTodos(data.todos || [])
      setMemories(data.memories || {})

      // Speak the response
      speakText(data.response)
    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = VOICE_CONFIG.speechRate
      utterance.pitch = VOICE_CONFIG.speechPitch
      utterance.volume = VOICE_CONFIG.speechVolume
      window.speechSynthesis.speak(utterance)
    }
  }

  const handleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser.')
      return
    }

    if (isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    } else {
      recognitionRef.current.start()
      setIsListening(true)
    }
  }

  const handleToggleTodo = async (id: string, done: boolean) => {
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ done })
      })

      if (response.ok) {
        fetchTodos()
      }
    } catch (error) {
      console.error('Failed to toggle todo:', error)
    }
  }

  const handleDeleteTodo = async (id: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        fetchTodos()
      }
    } catch (error) {
      console.error('Failed to delete todo:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 Voice AI Assistant</h1>
        <p>Powered by Claude</p>
      </header>

      <div className="app-container">
        <div className="main-panel">
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
          />
          <VoiceButton
            isListening={isListening}
            onClick={handleVoiceInput}
          />
        </div>

        <div className="side-panel">
          <TodoList
            todos={todos}
            onToggle={handleToggleTodo}
            onDelete={handleDeleteTodo}
          />
          <MemoryPanel memories={memories} />
        </div>
      </div>
    </div>
  )
}

export default App
