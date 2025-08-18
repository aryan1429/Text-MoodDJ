import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// Filter out noise from browser extensions and development warnings
const isDevelopment = import.meta.env.DEV;
if (isDevelopment) {
  // Add development-friendly CSP to allow blob URLs and reduce CSP violations
  const meta = document.createElement('meta');
  meta.httpEquiv = 'Content-Security-Policy';
  meta.content = "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: data: *; object-src 'none';";
  document.head.appendChild(meta);

  const originalError = console.error;
  const originalWarn = console.warn;
  
  console.error = (...args) => {
    // Suppress common extension-related errors and CSP warnings
    const message = args[0]?.toString() || '';
    if (
      message.includes('enable_copy') ||
      message.includes('content-all') ||
      message.includes('Tabs cannot be edited') ||
      message.includes('E.C.P is not enabled') ||
      message.includes('Content Security Policy') ||
      message.includes('blob:https://www.youtube.com') ||
      message.includes('blob:<URL>') ||
      message.includes('[Report Only]') ||
      message.includes('script-src') ||
      message.includes('script-src-elem') ||
      message.includes('Refused to load the script') ||
      message.includes('violates the following Content Security Policy')
    ) {
      return; // Suppress these extension and CSP errors
    }
    originalError.apply(console, args);
  };

  console.warn = (...args) => {
    const message = args[0]?.toString() || '';
    if (
      message.includes('Download the React DevTools') ||
      message.includes('react-dom_client.js') ||
      message.includes('React DevTools') ||
      message.includes('better development experience')
    ) {
      return; // Suppress React DevTools warning
    }
    originalWarn.apply(console, args);
  };
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
