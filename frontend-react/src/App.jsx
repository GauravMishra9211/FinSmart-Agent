import React from 'react'
import Chat from './components/Chat.jsx'

export default function App(){
  return (
    <div className="app">
      <header>
        <div>
          <div className="brand">🤖 FinSmart Agent</div>
          <div className="small">Personal Loan Assistant • Challenge II (BFSI)</div>
        </div>
        <div className="badges">
          <div className="badge">VisionCoders AI</div>
          <div className="badge">FinSmart</div>
        </div>
      </header>
      <Chat />
    </div>
  )
}
