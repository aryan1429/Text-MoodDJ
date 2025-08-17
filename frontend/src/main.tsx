import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// Filter out noise from browser extensions in development
const isDevelopment = import.meta.env.DEV;
if (isDevelopment) {
  const originalError = console.error;
  console.error = (...args) => {
    // Suppress common extension-related errors
    const message = args[0]?.toString() || '';
    if (
      message.includes('enable_copy') ||
      message.includes('content-all') ||
      message.includes('Tabs cannot be edited') ||
      message.includes('E.C.P is not enabled')
    ) {
      return; // Suppress these extension errors
    }
    originalError.apply(console, args);
  };
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
