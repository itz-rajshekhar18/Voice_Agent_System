import './TodoList.css'

interface Todo {
  id: string
  title: string
  done: boolean
  priority: 'low' | 'medium' | 'high'
  due?: string
  created: string
}

interface TodoListProps {
  todos: Todo[]
  onToggle: (id: string, done: boolean) => void
  onDelete: (id: string) => void
}

function TodoList({ todos, onToggle, onDelete }: TodoListProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return '#ef4444'
      case 'medium':
        return '#f59e0b'
      case 'low':
        return '#10b981'
      default:
        return '#6b7280'
    }
  }

  const pendingTodos = todos.filter(todo => !todo.done)
  const completedTodos = todos.filter(todo => todo.done)

  return (
    <div className="todo-list">
      <div className="todo-header">
        <h2>📝 Tasks</h2>
        <span className="todo-count">
          {pendingTodos.length} pending
        </span>
      </div>

      <div className="todo-content">
        {todos.length === 0 ? (
          <div className="empty-state">
            <p>No tasks yet!</p>
            <p className="empty-hint">Ask me to add a task</p>
          </div>
        ) : (
          <>
            {pendingTodos.length > 0 && (
              <div className="todo-section">
                <h3>Pending</h3>
                {pendingTodos.map(todo => (
                  <div key={todo.id} className="todo-item fade-in">
                    <input
                      type="checkbox"
                      checked={todo.done}
                      onChange={() => onToggle(todo.id, !todo.done)}
                      className="todo-checkbox"
                    />
                    <div className="todo-details">
                      <div className="todo-title">{todo.title}</div>
                      <div className="todo-meta">
                        <span
                          className="todo-priority"
                          style={{ color: getPriorityColor(todo.priority) }}
                        >
                          {todo.priority}
                        </span>
                        {todo.due && (
                          <span className="todo-due">📅 {todo.due}</span>
                        )}
                      </div>
                    </div>
                    <button
                      onClick={() => onDelete(todo.id)}
                      className="todo-delete"
                      title="Delete task"
                    >
                      🗑️
                    </button>
                  </div>
                ))}
              </div>
            )}

            {completedTodos.length > 0 && (
              <div className="todo-section">
                <h3>Completed</h3>
                {completedTodos.map(todo => (
                  <div key={todo.id} className="todo-item completed fade-in">
                    <input
                      type="checkbox"
                      checked={todo.done}
                      onChange={() => onToggle(todo.id, !todo.done)}
                      className="todo-checkbox"
                    />
                    <div className="todo-details">
                      <div className="todo-title">{todo.title}</div>
                    </div>
                    <button
                      onClick={() => onDelete(todo.id)}
                      className="todo-delete"
                      title="Delete task"
                    >
                      🗑️
                    </button>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default TodoList
