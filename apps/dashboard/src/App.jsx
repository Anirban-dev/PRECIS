import React, { useState, useEffect, useRef } from 'react'
import { 
  Shield, 
  Activity, 
  Volume2, 
  Users, 
  AlertTriangle, 
  TrendingUp, 
  RotateCcw, 
  Radio, 
  MapPin, 
  Flame, 
  ShieldAlert,
  Server,
  BellRing
} from 'lucide-react'

export default function App() {
  const [connected, setConnected] = useState(false)
  const [telemetry, setTelemetry] = useState({
    cci: 12.5,
    ops: 5.0,
    psi: 0.08,
    decibel: 54.2,
    person_count: 84,
    stress_pitch_drift: 0.02,
    screaming: false,
    alarm_level: "GREEN",
    dispatches: [],
    recent_alerts: []
  })
  
  const wsRef = useRef(null)
  const reconnectTimeoutRef = useRef(null)

  // API host configuration
  const API_HOST = window.location.hostname || "localhost"
  const WS_URL = `ws://${API_HOST}:8000/ws/stream`
  const HTTP_URL = `http://${API_HOST}:8000/api`

  const connectWebSocket = () => {
    console.log(`Connecting to WebSocket at: ${WS_URL}`)
    const ws = new WebSocket(WS_URL)
    wsRef.current = ws

    ws.onopen = () => {
      console.log("WebSocket connected.")
      setConnected(true)
    }

    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data)
        if (payload.data) {
          setTelemetry(payload.data)
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err)
      }
    }

    ws.onclose = () => {
      console.log("WebSocket disconnected. Attempting reconnect...")
      setConnected(false)
      reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000)
    }

    ws.onerror = (err) => {
      console.error("WebSocket error:", err)
      ws.close()
    }
  }

  useEffect(() => {
    connectWebSocket()
    return () => {
      if (wsRef.current) wsRef.current.close()
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current)
    }
  }, [])

  // Trigger dispatch REST call
  const triggerDispatch = async (level) => {
    try {
      const response = await fetch(`${HTTP_URL}/dispatch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ alert_level: level })
      })
      const data = await response.json()
      console.log(`Dispatch triggered for ${level}:`, data)
    } catch (error) {
      console.error("Failed to trigger dispatch:", error)
    }
  }

  // Reset system state REST call
  const resetSystem = async () => {
    try {
      const response = await fetch(`${HTTP_URL}/reset`, { method: "POST" })
      const data = await response.json()
      console.log("System state reset:", data)
    } catch (error) {
      console.error("Failed to reset system:", error)
    }
  }

  // Class helper for alert pulse effects
  const getAlarmClass = () => {
    switch (telemetry.alarm_level) {
      case "RED": return "pulse-red"
      case "ORANGE": return "pulse-orange"
      case "YELLOW": return "pulse-yellow"
      default: return "pulse-green"
    }
  }

  // Color helper for text & highlights
  const getAlarmColor = (level = telemetry.alarm_level) => {
    switch (level) {
      case "RED": return "#ef4444"
      case "ORANGE": return "#f59e0b"
      case "YELLOW": return "#eab308"
      default: return "#10b981"
    }
  }

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px', boxSizing: 'border-box' }}>
      {/* Header section */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingBottom: '20px',
        borderBottom: '1px solid rgba(255,255,255,0.08)',
        marginBottom: '30px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #2563eb, #10b981)',
            padding: '10px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Shield size={28} color="#ffffff" />
          </div>
          <div>
            <h1 style={{ fontSize: '24px', fontWeight: '800', background: 'linear-gradient(to right, #ffffff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              PRECIS
            </h1>
            <span style={{ fontSize: '11px', color: '#64748b', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
              Predictive Crowd Resonance & Intelligence
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            backgroundColor: 'rgba(15,23,42,0.6)',
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '12px',
            border: '1px solid rgba(255,255,255,0.05)'
          }}>
            <Server size={14} color={connected ? "#10b981" : "#ef4444"} />
            <span style={{ color: connected ? "#a7f3d0" : "#fca5a5" }}>
              {connected ? "LIVE METRICS" : "CONNECTING..."}
            </span>
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            backgroundColor: 'rgba(15,23,42,0.6)',
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '12px',
            border: '1px solid rgba(255,255,255,0.05)'
          }}>
            <span className={`status-dot ${telemetry.alarm_level.toLowerCase()}`}></span>
            <span style={{ fontWeight: '700', color: getAlarmColor() }}>
              SYSTEM LEVEL: {telemetry.alarm_level}
            </span>
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '24px' }}>
        
        {/* Main dials: CCI & OPS */}
        <section className={`glass-panel ${getAlarmClass()}`} style={{
          gridColumn: 'span 8',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          minHeight: '260px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div>
              <h2 style={{ fontSize: '18px', fontWeight: '700', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Activity size={18} color="#3b82f6" /> Real-time Crowd Resonance
              </h2>
              <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                Synthesized crowd dynamics, velocity convergence, and vocal stress indicators.
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '30px', alignItems: 'center', flexWrap: 'wrap' }}>
            <div style={{ flex: '1', minWidth: '180px', display: 'flex', alignItems: 'center', gap: '20px' }}>
              <div style={{
                position: 'relative',
                width: '120px',
                height: '120px',
                borderRadius: '50%',
                background: `conic-gradient(${getAlarmColor()} ${telemetry.cci}%, rgba(255,255,255,0.05) 0)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <div style={{
                  position: 'absolute',
                  width: '100px',
                  height: '100px',
                  borderRadius: '50%',
                  backgroundColor: '#0f172a',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <span style={{ fontSize: '28px', fontWeight: '800', fontFamily: 'Outfit', color: '#ffffff' }}>
                    {telemetry.cci}%
                  </span>
                  <span style={{ fontSize: '9px', color: '#64748b', fontWeight: '600', letterSpacing: '0.05em' }}>
                    CCI INDEX
                  </span>
                </div>
              </div>
              <div>
                <h3 style={{ fontSize: '16px', fontWeight: '600' }}>Crowd Criticality</h3>
                <p style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
                  Risk of immediate crowd instability based on acoustic waves and motion divergence vectors.
                </p>
              </div>
            </div>

            <div style={{ flex: '1', minWidth: '180px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '13px' }}>
                <span style={{ color: '#94a3b8', fontWeight: '500' }}>Outstroke Probability (OPS)</span>
                <span style={{ fontWeight: '700', color: getAlarmColor(telemetry.ops > 70 ? "RED" : telemetry.ops > 40 ? "ORANGE" : "GREEN") }}>
                  {telemetry.ops}%
                </span>
              </div>
              <div style={{ height: '8px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                  width: `${telemetry.ops}%`,
                  height: '100%',
                  background: `linear-gradient(to right, #10b981, ${getAlarmColor(telemetry.ops > 70 ? "RED" : telemetry.ops > 40 ? "ORANGE" : "GREEN")})`,
                  borderRadius: '4px',
                  transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)'
                }}></div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '16px', marginBottom: '8px', fontSize: '13px' }}>
                <span style={{ color: '#94a3b8', fontWeight: '500' }}>Phase State Index (PSI)</span>
                <span style={{ fontWeight: '700', color: '#3b82f6' }}>{telemetry.psi}</span>
              </div>
              <div style={{ height: '8px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                  width: `${telemetry.psi * 100}%`,
                  height: '100%',
                  backgroundColor: '#3b82f6',
                  borderRadius: '4px',
                  transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)'
                }}></div>
              </div>
            </div>
          </div>
        </section>

        {/* Dispatch Control panel */}
        <section className="glass-panel" style={{
          gridColumn: 'span 4',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          minHeight: '260px'
        }}>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: '700', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <ShieldAlert size={18} color="#f59e0b" /> Dispatch Control Room
            </h2>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>
              Anticipatory triage triggers for emergency deployment services.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', margin: '20px 0' }}>
            <button 
              onClick={() => triggerDispatch("YELLOW")}
              style={{
                padding: '10px',
                backgroundColor: 'rgba(234, 179, 8, 0.1)',
                border: '1px solid rgba(234, 179, 8, 0.2)',
                borderRadius: '8px',
                color: '#eab308',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(234, 179, 8, 0.2)' }}
              onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(234, 179, 8, 0.1)' }}
            >
              Trigger Yellow
            </button>
            <button 
              onClick={() => triggerDispatch("ORANGE")}
              style={{
                padding: '10px',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                border: '1px solid rgba(245, 158, 11, 0.2)',
                borderRadius: '8px',
                color: '#f59e0b',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(245, 158, 11, 0.2)' }}
              onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(245, 158, 11, 0.1)' }}
            >
              Trigger Orange
            </button>
            <button 
              onClick={() => triggerDispatch("RED")}
              style={{
                padding: '10px',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                border: '1px solid rgba(239, 68, 68, 0.2)',
                borderRadius: '8px',
                color: '#ef4444',
                fontWeight: '700',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.2)' }}
              onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)' }}
            >
              Trigger RED Alert
            </button>
            <button 
              onClick={resetSystem}
              style={{
                padding: '10px',
                backgroundColor: 'rgba(148, 163, 184, 0.05)',
                border: '1px solid rgba(148, 163, 184, 0.1)',
                borderRadius: '8px',
                color: '#94a3b8',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(148, 163, 184, 0.1)' }}
              onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(148, 163, 184, 0.05)' }}
            >
              <RotateCcw size={14} /> Reset State
            </button>
          </div>
        </section>

        {/* Telemetry card grid */}
        <div style={{ gridColumn: 'span 12', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
          
          <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'rgba(59, 130, 246, 0.1)', display: 'flex' }}>
              <Users size={22} color="#3b82f6" />
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Crowd Size</span>
              <h3 style={{ fontSize: '20px', fontWeight: '700', color: '#f8fafc' }}>{telemetry.person_count} <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: 'normal' }}>tracked</span></h3>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'rgba(16, 185, 129, 0.1)', display: 'flex' }}>
              <Volume2 size={22} color="#10b981" />
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Acoustic Amplitude</span>
              <h3 style={{ fontSize: '20px', fontWeight: '700', color: '#f8fafc' }}>{telemetry.decibel} <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: 'normal' }}>dB</span></h3>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'rgba(234, 179, 8, 0.1)', display: 'flex' }}>
              <TrendingUp size={22} color="#eab308" />
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Stress Pitch Drift</span>
              <h3 style={{ fontSize: '20px', fontWeight: '700', color: '#f8fafc' }}>{telemetry.stress_pitch_drift}</h3>
            </div>
          </div>

          <div className="glass-panel" style={{ 
            padding: '20px', 
            display: 'flex', 
            alignItems: 'center', 
            gap: '16px', 
            border: telemetry.screaming ? '1px solid rgba(239, 68, 68, 0.3)' : '1px solid rgba(255,255,255,0.08)',
            backgroundColor: telemetry.screaming ? 'rgba(239, 68, 68, 0.05)' : 'rgba(15, 23, 42, 0.45)'
          }}>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: telemetry.screaming ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255,255,255,0.05)', display: 'flex' }}>
              <Radio size={22} color={telemetry.screaming ? "#ef4444" : "#94a3b8"} />
            </div>
            <div>
              <span style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', fontWeight: '600' }}>Screaming State</span>
              <h3 style={{ fontSize: '18px', fontWeight: '700', color: telemetry.screaming ? '#ef4444' : '#94a3b8' }}>
                {telemetry.screaming ? "CRITICAL DETECTED" : "NOMINAL"}
              </h3>
            </div>
          </div>

        </div>

        {/* Real-time Alerts feed */}
        <section className="glass-panel" style={{
          gridColumn: 'span 5',
          padding: '20px',
          height: '360px',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <h2 style={{ fontSize: '16px', fontWeight: '700', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
            <BellRing size={16} color="#ef4444" /> Live Warning Logs
          </h2>
          <div style={{ flex: '1', overflowY: 'auto', marginTop: '12px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {telemetry.recent_alerts.length === 0 ? (
              <p style={{ color: '#475569', fontSize: '12px', textAlign: 'center', padding: '20px 0' }}>No active alarms detected.</p>
            ) : (
              telemetry.recent_alerts.map((alert, idx) => (
                <div key={idx} style={{
                  padding: '10px',
                  borderRadius: '8px',
                  backgroundColor: 'rgba(15, 23, 42, 0.6)',
                  borderLeft: `3px solid ${getAlarmColor(alert.level)}`,
                  fontSize: '12px',
                  lineHeight: '1.4'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ color: getAlarmColor(alert.level), fontWeight: '700' }}>{alert.level}</span>
                    <span style={{ color: '#475569', fontSize: '10px' }}>{alert.timestamp}</span>
                  </div>
                  <p style={{ margin: '0', color: '#cbd5e1' }}>{alert.message}</p>
                </div>
              ))
            )}
          </div>
        </section>

        {/* Active Dispatches table */}
        <section className="glass-panel" style={{
          gridColumn: 'span 7',
          padding: '20px',
          height: '360px',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <h2 style={{ fontSize: '16px', fontWeight: '700', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
            <MapPin size={16} color="#3b82f6" /> Emergency Dispatches
          </h2>
          
          <div style={{ flex: '1', overflowY: 'auto', marginTop: '12px' }}>
            {telemetry.dispatches.length === 0 ? (
              <p style={{ color: '#475569', fontSize: '12px', textAlign: 'center', padding: '20px 0' }}>No emergency dispatches active.</p>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', textAlign: 'left' }}>
                <thead>
                  <tr style={{ color: '#64748b', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <th style={{ padding: '8px' }}>ID</th>
                    <th style={{ padding: '8px' }}>LEVEL</th>
                    <th style={{ padding: '8px' }}>UNITS (P/M/F)</th>
                    <th style={{ padding: '8px' }}>COORDINATES</th>
                    <th style={{ padding: '8px' }}>STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  {telemetry.dispatches.map((dispatch, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)', color: '#e2e8f0' }}>
                      <td style={{ padding: '10px 8px', fontWeight: '600' }}>{dispatch.dispatch_id}</td>
                      <td style={{ padding: '10px 8px', color: getAlarmColor(dispatch.alert_level), fontWeight: '700' }}>
                        {dispatch.alert_level}
                      </td>
                      <td style={{ padding: '10px 8px' }}>
                        <span style={{ color: '#93c5fd' }}>{dispatch.allocated_police_units}P</span> / <span style={{ color: '#fca5a5' }}>{dispatch.allocated_medical_units}M</span> / <span style={{ color: '#fcd34d' }}>{dispatch.allocated_fire_units}F</span>
                      </td>
                      <td style={{ padding: '10px 8px', color: '#94a3b8' }}>
                        {dispatch.triage_zone.lat.toFixed(4)}, {dispatch.triage_zone.lng.toFixed(4)}
                      </td>
                      <td style={{ padding: '10px 8px' }}>
                        <span style={{
                          backgroundColor: 'rgba(16, 185, 129, 0.1)',
                          border: '1px solid rgba(16, 185, 129, 0.2)',
                          padding: '2px 6px',
                          borderRadius: '4px',
                          color: '#10b981',
                          fontWeight: 'bold',
                          fontSize: '10px'
                        }}>
                          {dispatch.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>

      </div>
    </div>
  )
}
