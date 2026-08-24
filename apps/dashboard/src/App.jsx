import React, { useState, useEffect, useRef } from 'react'
import { Shield, Activity, Volume2, Users, AlertTriangle, TrendingUp, RotateCcw, Radio, MapPin, Flame, ShieldAlert, Server, BellRing, Video, Upload, Camera, Square, Play } from 'lucide-react'

export default function App() {
  const [connected, setConnected] = useState(false)
  const [mode, setMode] = useState('live') // live | upload | dashboard
  const [ BottomTab, setBottomTab ] = useState('alerts')
  const [telemetry, setTelemetry] = useState({
    cci: 12.5, ops: 5.0, psi: 0.08, decibel: 54.2, person_count: 84,
    stress_pitch_drift: 0.02, screaming: false, alarm_level: "GREEN", dispatches: [], recent_alerts: []
  })
  const [videoState, setVideoState] = useState({ mode: 'simulation', active: false, progress: 0 })
  const [simEnabled, setSimEnabled] = useState(false)
  const [liveFrame, setLiveFrame] = useState(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [uploading, setUploading] = useState(false)

  const wsRef = useRef(null)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)
  const intervalRef = useRef(null)
  const fileVideoRef = useRef(null)

  const API_HOST = window.location.hostname || "localhost"
  const WS_URL = `ws://${API_HOST}:8000/ws/stream`
  const HTTP_URL = `http://${API_HOST}:8000/api`

  const connectWebSocket = () => {
    const ws = new WebSocket(WS_URL)
    wsRef.current = ws
    ws.onopen = () => setConnected(true)
    ws.onmessage = (e) => {
      try {
        const p = JSON.parse(e.data)
        if (p.data) setTelemetry(p.data)
        if (p.video_state) setVideoState(p.video_state)
        if (p.event === 'video_frame' && p.frame) setLiveFrame(`data:image/jpeg;base64,${p.frame}`)
      } catch {}
    }
    ws.onclose = () => { setConnected(false); setTimeout(connectWebSocket, 3000) }
    ws.onerror = () => ws.close()
  }
  useEffect(() => { connectWebSocket(); fetch(`${HTTP_URL}/simulation`).then(r=>r.json()).then(j=>setSimEnabled(!!j.simulation_enabled)).catch(()=>{}); return () => { wsRef.current?.close(); stopLive() } }, [])
  const toggleSim = async () => {
    const next = !simEnabled
    const r = await fetch(`${HTTP_URL}/simulation`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({enabled: next})})
    const j = await r.json(); setSimEnabled(!!j.simulation_enabled)
  }

  // Live camera
  const startLive = async () => {
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 360 }, audio: false })
      streamRef.current = s
      if (videoRef.current) { videoRef.current.srcObject = s; await videoRef.current.play() }
      setIsStreaming(true)
      fetch(`${HTTP_URL}/video/live/start`, { method: 'POST' }).catch(()=>{})
      // send frames via WS if open, else HTTP
      intervalRef.current = setInterval(() => {
        if (!videoRef.current || !canvasRef.current) return
        const c = canvasRef.current; c.width = 640; c.height = 360
        const ctx = c.getContext('2d'); ctx.drawImage(videoRef.current, 0, 0, 640, 360)
        const b64 = c.toDataURL('image/jpeg', 0.6)
        if (wsRef.current?.readyState === 1) {
          wsRef.current.send(JSON.stringify({ event: 'frame', frame: b64 }))
        } else {
          fetch(`${HTTP_URL}/video/live/frame`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ frame: b64 }) }).catch(()=>{})
        }
      }, 500) // 2 fps
    } catch (e) { alert('Camera access denied: '+ e.message) }
  }
  const stopLive = () => {
    clearInterval(intervalRef.current); intervalRef.current = null
    streamRef.current?.getTracks().forEach(t=>t.stop()); streamRef.current=null
    if (videoRef.current) videoRef.current.srcObject = null
    setIsStreaming(false); setLiveFrame(null)
    fetch(`${HTTP_URL}/video/live/stop`, { method:'POST'}).catch(()=>{})
  }

  // Upload
  const onUpload = async (e) => {
    const f = e.target.files?.[0]; if (!f) return
    setUploading(true)
    // preview locally
    if (fileVideoRef.current) { fileVideoRef.current.src = URL.createObjectURL(f); fileVideoRef.current.load() }
    const fd = new FormData(); fd.append('file', f)
    try {
      const r = await fetch(`${HTTP_URL}/video/upload`, { method:'POST', body: fd })
      const j = await r.json(); console.log('upload', j)
    } catch (err) { console.error(err); alert('Upload failed') }
    setUploading(false)
  }
  const stopVideo = async () => { await fetch(`${HTTP_URL}/video/stop`, {method:'POST'}); setLiveFrame(null) }

  const triggerDispatch = async (level) => {
    await fetch(`${HTTP_URL}/dispatch`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({alert_level: level})})
  }
  const resetSystem = async () => { await fetch(`${HTTP_URL}/reset`, {method:'POST'}); setLiveFrame(null) }

  const getAlarmColor = (level=telemetry.alarm_level) => ({RED:'#ef4444',ORANGE:'#f59e0b',YELLOW:'#eab308',GREEN:'#10b981'}[level]||'#10b981')
  const getAlarmClass = () => ({RED:'pulse-red',ORANGE:'pulse-orange',YELLOW:'pulse-yellow',GREEN:'pulse-green'}[telemetry.alarm_level]||'pulse-green')

  return (
    <div style={{maxWidth:1280, margin:'0 auto', padding:'20px 24px 40px'}}>
      {/* Header */}
      <header style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:20}}>
        <div style={{display:'flex',alignItems:'center',gap:12}}>
          <div style={{background:'linear-gradient(135deg,#2563eb,#10b981)',padding:9,borderRadius:12,display:'flex'}}><Shield size={22} color="#fff"/></div>
          <div>
            <h1 style={{fontSize:22,fontWeight:800,letterSpacing:'-0.02em',background:'linear-gradient(to right,#fff,#94a3b8)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>PRECIS</h1>
            <span style={{fontSize:10,color:'#64748b',letterSpacing:'0.08em',textTransform:'uppercase'}}>Crowd Intelligence Platform</span>
          </div>
        </div>
        <div style={{display:'flex',gap:10,alignItems:'center'}}>
          <span style={{display:'flex',alignItems:'center',gap:6,background:'rgba(15,23,42,0.6)',padding:'6px 12px',borderRadius:20,fontSize:11,border:'1px solid rgba(255,255,255,0.06)'}}>
            <Server size={12} color={connected?'#10b981':'#ef4444'}/><span style={{color: connected?'#a7f3d0':'#fca5a5'}}>{connected?'LIVE':'CONNECTING'}</span>
          </span>
          <span style={{display:'flex',alignItems:'center',gap:6,background:'rgba(15,23,42,0.6)',padding:'6px 12px',borderRadius:20,fontSize:11,border:`1px solid ${getAlarmColor()}30`}}>
            <span className={`status-dot ${telemetry.alarm_level.toLowerCase()}`}></span>
            <b style={{color:getAlarmColor()}}>{telemetry.alarm_level}</b>
            <span style={{color:'#64748b',marginLeft:4,fontSize:10}}>{videoState.mode?.toUpperCase()}</span>
          </span>
        </div>
      </header>

      {/* Mode tabs */}
      <div style={{display:'flex',gap:8,marginBottom:16}}>
        {[
          {id:'live',label:'Live Camera',icon:Camera},
          {id:'upload',label:'Recorded Video',icon:Upload},
          {id:'dashboard',label:'Telemetry',icon:Activity},
        ].map(t=>(
          <button key={t.id} onClick={()=>setMode(t.id)} style={{
            display:'flex',alignItems:'center',gap:7,padding:'8px 14px',borderRadius:10,fontSize:13,fontWeight:600,cursor:'pointer',
            background: mode===t.id?'#2563eb':'rgba(255,255,255,0.06)',color: mode===t.id?'#fff':'#94a3b8',border:'1px solid '+(mode===t.id?'#2563eb':'rgba(255,255,255,0.06)')
          }}><t.icon size={14}/>{t.label}</button>
        ))}
        <div style={{marginLeft:'auto',display:'flex',gap:8,alignItems:'center'}}>
          <button onClick={toggleSim} title={simEnabled ? 'Pause demo drift' : 'Enable demo drift'} style={{padding:'8px 12px',borderRadius:10,background: simEnabled?'rgba(16,185,129,0.15)':'rgba(255,255,255,0.06)',border:`1px solid ${simEnabled?'rgba(16,185,129,0.3)':'rgba(255,255,255,0.06)'}`,color: simEnabled?'#10b981':'#94a3b8',fontSize:11,fontWeight:700,display:'flex',alignItems:'center',gap:6,cursor:'pointer'}}>
            <Activity size={12}/>{simEnabled ? 'Demo ON' : 'Demo OFF'}
          </button>
          <button onClick={resetSystem} style={{padding:'8px 12px',borderRadius:10,background:'rgba(255,255,255,0.06)',border:'1px solid rgba(255,255,255,0.06)',color:'#94a3b8',fontSize:12,display:'flex',alignItems:'center',gap:6,cursor:'pointer'}}><RotateCcw size={12}/>Reset</button>
        </div>
      </div>

      {/* Main layout */}
      <div style={{display:'grid',gridTemplateColumns: mode==='dashboard' ? '1fr' : '1.55fr 0.85fr',gap:16}}>
        {/* VIDEO PANEL */}
        <section className="glass-panel" style={{padding:16,minHeight:380,display:'flex',flexDirection:'column',overflow:'hidden'}}>
          {mode==='live' && (
            <>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:12}}>
                <h3 style={{fontSize:13,fontWeight:700,color:'#e2e8f0',display:'flex',alignItems:'center',gap:8}}><Video size={14} color="#3b82f6"/>Live Camera Feed</h3>
                <div style={{display:'flex',gap:8}}>
                  {!isStreaming ? <button onClick={startLive} style={{background:'#10b981',color:'#fff',border:'none',padding:'7px 14px',borderRadius:8,fontSize:12,fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:6}}><Play size={12}/>Start Camera</button>
                  : <button onClick={stopLive} style={{background:'#ef4444',color:'#fff',border:'none',padding:'7px 14px',borderRadius:8,fontSize:12,fontWeight:700,cursor:'pointer',display:'flex',alignItems:'center',gap:6}}><Square size={12}/>Stop</button>}
                </div>
              </div>
              <div style={{flex:1,background:'#020617',borderRadius:12,overflow:'hidden',position:'relative',display:'flex',alignItems:'center',justifyContent:'center',border:'1px solid rgba(255,255,255,0.06)',minHeight:320}}>
                {/* hidden video + canvas */}
                <video ref={videoRef} autoPlay muted playsInline style={{display: isStreaming && !liveFrame ? 'block' : 'none',width:'100%',height:'100%',objectFit:'cover'}}/>
                {liveFrame ? <img src={liveFrame} alt="live" style={{width:'100%',height:'100%',objectFit:'cover'}}/> : !isStreaming && <div style={{textAlign:'center',color:'#475569',padding:40}}>
                  <Camera size={32} style={{opacity:0.4,marginBottom:8}}/><p style={{fontSize:12}}>Click <b style={{color:'#94a3b8'}}>Start Camera</b> to stream live webcam.<br/>Frames are sent to backend at 2 FPS for crowd analysis.</p>
                </div>}
                {isStreaming && <span style={{position:'absolute',top:10,left:10,background:'#ef4444',color:'#fff',fontSize:10,fontWeight:800,padding:'3px 8px',borderRadius:20,display:'flex',alignItems:'center',gap:6}}><span style={{width:7,height:7,background:'#fff',borderRadius:'50%',display:'inline-block',animation:'pulse-slow 1s infinite'}}/>REC</span>}
              </div>
              <canvas ref={canvasRef} style={{display:'none'}}/>
              <p style={{fontSize:10,color:'#475569',marginTop:8}}>Backend: <code style={{color:'#64748b'}}>/api/video/live/frame</code> • WS event <code>video_frame</code> • {videoState.active ? 'Processing' : 'Idle'}</p>
            </>
          )}
          {mode==='upload' && (
            <>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:12}}>
                <h3 style={{fontSize:13,fontWeight:700,color:'#e2e8f0',display:'flex',alignItems:'center',gap:8}}><Upload size={14} color="#8b5cf6"/>Recorded Video Analysis</h3>
                {videoState.active && <button onClick={stopVideo} style={{background:'rgba(239,68,68,0.15)',border:'1px solid rgba(239,68,68,0.25)',color:'#ef4444',padding:'6px 12px',borderRadius:8,fontSize:11,fontWeight:700,cursor:'pointer'}}><Square size={10}/> Stop Processing</button>}
              </div>
              <label style={{border:'1.5px dashed rgba(139,92,246,0.35)',background:'rgba(139,92,246,0.06)',borderRadius:12,padding:18,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',cursor:'pointer',marginBottom:12}}>
                <Upload size={20} color="#8b5cf6"/>
                <span style={{fontSize:12,fontWeight:600,color:'#c4b5fd',marginTop:6}}>{uploading ? 'Uploading...' : 'Drop or click to upload video'}</span>
                <span style={{fontSize:10,color:'#64748b'}}>MP4, AVI, MOV • processed at 5 FPS via OpenCV</span>
                <input type="file" accept="video/*" onChange={onUpload} style={{display:'none'}}/>
              </label>
              <div style={{flex:1,background:'#020617',borderRadius:12,overflow:'hidden',border:'1px solid rgba(255,255,255,0.06)',minHeight:260,display:'flex',alignItems:'center',justifyContent:'center'}}>
                {liveFrame ? <img src={liveFrame} alt="processed" style={{width:'100%',height:'100%',objectFit:'cover'}}/> :
                  <video ref={fileVideoRef} controls style={{width:'100%',height:'100%'}}/>
                }
                {!liveFrame && !fileVideoRef.current?.src && <span style={{fontSize:11,color:'#475569'}}>Preview appears here</span>}
              </div>
              {videoState.active && (
                <div style={{marginTop:10}}>
                  <div style={{display:'flex',justifyContent:'space-between',fontSize:11,color:'#94a3b8',marginBottom:4}}><span>Processing {videoState.filename}</span><span>{videoState.progress}%</span></div>
                  <div style={{height:6,background:'rgba(255,255,255,0.08)',borderRadius:4,overflow:'hidden'}}><div style={{width:`${videoState.progress}%`,height:'100%',background:'#8b5cf6',transition:'width 0.3s'}}/></div>
                </div>
              )}
            </>
          )}
          {mode==='dashboard' && (
            <div style={{display:'flex',flexDirection:'column',gap:14}}>
              <h3 style={{fontSize:13,fontWeight:700,color:'#e2e8f0',display:'flex',alignItems:'center',gap:8}}><Activity size={14} color="#3b82f6"/>System Overview</h3>
              <div style={{height:160,background:'#020617',borderRadius:12,border:'1px solid rgba(255,255,255,0.06)',display:'flex',alignItems:'center',justifyContent:'center'}}>
                {liveFrame ? <img src={liveFrame} alt="frame" style={{width:'100%',height:'100%',objectFit:'cover',borderRadius:12}}/> : <span style={{fontSize:11,color:'#475569'}}>No active video — switch to Live or Upload</span>}
              </div>
            </div>
          )}
        </section>

        {/* TELEMETRY PANEL */}
        <div style={{display:'flex',flexDirection:'column',gap:12}}>
          <section className={`glass-panel ${getAlarmClass()}`} style={{padding:16}}>
            <h3 style={{fontSize:12,fontWeight:700,color:'#e2e8f0',display:'flex',alignItems:'center',gap:6,marginBottom:12}}><Activity size={14} color={getAlarmColor()}/> Crowd Resonance</h3>
            <div style={{display:'flex',alignItems:'center',gap:14,marginBottom:14}}>
              <div style={{width:96,height:96,borderRadius:'50%',background:`conic-gradient(${getAlarmColor()} ${telemetry.cci}%, rgba(255,255,255,0.06) 0)`,display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
                <div style={{width:78,height:78,borderRadius:'50%',background:'#0f172a',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center'}}>
                  <span style={{fontSize:20,fontWeight:800,color:'#fff'}}>{telemetry.cci}%</span><span style={{fontSize:7,color:'#64748b',fontWeight:700,letterSpacing:'0.08em'}}>CCI</span>
                </div>
              </div>
              <div style={{flex:1}}>
                <div style={{fontSize:11,color:'#94a3b8',marginBottom:2}}>Outstroke Probability</div>
                <div style={{display:'flex',justifyContent:'space-between',fontSize:12,marginBottom:4}}><span style={{color:'#64748b'}}>OPS</span><b style={{color:getAlarmColor(telemetry.ops>70?'RED':telemetry.ops>40?'ORANGE':'GREEN')}}>{telemetry.ops}%</b></div>
                <div style={{height:6,background:'rgba(255,255,255,0.06)',borderRadius:4,overflow:'hidden',marginBottom:10}}><div style={{width:`${telemetry.ops}%`,height:'100%',background:getAlarmColor(telemetry.ops>70?'RED':telemetry.ops>40?'ORANGE':'GREEN'),transition:'width 0.5s'}}/></div>
                <div style={{display:'flex',justifyContent:'space-between',fontSize:12}}><span style={{color:'#64748b'}}>PSI</span><b style={{color:'#3b82f6'}}>{telemetry.psi}</b></div>
                <div style={{height:6,background:'rgba(255,255,255,0.06)',borderRadius:4,overflow:'hidden',marginTop:4}}><div style={{width:`${telemetry.psi*100}%`,height:'100%',background:'#3b82f6'}}/></div>
              </div>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
              <div style={{background:'rgba(255,255,255,0.04)',borderRadius:10,padding:10,display:'flex',alignItems:'center',gap:8}}>
                <Users size={16} color="#3b82f6"/><div><div style={{fontSize:9,color:'#64748b',fontWeight:700}}>CROWD</div><div style={{fontSize:13,fontWeight:700}}>{telemetry.person_count}</div></div>
              </div>
              <div style={{background:'rgba(255,255,255,0.04)',borderRadius:10,padding:10,display:'flex',alignItems:'center',gap:8}}>
                <Volume2 size={16} color="#10b981"/><div><div style={{fontSize:9,color:'#64748b',fontWeight:700}}>dB</div><div style={{fontSize:13,fontWeight:700}}>{telemetry.decibel}</div></div>
              </div>
              <div style={{background:'rgba(255,255,255,0.04)',borderRadius:10,padding:10,display:'flex',alignItems:'center',gap:8}}>
                <TrendingUp size={16} color="#eab308"/><div><div style={{fontSize:9,color:'#64748b',fontWeight:700}}>STRESS</div><div style={{fontSize:13,fontWeight:700}}>{telemetry.stress_pitch_drift}</div></div>
              </div>
              <div style={{background: telemetry.screaming?'rgba(239,68,68,0.08)':'rgba(255,255,255,0.04)',border:`1px solid ${telemetry.screaming?'rgba(239,68,68,0.2)':'transparent'}`,borderRadius:10,padding:10,display:'flex',alignItems:'center',gap:8}}>
                <Radio size={16} color={telemetry.screaming?'#ef4444':'#64748b'}/><div><div style={{fontSize:9,color:'#64748b',fontWeight:700}}>SCREAM</div><div style={{fontSize:11,fontWeight:700,color:telemetry.screaming?'#ef4444':'#94a3b8'}}>{telemetry.screaming?'DETECTED':'NOMINAL'}</div></div>
              </div>
            </div>
          </section>

          <section className="glass-panel" style={{padding:14}}>
            <h3 style={{fontSize:12,fontWeight:700,color:'#e2e8f0',display:'flex',alignItems:'center',gap:6,marginBottom:10}}><ShieldAlert size={14} color="#f59e0b"/> Dispatch</h3>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
              {['YELLOW','ORANGE','RED'].map(l=>(
                <button key={l} onClick={()=>triggerDispatch(l)} style={{padding:'8px',borderRadius:8,fontSize:11,fontWeight:700,cursor:'pointer',border:`1px solid ${l==='RED'?'rgba(239,68,68,0.3)':l==='ORANGE'?'rgba(245,158,11,0.3)':'rgba(234,179,8,0.3)'}`,background:l==='RED'?'rgba(239,68,68,0.12)':l==='ORANGE'?'rgba(245,158,11,0.1)':'rgba(234,179,8,0.1)',color:getAlarmColor(l)}}>Trigger {l}</button>
              ))}
              <button onClick={resetSystem} style={{padding:'8px',borderRadius:8,fontSize:11,fontWeight:600,cursor:'pointer',background:'rgba(255,255,255,0.04)',border:'1px solid rgba(255,255,255,0.06)',color:'#94a3b8',display:'flex',alignItems:'center',justifyContent:'center',gap:6}}><RotateCcw size={10}/>Reset</button>
            </div>
          </section>
        </div>
      </div>

      {/* Bottom feed */}
      <div className="glass-panel" style={{marginTop:14,padding:0,overflow:'hidden'}}>
        <div style={{display:'flex',gap:0,borderBottom:'1px solid rgba(255,255,255,0.06)'}}>
          {[{id:'alerts',label:'Live Alerts',icon:BellRing},{id:'dispatches',label:'Dispatches',icon:MapPin}].map(t=>(
            <button key={t.id} onClick={()=>setBottomTab(t.id)} style={{flex:1,padding:'10px',fontSize:12,fontWeight:700,display:'flex',alignItems:'center',justifyContent:'center',gap:6,cursor:'pointer',background:BottomTab===t.id?'rgba(255,255,255,0.04)':'transparent',color:BottomTab===t.id?'#e2e8f0':'#64748b',border:'none',borderBottom:BottomTab===t.id?'2px solid #3b82f6':'2px solid transparent'}}><t.icon size={13}/>{t.label} {t.id==='alerts'?`(${telemetry.recent_alerts.length})`:`(${telemetry.dispatches.length})`}</button>
          ))}
        </div>
        <div style={{maxHeight:200,overflowY:'auto',padding:12}}>
          {BottomTab==='alerts' ? (
            telemetry.recent_alerts.length===0 ? <p style={{fontSize:11,color:'#475569',textAlign:'center',padding:16}}>No active alarms.</p> :
            <div style={{display:'flex',flexDirection:'column',gap:8}}>
              {telemetry.recent_alerts.map((a,i)=>(
                <div key={i} style={{padding:'8px 10px',borderRadius:8,background:'rgba(15,23,42,0.6)',borderLeft:`3px solid ${getAlarmColor(a.level)}`,fontSize:11,display:'flex',justifyContent:'space-between',gap:12}}>
                  <span><b style={{color:getAlarmColor(a.level)}}>{a.level}</b> <span style={{color:'#cbd5e1',marginLeft:6}}>{a.message}</span></span><span style={{color:'#475569',fontSize:10,whiteSpace:'nowrap'}}>{a.timestamp}</span>
                </div>
              ))}
            </div>
          ) : (
            telemetry.dispatches.length===0 ? <p style={{fontSize:11,color:'#475569',textAlign:'center',padding:16}}>No dispatches.</p> :
            <table style={{width:'100%',fontSize:11,borderCollapse:'collapse'}}>
              <thead><tr style={{color:'#64748b',borderBottom:'1px solid rgba(255,255,255,0.06)'}}><th style={{padding:'6px 8px',textAlign:'left'}}>ID</th><th style={{padding:6}}>LEVEL</th><th style={{padding:6}}>UNITS</th><th style={{padding:6}}>COORDS</th><th style={{padding:6}}>STATUS</th></tr></thead>
              <tbody>{telemetry.dispatches.map((d,i)=>(
                <tr key={i} style={{borderBottom:'1px solid rgba(255,255,255,0.03)',color:'#e2e8f0'}}><td style={{padding:'8px',fontWeight:600}}>{d.dispatch_id}</td><td style={{color:getAlarmColor(d.alert_level),fontWeight:700}}>{d.alert_level}</td><td style={{textAlign:'center'}}>{d.allocated_police_units}P / {d.allocated_medical_units}M / {d.allocated_fire_units}F</td><td style={{color:'#94a3b8',fontSize:10}}>{d.triage_zone.lat.toFixed(4)}, {d.triage_zone.lng.toFixed(4)}</td><td><span style={{background:'rgba(16,185,129,0.12)',border:'1px solid rgba(16,185,129,0.2)',padding:'2px 6px',borderRadius:4,color:'#10b981',fontSize:9,fontWeight:700}}>{d.status}</span></td></tr>
              ))}</tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
