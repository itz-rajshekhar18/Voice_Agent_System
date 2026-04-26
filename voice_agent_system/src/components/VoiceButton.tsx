import './VoiceButton.css'

interface VoiceButtonProps {
  isListening: boolean
  onClick: () => void
}

function VoiceButton({ isListening, onClick }: VoiceButtonProps) {
  return (
    <button
      className={`voice-button ${isListening ? 'listening' : ''}`}
      onClick={onClick}
      title={isListening ? 'Stop listening' : 'Start voice input'}
    >
      <div className="voice-icon">
        {isListening ? (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="4" width="4" height="16" rx="1" />
            <rect x="14" y="4" width="4" height="16" rx="1" />
          </svg>
        ) : (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
          </svg>
        )}
      </div>
      <span className="voice-text">
        {isListening ? 'Listening...' : 'Press to speak'}
      </span>
      {isListening && (
        <div className="pulse-rings">
          <div className="pulse-ring"></div>
          <div className="pulse-ring"></div>
          <div className="pulse-ring"></div>
        </div>
      )}
    </button>
  )
}

export default VoiceButton
