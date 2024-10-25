import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { StoreProvider } from './store.tsx'
import { GoogleOAuthProvider } from '@react-oauth/google'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <StoreProvider>
      <GoogleOAuthProvider clientId='686843709663-ll0afih2ugqt44lgv5oqucm67kjq0heq.apps.googleusercontent.com'>
        <App />
      </GoogleOAuthProvider>
    </StoreProvider>
  </React.StrictMode>,
)
