import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, Shield, AlertTriangle, AlertCircle, RefreshCw, 
  MapPin, Eye, Volume2, Users, Radio, Navigation, 
  Zap, HeartHandshake, ShieldAlert, Cpu
} from 'lucide-react';

export default function App() {
  const [data, setData] = useState({
    cci: 12.5,
    ops: 5.0,
    psi: 0.08,
    decibel: 54.2,
    person_count: 84,
    stress_pitch_drift: 0.02,
    screaming: false,
    alarm_level: 'GREEN',
    dispatches: [],
    recent_alerts: []
  });

  const [wsStatus, setWsStatus] = useState('CONNECTING');
  const [demoTriggering, setDemoTriggering] = useState(false);
  const [simMode, setSimMode] = useState(false);
  const [chartData, setChartData] = useState([]);
  
  const canvasRef = useRef(null);

  // Connect to WebSocket API Gateway
  useEffect(() => {
    let ws;
    let reconnectTimeout;
    
    function connect() {
      setWsStatus('CONNECTING');
      ws = new WebSocket('ws://localhost:8000/ws/stream');
      
      ws.onopen = () => {
        setWsStatus('CONNECTED');
        setSimMode(false);
        console.log('Connected to PRECIS API Gateway');
      };
      
      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          setData(payload.data);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };
      
      ws.onerror = (err) => {
        console.warn('WebSocket error, falling back to local simulation...');
        setWsStatus('DISCONNECTED');
      };
      
      ws.onclose = () => {
        setWsStatus('DISCONNECTED');
        // Retry connection every 5 seconds
        reconnectTimeout = setTimeout(connect, 5000);
      };
    }
    
    connect();
    
    return () => {
      if (ws) ws.close();
      clearTimeout(reconnectTimeout);
    };
  }, []);

  // Simple local simulation fallback if FastAPI server is not running yet
  useEffect(() => {
    if (wsStatus !== 'DISCONNECTED') return;
    setSimMode(true);
    
    let interval = setInterval(() => {
      setData(prev => {
        const cci = prev.cci;
        const alarm = prev.alarm_level;
        
        let nextPsi = prev.psi;
        let nextDecibel = prev.decibel;
        let nextStress = prev.stress_pitch_drift;
        let nextScream = prev.screaming;
        let count = prev.person_count;
        
        if (alarm === 'RED' || alarm === 'ORANGE') {
          // decay emergency back to normal
          const nextCci = Math.max(12.5, prev.cci - 3.5);
          const nextOps = Math.max(5.0, prev.ops - 4.2);
          const nextLvl = nextCci >= 80 ? 'RED' : nextCci >= 55 ? 'ORANGE' : nextCci >= 30 ? 'YELLOW' : 'GREEN';
          return {
            ...prev,
            cci: parseFloat(nextCci.toFixed(1)),
            ops: parseFloat(nextOps.toFixed(1)),
            psi: parseFloat(Math.max(0.08, prev.psi - 0.04).toFixed(2)),
            decibel: parseFloat(Math.max(54.2, prev.decibel - 1.2).toFixed(1)),
            stress_pitch_drift: parseFloat(Math.max(0.02, prev.stress_pitch_drift - 0.02).toFixed(2)),
            screaming: nextCci < 30 ? false : prev.screaming,
            alarm_level: nextLvl
          };
        }
        
        // Random walk simulation for base state
        nextPsi = Math.max(0.02, Math.min(0.9, prev.psi + (Math.random() - 0.5) * 0.02));
        nextDecibel = Math.max(45, Math.min(85, prev.decibel + (Math.random() - 0.5) * 2));
        nextStress = Math.max(0.0, Math.min(1.0, prev.stress_pitch_drift + (Math.random() - 0.5) * 0.01));
        count = Math.max(40, Math.min(180, prev.person_count + randomInt(-3, 3)));
        
        const computedCci = (nextPsi * 100 * 0.5) + (nextStress * 100 * 0.3) + (((nextDecibel - 40) * 1.5) * 0.2);
        const finalCci = Math.max(0, Math.min(100, computedCci));
        
        const ops = 100 / (1 + Math.exp(-10 * (nextPsi - 0.5)));
        
        let nextLvl = 'GREEN';
        if (finalCci >= 80) nextLvl = 'RED';
        else if (finalCci >= 55) nextLvl = 'ORANGE';
        else if (finalCci >= 30) nextLvl = 'YELLOW';
        
        return {
          ...prev,
          cci: parseFloat(finalCci.toFixed(1)),
          ops: parseFloat(ops.toFixed(1)),
          psi: parseFloat(nextPsi.toFixed(2)),
          decibel: parseFloat(nextDecibel.toFixed(1)),
          stress_pitch_drift: parseFloat(nextStress.toFixed(2)),
          screaming: nextLvl === 'RED' ? true : false,
          person_count: count,
          alarm_level: nextLvl
        };
      });
    }, 1500);
    
    return () => clearInterval(interval);
  }, [wsStatus]);

  // Keep a running timeline chart in state
  useEffect(() => {
    setChartData(prev => {
      const updated = [...prev, { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), cci: data.cci, ops: data.ops }];
      if (updated.length > 15) updated.shift();
      return updated;
    });
  }, [data.cci, data.ops]);

  // Optical flow / vector field animation canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrame;
    
    // Create random particles tracking crowd motion
    const particles = [];
    for (let i = 0; i < 40; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        color: 'hsla(250, 89%, 65%, 0.4)'
      });
    }

    function render() {
      ctx.fillStyle = 'rgba(10, 15, 30, 0.2)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw grid lines representing optical flow mesh
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
      ctx.lineWidth = 1;
      const step = 20;
      for (let x = 0; x < canvas.width; x += step) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += step) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Draw particle flow vectors
      const scale = data.psi * 8; // Higher PSI = higher speed vectors
      particles.forEach(p => {
        p.vx = p.vx * 0.95 + (Math.random() - 0.5) * scale;
        p.vy = p.vy * 0.95 + (Math.random() - 0.5) * scale;
        
        p.x += p.vx;
        p.y += p.vy;
        
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = data.alarm_level === 'RED' ? 'rgba(239, 68, 68, 0.6)' : 'rgba(99, 102, 241, 0.6)';
        ctx.fill();

        // Vector line
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x + p.vx * 4, p.y + p.vy * 4);
        ctx.strokeStyle = data.alarm_level === 'RED' ? 'rgba(239, 68, 68, 0.3)' : 'rgba(99, 102, 241, 0.3)';
        ctx.lineWidth = 1.5;
        ctx.stroke();
      });

      // Draw mock tracking bounding boxes
      ctx.strokeStyle = data.alarm_level === 'RED' ? 'rgba(239, 68, 68, 0.8)' : 'rgba(34, 197, 94, 0.8)';
      ctx.lineWidth = 1.5;
      
      const boxes = [
        { x: 30, y: 40, w: 40, h: 80, label: 'TRK-242' },
        { x: 120, y: 70, w: 35, h: 75, label: 'TRK-105' },
        { x: 200, y: 30, w: 45, h: 90, label: 'TRK-89' }
      ];

      boxes.forEach(b => {
        // sway box slightly representing movement
        const sway = Math.sin(Date.now() / 200 + b.x) * (2 + data.psi * 15);
        ctx.strokeRect(b.x + sway, b.y, b.w, b.h);
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(b.x + sway, b.y - 15, 60, 15);
        
        ctx.fillStyle = '#fff';
        ctx.font = '9px Inter';
        ctx.fillText(b.label, b.x + sway + 4, b.y - 4);
      });

      // Draw shockwave center warning if RED
      if (data.alarm_level === 'RED') {
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, (Date.now() / 10) % 80, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.5)';
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      animationFrame = requestAnimationFrame(render);
    }
    
    render();
    
    return () => cancelAnimationFrame(animationFrame);
  }, [data.psi, data.alarm_level]);

  // Utility to generate random integer
  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  // Trigger FastAPI dispatch endpoint
  const handleDispatch = async (level) => {
    setDemoTriggering(true);
    try {
      if (wsStatus === 'CONNECTED') {
        await fetch('http://localhost:8000/api/dispatch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ alert_level: level })
        });
      } else {
        // Simulate locally in stand-alone mode
        const dispatch_id = `DSP-${Date.now()}-${randomInt(100, 999)}`;
        const allocated_police = level === 'RED' ? 12 : level === 'ORANGE' ? 6 : 3;
        const allocated_medical = level === 'RED' ? 6 : level === 'ORANGE' ? 3 : 1;
        const allocated_fire = level === 'RED' ? 3 : level === 'ORANGE' ? 1 : 0;
        
        const new_dispatch = {
          dispatch_id,
          timestamp: new Date().toLocaleTimeString(),
          alert_level: level,
          allocated_police_units: allocated_police,
          allocated_medical_units: allocated_medical,
          allocated_fire_units: allocated_fire,
          triage_zone: { lat: 22.5726, lng: 88.3639 },
          notified_hospitals: level === 'RED' ? ["Ruby General Hospital", "Fortis Healthcare"] : ["Ruby General Hospital"],
          status: "DISPATCHED"
        };
        
        setData(prev => ({
          ...prev,
          cci: level === 'RED' ? 92.4 : level === 'ORANGE' ? 68.2 : 42.1,
          ops: level === 'RED' ? 88.1 : level === 'ORANGE' ? 55.4 : 31.8,
          psi: level === 'RED' ? 0.89 : level === 'ORANGE' ? 0.61 : 0.42,
          alarm_level: level,
          dispatches: [new_dispatch, ...prev.dispatches].slice(0, 10),
          recent_alerts: [
            { timestamp: new Date().toLocaleTimeString(), message: `Anticipatory Dispatch dispatched. Level: ${level}. Units: Police: ${allocated_police}, Med: ${allocated_medical}.`, level },
            ...prev.recent_alerts
          ].slice(0, 15)
        }));
      }
    } catch (e) {
      console.error(e);
    }
    setDemoTriggering(false);
  };

  const handleReset = async () => {
    try {
      if (wsStatus === 'CONNECTED') {
        await fetch('http://localhost:8000/api/reset', { method: 'POST' });
      } else {
        setData(prev => ({
          ...prev,
          cci: 12.5,
          ops: 5.0,
          psi: 0.08,
          decibel: 54.2,
          person_count: 84,
          stress_pitch_drift: 0.02,
          screaming: false,
          alarm_level: 'GREEN',
          dispatches: [],
          recent_alerts: [{ timestamp: new Date().toLocaleTimeString(), message: "System status normalized. Monitoring active.", level: "GREEN" }]
        }));
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Color mapping utilities
  const getAlarmColorClass = (lvl) => {
    if (lvl === 'RED') return 'text-red-500 border-red-500/20 bg-red-500/5';
    if (lvl === 'ORANGE') return 'text-orange-500 border-orange-500/20 bg-orange-500/5';
    if (lvl === 'YELLOW') return 'text-yellow-500 border-yellow-500/20 bg-yellow-500/5';
    return 'text-emerald-500 border-emerald-500/20 bg-emerald-500/5';
  };

  const getAlarmHex = (lvl) => {
    if (lvl === 'RED') return '#ef4444';
    if (lvl === 'ORANGE') return '#f97316';
    if (lvl === 'YELLOW') return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#080B15] text-slate-100 p-6 md:p-8">
      {/* Top Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800/80 pb-6 mb-8">
        <div>
          <div className="flex items-center gap-3">
            <span className="bg-gradient-to-r from-indigo-500 to-violet-600 p-2 rounded-lg text-white">
              <Shield className="w-6 h-6" />
            </span>
            <div>
              <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">PRECIS</h1>
              <p className="text-slate-400 text-xs tracking-wider uppercase font-semibold">Neural-Shield CRIS v3 Control Portal</p>
            </div>
          </div>
        </div>
        
        {/* Status Indicators */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
            <span className={`pulse-indicator ${data.alarm_level.toLowerCase()}`} />
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">
              CROWD STATUS: {data.alarm_level}
            </span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
            <Radio className={`w-4 h-4 ${wsStatus === 'CONNECTED' ? 'text-indigo-400 animate-pulse' : 'text-slate-500'}`} />
            <span className="text-xs font-medium text-slate-300">
              GATEWAY: {wsStatus === 'CONNECTED' ? 'LIVE' : simMode ? 'STANDALONE (SIM)' : 'OFFLINE'}
            </span>
          </div>

          <button 
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs font-semibold"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            RESET DEMO
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <main className="dashboard-grid flex-1">
        {/* LEFT COLUMN: Vision Feed & Analytics Chart */}
        <section className="col-span-12 lg:col-span-7 flex flex-col gap-6">
          
          {/* CCTV Feed Mock Canvas */}
          <div className="glass-panel relative overflow-hidden flex-1 min-h-[350px] flex flex-col justify-between">
            <div className="absolute inset-0 bg-slate-950/80 z-0" />
            
            <canvas 
              ref={canvasRef} 
              width={640} 
              height={360}
              className="absolute inset-0 w-full h-full object-cover z-10"
            />
            
            {/* Overlay UI */}
            <div className="relative z-20 flex justify-between items-start pointer-events-none">
              <span className="flex items-center gap-2 px-2.5 py-1 rounded bg-black/60 border border-slate-800 text-xs text-slate-300">
                <Eye className="w-3.5 h-3.5 text-indigo-400" />
                LIVE VIDEO FEED: CAM-01 (Stadium Zone B)
              </span>
              <span className="px-2 py-1 rounded bg-red-600 text-[10px] font-bold text-white tracking-widest uppercase animate-pulse">
                REC
              </span>
            </div>

            <div className="relative z-20 flex justify-between items-end pointer-events-none mt-auto">
              <div className="flex flex-col gap-1 text-left bg-black/60 p-2.5 rounded border border-slate-800">
                <span className="text-[10px] font-bold text-slate-400">CLASSICAL CV METRICS:</span>
                <span className="text-xs text-slate-200">Sway Amplification: {(data.psi * 15).toFixed(1)} mm</span>
                <span className="text-xs text-slate-200">Dominant Freq: {(0.8 + data.psi * 0.4).toFixed(2)} Hz</span>
              </div>
              <div className="text-right text-[10px] font-mono text-slate-400 bg-black/60 p-2.5 rounded border border-slate-800">
                {new Date().toISOString()}
              </div>
            </div>
          </div>

          {/* Timeline Chart */}
          <div className="glass-panel">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-white">
              <Activity className="w-4 h-4 text-indigo-400" />
              Criticality Projection Time-series
            </h3>
            
            <div className="h-[180px] w-full flex items-end gap-1.5 border-b border-l border-slate-800 pb-2 pl-2">
              {chartData.map((d, i) => (
                <div key={i} className="flex-1 flex flex-col justify-end h-full group relative">
                  {/* CCI Bar */}
                  <div 
                    className="w-full rounded-t-sm transition-all duration-300"
                    style={{ 
                      height: `${d.cci}%`, 
                      background: `linear-gradient(to top, rgba(99, 102, 241, 0.2), ${getAlarmHex(data.alarm_level)})` 
                    }}
                  />
                  {/* Time label on hover */}
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block bg-slate-900 border border-slate-800 p-1.5 rounded text-[9px] whitespace-nowrap z-50">
                    <p className="text-white font-semibold">CCI: {d.cci}%</p>
                    <p className="text-slate-400">OPS: {d.ops}%</p>
                    <p className="text-slate-500">{d.time}</p>
                  </div>
                </div>
              ))}
              
              {chartData.length === 0 && (
                <div className="w-full h-full flex items-center justify-center text-slate-500 text-xs">
                  Awaiting data frames...
                </div>
              )}
            </div>
            <div className="flex justify-between items-center text-[10px] text-slate-500 mt-2">
              <span>-15 Frames</span>
              <span>Live Tick Time</span>
            </div>
          </div>

        </section>

        {/* RIGHT COLUMN: Core Gauges, Alerts, Dispatch Center */}
        <section className="col-span-12 lg:col-span-5 flex flex-col gap-6">
          
          {/* Key Analytics Gauges */}
          <div className="grid grid-cols-2 gap-4">
            {/* CCI Gauge */}
            <div className="glass-panel flex flex-col items-center justify-center text-center p-4">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Crowd Criticality (CCI)</span>
              <div className="relative flex items-center justify-center w-28 h-28">
                {/* SVG circular track */}
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="56" cy="56" r="48" stroke="#1e293b" strokeWidth="6" fill="transparent" />
                  <circle 
                    cx="56" 
                    cy="56" 
                    r="48" 
                    stroke={getAlarmHex(data.alarm_level)} 
                    strokeWidth="8" 
                    fill="transparent" 
                    strokeDasharray={301.6}
                    strokeDashoffset={301.6 - (301.6 * data.cci) / 100}
                    className="transition-all duration-500"
                  />
                </svg>
                <div className="absolute flex flex-col items-center">
                  <span className="text-3xl font-extrabold text-white">{data.cci}%</span>
                  <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Index</span>
                </div>
              </div>
            </div>

            {/* OPS Gauge */}
            <div className="glass-panel flex flex-col items-center justify-center text-center p-4">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Surge Outstroke (OPS)</span>
              <div className="relative flex items-center justify-center w-28 h-28">
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="56" cy="56" r="48" stroke="#1e293b" strokeWidth="6" fill="transparent" />
                  <circle 
                    cx="56" 
                    cy="56" 
                    r="48" 
                    stroke="#818cf8" 
                    strokeWidth="8" 
                    fill="transparent" 
                    strokeDasharray={301.6}
                    strokeDashoffset={301.6 - (301.6 * data.ops) / 100}
                    className="transition-all duration-500"
                  />
                </svg>
                <div className="absolute flex flex-col items-center">
                  <span className="text-3xl font-extrabold text-white">{data.ops}%</span>
                  <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Probability</span>
                </div>
              </div>
            </div>
          </div>

          {/* Micro Telemetry Details */}
          <div className="glass-panel grid grid-cols-2 gap-4 p-4">
            <div className="flex items-center gap-3">
              <span className="bg-slate-900 border border-slate-800 p-2 rounded text-slate-400">
                <Users className="w-4 h-4" />
              </span>
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Person Count</p>
                <p className="text-lg font-bold text-white">{data.person_count}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="bg-slate-900 border border-slate-800 p-2 rounded text-slate-400">
                <Zap className="w-4 h-4 text-violet-400" />
              </span>
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Phase Index (PSI)</p>
                <p className="text-lg font-bold text-white">{data.psi}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="bg-slate-900 border border-slate-800 p-2 rounded text-slate-400">
                <Volume2 className="w-4 h-4 text-emerald-400" />
              </span>
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Audio DB</p>
                <p className="text-lg font-bold text-white">{data.decibel} dB</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="bg-slate-900 border border-slate-800 p-2 rounded text-slate-400">
                <Activity className="w-4 h-4 text-amber-400" />
              </span>
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Acoustic Stress</p>
                <p className="text-lg font-bold text-white">{data.stress_pitch_drift}</p>
              </div>
            </div>
          </div>

          {/* Anticipatory Dispatch Center */}
          <div className="glass-panel">
            <h3 className="text-md font-bold text-white mb-3 flex items-center gap-2">
              <HeartHandshake className="w-4 h-4 text-indigo-400" />
              Anticipatory Dispatch Controls
            </h3>
            <p className="text-slate-400 text-xs mb-4">
              Inject alerts to test cascade scripts and response agency routing.
            </p>
            
            <div className="flex flex-wrap gap-3">
              <button 
                onClick={() => handleDispatch('YELLOW')}
                disabled={demoTriggering}
                className="flex-1 px-3 py-2 rounded bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 font-bold text-xs hover:bg-yellow-500/20"
              >
                TEST WARNING
              </button>
              <button 
                onClick={() => handleDispatch('ORANGE')}
                disabled={demoTriggering}
                className="flex-1 px-3 py-2 rounded bg-orange-500/10 border border-orange-500/30 text-orange-400 font-bold text-xs hover:bg-orange-500/20"
              >
                TEST SERIOUS
              </button>
              <button 
                onClick={() => handleDispatch('RED')}
                disabled={demoTriggering}
                className="flex-1 px-3 py-2 rounded bg-red-500/10 border border-red-500/30 text-red-400 font-bold text-xs hover:bg-red-500/20"
              >
                TEST CRITICAL
              </button>
            </div>
            
            {/* Active Dispatches List */}
            <div className="mt-4 pt-4 border-t border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                <Navigation className="w-3.5 h-3.5 text-indigo-400" />
                Active Responses
              </h4>
              <div className="space-y-3 max-h-[140px] overflow-y-auto">
                {data.dispatches.map((d, index) => (
                  <div key={index} className="bg-slate-900/60 border border-slate-800 rounded p-2.5 text-xs">
                    <div className="flex justify-between font-bold mb-1">
                      <span className="text-slate-200">{d.dispatch_id}</span>
                      <span className={`px-1.5 py-0.5 rounded text-[9px] uppercase ${
                        d.alert_level === 'RED' ? 'bg-red-500/20 text-red-400' : 'bg-orange-500/20 text-orange-400'
                      }`}>
                        {d.alert_level}
                      </span>
                    </div>
                    <div className="grid grid-cols-3 text-slate-400 gap-1 text-[10px]">
                      <span>👮 Police: {d.allocated_police_units}</span>
                      <span>🚑 Medics: {d.allocated_medical_units}</span>
                      <span>🚒 Fire: {d.allocated_fire_units}</span>
                    </div>
                    <p className="text-[9px] text-slate-500 mt-1">
                      Target: {d.triage_zone.lat.toFixed(4)}N, {d.triage_zone.lng.toFixed(4)}E | Hospitals: {d.notified_hospitals.join(', ')}
                    </p>
                  </div>
                ))}
                {data.dispatches.length === 0 && (
                  <p className="text-slate-500 text-center text-xs py-2">No active dispatches. System idle.</p>
                )}
              </div>
            </div>
          </div>

          {/* Alarm History & Causal Analysis */}
          <div className="glass-panel flex-1">
            <h3 className="text-md font-bold text-white mb-3 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-indigo-400" />
              Intelligence Broadcast Logs
            </h3>
            <div className="space-y-2.5 max-h-[180px] overflow-y-auto pr-1">
              {data.recent_alerts.map((a, i) => (
                <div key={i} className="flex gap-2.5 text-xs text-left">
                  <span className="text-slate-500 font-mono select-none">{a.timestamp}</span>
                  <p className="text-slate-300">
                    <span className={`font-semibold mr-1.5 ${
                      a.level === 'RED' ? 'text-red-400' : a.level === 'ORANGE' ? 'text-orange-400' : 'text-amber-400'
                    }`}>
                      [{a.level}]
                    </span>
                    {a.message}
                  </p>
                </div>
              ))}
              {data.recent_alerts.length === 0 && (
                <p className="text-slate-500 text-xs py-2 text-center">Awaiting log streams...</p>
              )}
            </div>
          </div>

        </section>
      </main>

      {/* Footer */}
      <footer className="mt-8 pt-6 border-t border-slate-800/80 flex flex-col md:flex-row justify-between items-center text-xs text-slate-500 gap-4">
        <p>© 2026 PRECIS & NEURAL-SHIELD R&D Consortium. Government-Grade Crowd Safety Systems.</p>
        <p className="flex items-center gap-1.5 font-mono">
          <Cpu className="w-3.5 h-3.5 text-indigo-500" />
          FPGA Edge Nodes Connected: 12/12
        </p>
      </footer>
    </div>
  );
}
