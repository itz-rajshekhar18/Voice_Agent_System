// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Voice Configuration
export const VOICE_CONFIG = {
  language: 'en-US',
  speechRate: 0.9,
  speechPitch: 1,
  speechVolume: 1,
}

// App Configuration
export const APP_CONFIG = {
  maxMessageHistory: 50,
  autoSaveInterval: 5000, // ms
}
