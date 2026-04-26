import './MemoryPanel.css'

interface Memory {
  [key: string]: string
}

interface MemoryPanelProps {
  memories: Memory
}

function MemoryPanel({ memories }: MemoryPanelProps) {
  const memoryEntries = Object.entries(memories)

  return (
    <div className="memory-panel">
      <div className="memory-header">
        <h2>🧠 Memories</h2>
        <span className="memory-count">
          {memoryEntries.length} stored
        </span>
      </div>

      <div className="memory-content">
        {memoryEntries.length === 0 ? (
          <div className="empty-state">
            <p>No memories yet!</p>
            <p className="empty-hint">I'll remember important things you tell me</p>
          </div>
        ) : (
          <div className="memory-list">
            {memoryEntries.map(([key, value]) => (
              <div key={key} className="memory-item fade-in">
                <div className="memory-key">{key}</div>
                <div className="memory-value">{value}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default MemoryPanel
