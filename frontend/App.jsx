import React, { useState, useEffect, useRef } from 'react'
import { sendMessage, saveProfile } from './api'

export default function App(){
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [userId, setUserId] = useState(null)
  const bottomRef = useRef()

  useEffect(()=>{ bottomRef.current?.scrollIntoView({behavior:'smooth'}) },[messages])

  const handleSend = async () => {
    if(!input.trim()) return
    setMessages(m=>[...m, { role:'user', text: input }])
    setInput("")
    const res = await sendMessage(userId, input)
    setMessages(m=>[...m, { role:'bot', text: res.reply }])
  }

  const handleSaveProfile = async () => {
    const profile = { name:'Demo User', age:25, gender:'male', dietary_preferences:'vegetarian', fitness_goals:'weight loss' }
    const res = await saveProfile(profile)
    setUserId(res.user_id)
    setMessages(m=>[...m, { role:'bot', text:`Profile saved (id: ${res.user_id})`}])
  }

  return (
    <div style={{maxWidth:720, margin:'0 auto', padding:20}}>
      <h1>Personalized Health & Wellness Chatbot</h1>
      <div style={{border:'1px solid #ddd', borderRadius:8, padding:12, minHeight:300, maxHeight:600, overflowY:'auto'}}>
        {messages.map((m, i)=> (
          <div key={i} style={{textAlign: m.role==='user' ? 'right' : 'left', margin:'8px 0'}}>
            <div style={{display:'inline-block', padding:10, borderRadius:8, background: m.role==='user' ? '#eef' : '#f3f3f3'}}>{m.text}</div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div style={{display:'flex', marginTop:12}}>
        <input value={input} onChange={e=>setInput(e.target.value)} style={{flex:1, padding:10}} placeholder="Type your question..." />
        <button onClick={handleSend} style={{marginLeft:8, padding:'10px 16px'}}>Send</button>
      </div>
      <div style={{marginTop:12}}>
        <button onClick={handleSaveProfile}>Save Demo Profile</button>
      </div>
    </div>
  )
}
