import React, { useEffect, useState } from 'react'
import Message from './Message.jsx'

const DEFAULT_API = localStorage.getItem('FINSMART_API') || 'http://localhost:8000'

export default function Chat(){
  const [apiBase, setApiBase] = useState(DEFAULT_API)
  const [msgs, setMsgs] = useState([])
  const [stage, setStage] = useState('greet')

  const push = (who, text, html=false) => setMsgs(m => [...m, {who, text, html}])

  useEffect(()=>{ greet() }, [])

  const greet = () => {
    setMsgs([])
    push('bot', "Hello! 👋 I'm your FinSmart Agent. I can help you get a personal loan approval in minutes.")
    push('bot', `Type <span class='kbd'>start</span> to begin or <span class='kbd'>api</span> to set API URL (current: ${apiBase}).`, true)
    setStage('greet')
  }

  const ask = (text, s) => { push('bot', text); setStage(s) }

  const submitLoan = async (payload) => {
    push('bot', '<span class="typing"><span></span><span></span><span></span></span>', true)
    try{
      const res = await fetch(`${apiBase}/loan/submit`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      // remove typing
      setMsgs(m => m.slice(0, -1))

      if(data.stage === 'verify' && data.status === 'failed'){
        push('bot', "❌ KYC failed: " + (data.reason || 'Address mismatch.'))
        push('bot', "Type 'restart' to try again."); setStage('done'); return
      }
      if(data.stage === 'underwrite' && data.status === 'rejected'){
        const emi = data.emi ? ` (EMI ≈ ₹${data.emi.toFixed(2)})` : ''
        push('bot', "❌ Loan Rejected: " + data.reason + emi)
        push('bot', "Try a lower amount or longer tenure. Type 'restart'."); setStage('done'); return
      }
      if(data.stage === 'sanction' && data.status === 'approved'){
        const emi = data.emi ? `₹${data.emi.toFixed(2)}` : '-'
        const pdf = data.pdf_relative_path || ''
        const base = apiBase.replace(/\/$/, '')
        const link = pdf ? `<div class="small">📄 Sanction Letter: <a class="link" target="_blank" href="${base}/${pdf.startsWith('/')? pdf.slice(1): pdf}">Open PDF</a></div>` : ''
        push('bot', `✅ Approved!\nApproval ID: ${data.approval_id}\nEMI (approx): ${emi}\n${link}`, true)
        push('bot', "Type 'restart' to run another case."); setStage('done'); return
      }
      push('bot', "Unexpected response. Type 'restart'."); setStage('done')
    }catch(e){
      setMsgs(m => m.slice(0, -1))
      push('bot', "Server error. Make sure API is running at: " + apiBase)
      setStage('done')
    }
  }

  const onSubmit = (e) => {
    e.preventDefault()
    const text = e.target.message.value.trim()
    if(!text) return
    setMsgs(m => [...m, {who:'user', text}])
    e.target.message.value=''

    if(text.toLowerCase()==='restart'){ greet(); return }
    if(text.toLowerCase()==='api'){ push('bot', "Send the base API URL now. Example: http://localhost:8000"); setStage('set_api'); return }

    switch(stage){
      case 'greet':
        if(text.toLowerCase()==='start') ask("Great! Enter your registered 10-digit phone number.", 'ask_phone')
        else push('bot', "Please type 'start' to begin.")
        break;
      case 'set_api':
        setApiBase(text); localStorage.setItem('FINSMART_API', text)
        push('bot', "API set to: " + text); push('bot', "Type 'start' to begin."); setStage('greet')
        break;
      case 'ask_phone':
        if(/^\d{10}$/.test(text)){
          window._phone = text; ask("How much loan do you want? (INR) e.g., 200000", 'ask_amount')
        } else push('bot', "Please enter a valid 10-digit phone number.")
        break;
      case 'ask_amount':
        if(/^[0-9]{4,9}$/.test(text)){
          window._amount = Number(text); ask("What tenure do you prefer? (months 6–60) e.g., 24", 'ask_tenure')
        } else push('bot', "Enter a valid amount in INR (e.g., 200000).")
        break;
      case 'ask_tenure':
        const t = Number(text)
        if(Number.isInteger(t) && t>=6 && t<=60){
          window._tenure = t; ask("Please confirm your city/address keyword for KYC (e.g., Noida, Delhi).", 'ask_address')
        } else push('bot', "Enter tenure in months (6–60).")
        break;
      case 'ask_address':
        window._address = text; ask("What's your monthly net salary? (e.g., 65000)", 'ask_salary')
        break;
      case 'ask_salary':
        if(/^[0-9]{4,9}$/.test(text)){
          const salary = Number(text)
          submitLoan({
            phone: window._phone,
            amount: window._amount,
            tenure_months: window._tenure,
            address: window._address,
            salary
          })
        } else push('bot', "Enter valid monthly salary (e.g., 65000).")
        break;
      case 'done':
        push('bot', "Type 'restart' to begin again.")
        break;
      default:
        push('bot', "Type 'start' to begin.")
    }
  }

  return (
    <>
      <div id="chat">
        {msgs.map((m, i)=> <Message key={i} who={m.who} text={m.text} html={m.html} />)}
      </div>
      <footer>
        <form className="composer" onSubmit={onSubmit}>
          <input name="message" type="text" placeholder="Type here… (e.g., start)" autoComplete="off"/>
          <button type="submit">Send</button>
        </form>
      </footer>

      <div className="cfg">
        <div className="small">API Base URL</div>
        <input
          value={apiBase}
          onChange={(e)=>{setApiBase(e.target.value); localStorage.setItem('FINSMART_API', e.target.value)}}
          placeholder="http://localhost:8000"
        />
      </div>
    </>
  )
}
