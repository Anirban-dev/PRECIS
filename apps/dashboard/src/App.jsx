import React, { useState, useEffect, useRef } from 'react';
import {
  Activity, Shield, AlertTriangle, AlertCircle, RefreshCw,
  MapPin, Eye, Volume2, Users, Radio, Navigation,
  Zap, HeartHandshake, ShieldAlert, Cpu, Mic, Camera, Sliders, Play, Settings, Send, Bell
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

  // Interactive Simulator State
  const [selectedSensorType, setSelectedSensorType] = useState('yolo'); // 'yolo' or 'audio'
  const [simCameraId, setSimCameraId] = useState('CAM-01');
  const [simSensorId, setSimSensorId] = useState('MIC-01');

  // YOLO Sliders
  const [simPersonCount, setSimPersonCount] = useState(84);
  const [simDivergence, setSimDivergence] = useState(0.8);
  const [simVelocity, setSimVelocity] = useState(0.5);

  // Audio Sliders
  const [simDecibel, setSimDecibel] = useState(54.2);
  const [simStressDrift, setSimStressDrift] = useState(0.02);
  const [simScreaming, setSimScreaming] = useState(false);

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

  // Sync simulator sliders with actual incoming data
  useEffect(() => {
    if (wsStatus === 'CONNECTED') {
      setSimPersonCount(data.person_count);
      setSimDivergence(data.psi * 10.0);
      setSimDecibel(data.decibel);
      setSimStressDrift(data.stress_pitch_drift);
      setSimScreaming(data.screaming);
    }
  }, [data, wsStatus]);

  // Keep a running timeline chart in state
  useEffect(() => {
    setChartData(prev => {
      const updated = [...prev, { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), cci: data.cci, ops: data.ops }];
      if (updated.length > 20) updated.shift();
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
    for (let i = 0; i < 50; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        color: 'hsla(250, 89%, 65%, 0.4)'
      });
    }

    function render() {
      ctx.fillStyle = 'rgba(8, 11, 21, 0.15)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw grid lines representing optical flow mesh
      ctx.strokeStyle = 'rgba(99, 102, 241, 0.04)';
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
      const scale = data.psi * 12; // Higher PSI = higher speed vectors
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
        ctx.fillStyle = data.alarm_level === 'RED' ? 'rgba(239, 68, 68, 0.7)' : data.alarm_level === 'ORANGE' ? 'rgba(249, 115, 22, 0.7)' : 'rgba(99, 102, 241, 0.7)';
        ctx.fill();

        // Vector line
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x + p.vx * 3.5, p.y + p.vy * 3.5);
        ctx.strokeStyle = data.alarm_level === 'RED' ? 'rgba(239, 68, 68, 0.35)' : data.alarm_level === 'ORANGE' ? 'rgba(249, 115, 22, 0.35)' : 'rgba(99, 102, 241, 0.35)';
        ctx.lineWidth = 1.5;
        ctx.stroke();
      });

      // Draw mock tracking bounding boxes
      ctx.strokeStyle = data.alarm_level === 'RED' ? 'rgba(239, 68, 68, 0.85)' : data.alarm_level === 'ORANGE' ? 'rgba(249, 115, 22, 0.85)' : 'rgba(34, 197, 94, 0.85)';
      ctx.lineWidth = 1.5;

      const boxes = [
        { x: 50, y: 60, w: 40, h: 80, label: 'TRK-242 (Dens)' },
        { x: 170, y: 120, w: 35, h: 75, label: 'TRK-105 (Turb)' },
        { x: 300, y: 50, w: 45, h: 90, label: 'TRK-089 (Reso)' }
      ];

      boxes.forEach(b => {
        // sway box slightly representing movement
        const sway = Math.sin(Date.now() / 250 + b.x) * (2 + data.psi * 20);
        ctx.strokeRect(b.x + sway, b.y, b.w, b.h);

        ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
        ctx.fillRect(b.x + sway, b.y - 16, 75, 16);

        ctx.fillStyle = '#fff';
        ctx.font = '500 8.5px Inter';
        ctx.fillText(b.label, b.x + sway + 4, b.y - 5);
      });

      // Draw shockwave center warning if RED
      if (data.alarm_level === 'RED') {
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, (Date.now() / 8) % 120, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.4)';
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
          triage_zone: { lat: 22.5726 + (Math.random() - 0.5) * 0.01, lng: 88.3639 + (Math.random() - 0.5) * 0.01 },
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
            { timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), message: `Anticipatory Dispatch triggered. Level: ${level}. Police: ${allocated_police}, Med: ${allocated_medical}.`, level },
            ...prev.recent_alerts
          ].slice(0, 15)
        }));
      }
    } catch (e) {
      console.error(e);
    }
    setDemoTriggering(false);
  };

  // POST manually adjusted data to Ingest endpoints
  const handleSendIngest = async () => {
    try {
      if (selectedSensorType === 'yolo') {
        const payload = {
          camera_id: simCameraId,
          person_count: parseInt(simPersonCount),
          mean_velocity_magnitude: parseFloat(simVelocity),
          flow_divergence: parseFloat(simDivergence)
        };

        if (wsStatus === 'CONNECTED') {
          await fetch('http://localhost:8000/api/ingest/yolo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else {
          // Simulate locally
          setData(prev => {
            const nextPsi = Math.min(1.0, Math.max(0.0, payload.flow_divergence / 10.0));
            const vocal_factor = prev.stress_pitch_drift * 100;
            const decibel_factor = Math.min(100.0, Math.max(0.0, (prev.decibel - 40) * 1.5));
            const computedCci = (nextPsi * 100 * 0.5) + (vocal_factor * 0.3) + ((prev.screaming ? Math.max(decibel_factor, 85.0) : decibel_factor) * 0.2);
            const finalCci = Math.min(100.0, Math.max(0.0, computedCci));
            const ops_base = 100 / (1 + Math.exp(-10 * (nextPsi - 0.5)));
            const ops = Math.min(100.0, Math.max(0.0, ops_base + (vocal_factor * 0.1)));
            const nextLvl = finalCci >= 80 ? 'RED' : finalCci >= 55 ? 'ORANGE' : finalCci >= 30 ? 'YELLOW' : 'GREEN';

            return {
              ...prev,
              person_count: payload.person_count,
              psi: parseFloat(nextPsi.toFixed(2)),
              cci: parseFloat(finalCci.toFixed(1)),
              ops: parseFloat(ops.toFixed(1)),
              alarm_level: nextLvl,
              recent_alerts: [
                { timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), message: `Standalone Ingest (YOLO): ${payload.camera_id} updated. Count: ${payload.person_count}, Div: ${payload.flow_divergence}`, level: nextLvl },
                ...prev.recent_alerts
              ].slice(0, 15)
            };
          });
        }
      } else {
        const payload = {
          sensor_id: simSensorId,
          decibel_level: parseFloat(simDecibel),
          stress_pitch_drift: parseFloat(simStressDrift),
          screaming_detected: simScreaming
        };

        if (wsStatus === 'CONNECTED') {
          await fetch('http://localhost:8000/api/ingest/audio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else {
          // Simulate locally
          setData(prev => {
            const vocal_factor = payload.stress_pitch_drift * 100;
            let decibel_factor = Math.min(100.0, Math.max(0.0, (payload.decibel_level - 40) * 1.5));
            if (payload.screaming_detected) {
              decibel_factor = Math.max(decibel_factor, 85.0);
            }
            const computedCci = (prev.psi * 100 * 0.5) + (vocal_factor * 0.3) + (decibel_factor * 0.2);
            const finalCci = Math.min(100.0, Math.max(0.0, computedCci));
            const ops_base = 100 / (1 + Math.exp(-10 * (prev.psi - 0.5)));
            const ops = Math.min(100.0, Math.max(0.0, ops_base + (vocal_factor * 0.1)));
            const nextLvl = finalCci >= 80 ? 'RED' : finalCci >= 55 ? 'ORANGE' : finalCci >= 30 ? 'YELLOW' : 'GREEN';

            return {
              ...prev,
              decibel: payload.decibel_level,
              stress_pitch_drift: payload.stress_pitch_drift,
              screaming: payload.screaming_detected,
              cci: parseFloat(finalCci.toFixed(1)),
              ops: parseFloat(ops.toFixed(1)),
              alarm_level: nextLvl,
              recent_alerts: [
                { timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), message: `Standalone Ingest (Audio): ${payload.sensor_id} updated. Amp: ${payload.decibel_level} dB, Scream: ${payload.screaming_detected ? "YES" : "NO"}`, level: nextLvl },
                ...prev.recent_alerts
              ].slice(0, 15)
            };
          });
        }
      }
    } catch (e) {
      console.error("Ingest failed:", e);
    }
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
          recent_alerts: [{ timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), message: "System status normalized. Monitoring active.", level: "GREEN" }]
        }));
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Color mapping utilities
  const getAlarmHex = (lvl) => {
    if (lvl === 'RED') return '#ef4444';
    if (lvl === 'ORANGE') return '#f97316';
    if (lvl === 'YELLOW') return '#f59e0b';
    return '#10b981';
  };

  const getAlarmGlowClass = (lvl) => {
    if (lvl === 'RED') return 'border-red-500/30 shadow-[0_0_15px_-3px_rgba(239,68,68,0.25)]';
    if (lvl === 'ORANGE') return 'border-orange-500/30 shadow-[0_0_15px_-3px_rgba(249,115,22,0.25)]';
    if (lvl === 'YELLOW') return 'border-yellow-500/30 shadow-[0_0_15px_-3px_rgba(245,158,11,0.25)]';
    return 'border-[#272f45] hover:border-indigo-500/30';
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#070913] text-[#e2e8f0] font-sans antialiased">

      {/* Top Banner / Glowing Grid Background Overlay */}
      <div className="absolute top-0 left-0 w-full h-[350px] bg-gradient-to-b from-[#11132e]/20 via-[#070913]/0 to-transparent pointer-events-none z-0" />

      {/* Dynamic Alarm Alert Banner */}
      {data.alarm_level === 'RED' && (
        <div className="bg-red-950/40 border-b border-red-500/30 text-red-200 text-xs px-4 py-2 flex items-center justify-between animate-pulse relative z-30">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-500" />
            <span className="font-semibold uppercase tracking-wide">Critical Threat Alert:</span>
            <span>Crowd Criticality is extreme ({data.cci}%). Crowd collapse probability is highly accelerated.</span>
          </div>
          <span className="bg-red-500 text-black px-2 py-0.5 rounded text-[10px] font-bold">CRITICAL</span>
        </div>
      )}

      {/* Main Header */}
      <header className="relative z-10 flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 px-6 md:px-8 py-5 border-b border-slate-900 bg-[#070913]/80 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <span className="bg-gradient-to-br from-indigo-500 to-violet-600 p-2.5 rounded-xl shadow-[0_0_15px_rgba(99,102,241,0.4)] text-white">
              <Shield className="w-6 h-6" />
            </span>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-extrabold text-white tracking-tight font-display">PRECIS</h1>
                <span className="bg-[#141b35] text-indigo-400 border border-indigo-500/20 px-2 py-0.5 rounded text-[10px] font-bold tracking-wider">CRIS v3</span>
              </div>
              <p className="text-slate-400 text-xs tracking-wider uppercase font-semibold mt-0.5">Government-Grade Crowd Resonance & Intelligence System</p>
            </div>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex flex-wrap items-center gap-3">

          {/* Audio Scream Status Alert (CRITICAL EXTRA VISIBILITY) */}
          {data.screaming && (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-bold animate-bounce shadow-[0_0_15px_rgba(239,68,68,0.2)]">
              <Bell className="w-3.5 h-3.5 animate-ring" />
              SCREAM DETECTED
            </div>
          )}

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0f1224] border border-[#23294c]">
            <span className={`pulse-indicator ${data.alarm_level.toLowerCase()}`} />
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">
              ALERT INDEX: <span style={{ color: getAlarmHex(data.alarm_level) }}>{data.alarm_level}</span>
            </span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0f1224] border border-[#23294c]">
            <Radio className={`w-4 h-4 ${wsStatus === 'CONNECTED' ? 'text-emerald-400 animate-pulse' : 'text-amber-500'}`} />
            <span className="text-xs font-semibold text-slate-300">
              GATEWAY: {wsStatus === 'CONNECTED' ? 'LIVE' : simMode ? 'STANDALONE (SIM)' : 'OFFLINE'}
            </span>
          </div>

          <button
            onClick={handleReset}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-[#0f1224] hover:bg-[#181d3d] border border-[#23294c] hover:border-indigo-500/30 text-slate-300 text-xs font-bold transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            RESET DEMO
          </button>
        </div>
      </header>

      {/* Main Responsive Grid Layout */}
      <main className="relative z-10 flex-1 grid grid-cols-12 gap-6 p-6 md:p-8">

        {/* LEFT COLUMN: Map, Simulation Stream, Optical Flow (Col-span 7) */}
        <section className="col-span-12 xl:col-span-7 flex flex-col gap-6">

          {/* CCTV Feed with Integrated Optical Flow and Vector Overlays */}
          <div className={`glass-panel relative overflow-hidden h-[380px] flex flex-col justify-between transition-all duration-300 border ${getAlarmGlowClass(data.alarm_level)}`}>
            {/* Live canvas for computer vision overlay */}
            <canvas
              ref={canvasRef}
              width={640}
              height={360}
              className="absolute inset-0 w-full h-full object-cover z-10 opacity-70"
            />

            {/* Dark background layout layer */}
            <div className="absolute inset-0 bg-gradient-to-t from-[#080b15] via-transparent to-transparent pointer-events-none z-0" />

            {/* Top Overlay HUD */}
            <div className="relative z-20 flex justify-between items-start">
              <span className="flex items-center gap-2 px-2.5 py-1.5 rounded bg-black/75 border border-[#272f45]/60 text-[10px] uppercase font-bold tracking-wider text-slate-300">
                <Eye className="w-3.5 h-3.5 text-indigo-400" />
                LIVE COGNITIVE CV FEED — CAM-01 (Gate B Entrance)
              </span>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-red-600 text-[9px] font-bold text-white tracking-widest uppercase animate-pulse">
                  REC
                </span>
              </div>
            </div>

            {/* Simulated Heatmap Zone overlays depending on Alarm Levels */}
            {data.alarm_level === 'RED' && (
              <div className="absolute top-[30%] left-[45%] w-32 h-32 bg-red-600/25 blur-3xl rounded-full animate-pulse z-15" />
            )}
            {data.alarm_level === 'ORANGE' && (
              <div className="absolute top-[35%] left-[40%] w-24 h-24 bg-orange-500/20 blur-2xl rounded-full animate-pulse z-15" />
            )}

            {/* Bottom Overlay HUD */}
            <div className="relative z-20 flex justify-between items-end mt-auto">
              <div className="flex flex-col gap-1.5 text-left bg-black/75 p-3 rounded-lg border border-[#272f45]/50">
                <div className="text-[9px] font-bold tracking-widest text-[#6366f1] uppercase">CV SPECTRAL METRICS:</div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-slate-300 font-mono text-[10px]">
                  <span>Sway Scale: <span className="text-white font-bold">{(data.psi * 20).toFixed(1)} mm</span></span>
                  <span>Spatial Freq: <span className="text-white font-bold">{(0.6 + data.psi * 0.8).toFixed(2)} Hz</span></span>
                  <span>Density Load: <span className="text-white font-bold">{(data.person_count / 140).toFixed(2)} p/m²</span></span>
                  <span>Coherence: <span className="text-white font-bold">{(1.0 - data.psi * 0.6).toFixed(2)}</span></span>
                </div>
              </div>
              <div className="text-right text-[10px] font-mono text-slate-400 bg-black/75 p-3 rounded-lg border border-[#272f45]/50 flex flex-col gap-0.5">
                <span className="text-slate-500 uppercase tracking-widest text-[9px] font-bold">TIMESTAMP</span>
                <span>{new Date().toISOString()}</span>
              </div>
            </div>
          </div>

          {/* Interactive Map Visualizer (Aesthetic Stadium Blueprint) */}
          <div className="glass-panel relative flex flex-col min-h-[220px] p-5">
            <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center gap-2">
              <MapPin className="w-4 h-4 text-indigo-400" />
              Spatio-Temporal Tactical Map (Stadium Zone B)
            </h3>

            {/* Map Canvas Background Vector Blueprint */}
            <div className="relative flex-1 rounded-xl bg-[#0a0d1d] border border-[#272f45]/40 overflow-hidden flex items-center justify-center p-2 min-h-[140px]">

              {/* Concentric grid rings representing stadium */}
              <div className="absolute w-[90%] h-[90%] border border-dashed border-indigo-500/5 rounded-full" />
              <div className="absolute w-[60%] h-[60%] border border-dashed border-indigo-500/5 rounded-full" />
              <div className="absolute w-[30%] h-[30%] border border-dashed border-indigo-500/5 rounded-full" />
              <div className="absolute top-0 bottom-0 left-1/2 w-0 border-l border-indigo-500/5" />
              <div className="absolute left-0 right-0 top-1/2 h-0 border-t border-indigo-500/5" />

              {/* Cameras & Sensors Indicators */}
              <div className="absolute top-[20%] left-[25%] flex flex-col items-center group pointer-events-auto cursor-pointer">
                <Camera className="w-4 h-4 text-indigo-400 hover:scale-125 transition-transform" />
                <span className="text-[8px] font-mono mt-0.5 bg-slate-950 px-1 border border-indigo-500/20 rounded">CAM-01</span>
              </div>

              <div className="absolute top-[40%] right-[25%] flex flex-col items-center group pointer-events-auto cursor-pointer">
                <Camera className="w-4 h-4 text-indigo-400 hover:scale-125 transition-transform" />
                <span className="text-[8px] font-mono mt-0.5 bg-slate-950 px-1 border border-indigo-500/20 rounded">CAM-02</span>
              </div>

              <div className="absolute bottom-[20%] left-[55%] flex flex-col items-center group pointer-events-auto cursor-pointer">
                <Camera className="w-4 h-4 text-indigo-400 hover:scale-125 transition-transform" />
                <span className="text-[8px] font-mono mt-0.5 bg-slate-950 px-1 border border-indigo-500/20 rounded">CAM-03</span>
              </div>

              <div className="absolute top-[60%] left-[15%] flex flex-col items-center group pointer-events-auto cursor-pointer">
                <Mic className="w-4 h-4 text-emerald-400 hover:scale-125 transition-transform" />
                <span className="text-[8px] font-mono mt-0.5 bg-slate-950 px-1 border-emerald-500/20 rounded">MIC-01</span>
              </div>

              <div className="absolute bottom-[40%] right-[10%] flex flex-col items-center group pointer-events-auto cursor-pointer">
                <Mic className="w-4 h-4 text-emerald-400 hover:scale-125 transition-transform" />
                <span className="text-[8px] font-mono mt-0.5 bg-slate-950 px-1 border-emerald-500/20 rounded">MIC-02</span>
              </div>

              {/* Triage/Dispatches Pin */}
              {data.dispatches.map((d, index) => {
                const latOffset = (d.triage_zone.lat - 22.5726) * 5000;
                const lngOffset = (d.triage_zone.lng - 88.3639) * 5000;

                const topPct = 50 + Math.max(-45, Math.min(45, latOffset));
                const leftPct = 50 + Math.max(-45, Math.min(45, lngOffset));

                return (
                  <div
                    key={d.dispatch_id}
                    className="absolute flex flex-col items-center z-20 pointer-events-auto"
                    style={{ top: `${topPct}%`, left: `${leftPct}%` }}
                  >
                    <div className="relative">
                      <MapPin className="w-5 h-5 text-red-500 animate-bounce" />
                      <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full animate-ping" />
                    </div>
                    <span className="text-[8px] font-mono font-bold bg-slate-950 border border-red-500/30 text-red-400 px-1 py-0.5 rounded shadow shadow-red-500/20 mt-0.5">
                      {d.dispatch_id.split('-')[0]}-{d.dispatch_id.split('-')[1]}
                    </span>
                  </div>
                );
              })}

              {/* General warning zones (if high PSI) */}
              {data.psi >= 0.4 && (
                <div
                  className="absolute w-20 h-20 rounded-full bg-yellow-500/10 border border-yellow-500/30 blur-sm animate-pulse z-10"
                  style={{ top: '40%', left: '35%' }}
                />
              )}
              {data.psi >= 0.8 && (
                <div
                  className="absolute w-28 h-28 rounded-full bg-red-500/15 border border-red-500/30 blur-sm animate-pulse z-10"
                  style={{ top: '35%', left: '30%' }}
                />
              )}

              {/* Legend overlay */}
              <div className="absolute bottom-2 left-2 flex gap-3 text-[8.5px] font-semibold text-slate-400 bg-slate-950/80 p-1.5 rounded-lg border border-[#272f45]/50 pointer-events-none">
                <span className="flex items-center gap-1"><Camera className="w-2.5 h-2.5 text-indigo-400" /> Cameras</span>
                <span className="flex items-center gap-1"><Mic className="w-2.5 h-2.5 text-emerald-400" /> Sound</span>
                <span className="flex items-center gap-1"><MapPin className="w-2.5 h-2.5 text-red-500 animate-pulse" /> Active Dispatches</span>
              </div>
            </div>
          </div>

          {/* Real-time Timeline Analytics Plot */}
          <div className="glass-panel flex flex-col p-5">
            <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-indigo-400" />
              Criticality (CCI) & Outstroke Surge (OPS) Temporal Streams
            </h3>

            <div className="h-[140px] w-full flex items-end gap-1 border-b border-l border-slate-800 pb-2 pl-2 relative">

              {/* Y-Axis guide lines */}
              <div className="absolute w-full h-[1px] bg-slate-900 border-t border-dashed border-slate-800/60" style={{ bottom: '80%' }} />
              <div className="absolute w-full h-[1px] bg-slate-900 border-t border-dashed border-slate-800/60" style={{ bottom: '50%' }} />
              <div className="absolute w-full h-[1px] bg-slate-900 border-t border-dashed border-slate-800/60" style={{ bottom: '20%' }} />

              {chartData.map((d, i) => (
                <div key={i} className="flex-1 flex gap-[2px] items-end h-full group relative">

                  {/* CCI Bar */}
                  <div
                    className="flex-1 rounded-t-sm transition-all duration-300"
                    style={{
                      height: `${d.cci}%`,
                      background: `linear-gradient(to top, rgba(99, 102, 241, 0.2), ${getAlarmHex(data.alarm_level)})`
                    }}
                  />
                  {/* OPS Bar */}
                  <div
                    className="flex-1 rounded-t-sm transition-all duration-300"
                    style={{
                      height: `${d.ops}%`,
                      background: `linear-gradient(to top, rgba(129, 140, 248, 0.1), #6366f1)`
                    }}
                  />

                  {/* Tooltip on hover */}
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block bg-[#0e111d] border border-[#272f45] p-2 rounded-lg text-[9px] shadow-xl whitespace-nowrap z-50">
                    <p className="text-white font-bold flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: getAlarmHex(data.alarm_level) }}></span>
                      CCI: {d.cci}%
                    </p>
                    <p className="text-[#6366f1] font-bold flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#6366f1]"></span>
                      OPS: {d.ops}%
                    </p>
                    <p className="text-slate-500 font-mono mt-0.5">{d.time}</p>
                  </div>
                </div>
              ))}

              {chartData.length === 0 && (
                <div className="w-full h-full flex items-center justify-center text-slate-500 text-xs">
                  Awaiting system telemetry frames...
                </div>
              )}
            </div>

            <div className="flex justify-between items-center text-[9px] font-bold text-slate-500 mt-2.5 uppercase tracking-wider">
              <span>-20 Live Frames</span>
              <div className="flex gap-4">
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-indigo-500"></span> CCI Trend</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-indigo-400"></span> OPS Trend</span>
              </div>
              <span>Real-time Ingest Tick</span>
            </div>
          </div>

        </section>

        {/* RIGHT COLUMN: Gauges, Simulator Deck, Dispatches, Logs (Col-span 5) */}
        <section className="col-span-12 xl:col-span-5 flex flex-col gap-6">

          {/* Key Analytics Gauges */}
          <div className="grid grid-cols-2 gap-4">

            {/* CCI Gauge */}
            <div className={`glass-panel flex flex-col items-center justify-center text-center p-5 border ${getAlarmGlowClass(data.alarm_level)}`}>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5 text-indigo-400" />
                Crowd Criticality (CCI)
              </span>
              <div className="relative flex items-center justify-center w-28 h-28">
                {/* SVG circular track */}
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="56" cy="56" r="46" stroke="#161a35" strokeWidth="5" fill="transparent" />
                  <circle
                    cx="56"
                    cy="56"
                    r="46"
                    stroke={getAlarmHex(data.alarm_level)}
                    strokeWidth="7"
                    fill="transparent"
                    strokeDasharray={289.0}
                    strokeDashoffset={289.0 - (289.0 * data.cci) / 100}
                    className="transition-all duration-500"
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute flex flex-col items-center">
                  <span className="text-3xl font-black text-white">{data.cci}%</span>
                  <span className="text-[8.5px] uppercase font-bold text-slate-400 tracking-widest mt-0.5">INDEX SCORE</span>
                </div>
              </div>
            </div>

            {/* OPS Gauge */}
            <div className={`glass-panel flex flex-col items-center justify-center text-center p-5 border ${getAlarmGlowClass(data.alarm_level)}`}>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-indigo-400" />
                Surge Outstroke (OPS)
              </span>
              <div className="relative flex items-center justify-center w-28 h-28">
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="56" cy="56" r="46" stroke="#161a35" strokeWidth="5" fill="transparent" />
                  <circle
                    cx="56"
                    cy="56"
                    r="46"
                    stroke="#818cf8"
                    strokeWidth="7"
                    fill="transparent"
                    strokeDasharray={289.0}
                    strokeDashoffset={289.0 - (289.0 * data.ops) / 100}
                    className="transition-all duration-500"
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute flex flex-col items-center">
                  <span className="text-3xl font-black text-white">{data.ops}%</span>
                  <span className="text-[8.5px] uppercase font-bold text-slate-400 tracking-widest mt-0.5">PROBABILITY</span>
                </div>
              </div>
            </div>
          </div>

          {/* Micro Telemetry Details */}
          <div className="glass-panel grid grid-cols-2 gap-4 p-4 border border-[#272f45]/50">
            <div className="flex items-center gap-3 bg-[#0f1224]/60 p-3 rounded-xl border border-[#23294c]/40 hover:border-indigo-500/20">
              <span className="bg-[#171a35] border border-[#23294c] p-2 rounded-lg text-indigo-400">
                <Users className="w-4 h-4" />
              </span>
              <div>
                <p className="text-[9px] font-bold uppercase tracking-wider text-slate-500">Person Count</p>
                <p className="text-base font-bold text-white font-mono">{data.person_count}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 bg-[#0f1224]/60 p-3 rounded-xl border border-[#23294c]/40 hover:border-indigo-500/20">
              <span className="bg-[#171a35] border border-[#23294c] p-2 rounded-lg text-violet-400">
                <Zap className="w-4 h-4 text-violet-400" />
              </span>
              <div>
                <p className="text-[9px] font-bold uppercase tracking-wider text-slate-500">Spatial PSI</p>
                <p className="text-base font-bold text-white font-mono">{data.psi}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 bg-[#0f1224]/60 p-3 rounded-xl border border-[#23294c]/40 hover:border-indigo-500/20">
              <span className="bg-[#171a35] border border-[#23294c] p-2 rounded-lg text-emerald-400">
                <Volume2 className="w-4 h-4 text-emerald-400" />
              </span>
              <div>
                <p className="text-[9px] font-bold uppercase tracking-wider text-slate-500">Acoustic dB</p>
                <p className="text-base font-bold text-white font-mono">{data.decibel} dB</p>
              </div>
            </div>

            <div className="flex items-center gap-3 bg-[#0f1224]/60 p-3 rounded-xl border border-[#23294c]/40 hover:border-indigo-500/20">
              <span className="bg-[#171a35] border border-[#23294c] p-2 rounded-lg text-amber-400">
                <Mic className="w-4 h-4 text-amber-400" />
              </span>
              <div>
                <p className="text-[9px] font-bold uppercase tracking-wider text-slate-500">Vocal Stress</p>
                <p className="text-base font-bold text-white font-mono">{data.stress_pitch_drift}</p>
              </div>
            </div>
          </div>

          {/* Interactive Ingest Sensor Simulator (operator control deck covering backend APIs) */}
          <div className="glass-panel border border-[#272f45]/50 flex flex-col p-5">
            <div className="flex items-center justify-between mb-3 pb-3 border-b border-slate-900">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Sliders className="w-4 h-4 text-indigo-400" />
                Interactive Telemetry Injector
              </h3>
              <span className="text-[8px] bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 font-bold px-2 py-0.5 rounded tracking-wide">
                OPERATOR CONTROLLER
              </span>
            </div>

            <p className="text-slate-400 text-[10.5px] leading-relaxed mb-4">
              Simulate dynamic sensor thresholds and ingest them directly into the PRECIS coordinator via gateway API routes.
            </p>

            {/* Ingest Selector Tabs */}
            <div className="flex gap-2 mb-4 bg-[#0a0d1d] p-1 rounded-lg border border-[#23294c]/40">
              <button
                onClick={() => setSelectedSensorType('yolo')}
                className={`flex-1 py-1.5 rounded-md text-[10px] uppercase font-bold tracking-wide transition-all ${selectedSensorType === 'yolo'
                  ? 'bg-[#1c2242] border border-indigo-500/20 text-white shadow'
                  : 'text-slate-400 hover:text-white'
                  }`}
              >
                🎥 YOLO Vision (Ingest)
              </button>
              <button
                onClick={() => setSelectedSensorType('audio')}
                className={`flex-1 py-1.5 rounded-md text-[10px] uppercase font-bold tracking-wide transition-all ${selectedSensorType === 'audio'
                  ? 'bg-[#1c2242] border border-indigo-500/20 text-white shadow'
                  : 'text-slate-400 hover:text-white'
                  }`}
              >
                🎤 Audio MIC (Ingest)
              </button>
            </div>

            {/* TAB 1: YOLO Vision Inputs */}
            {selectedSensorType === 'yolo' && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-[9px] font-bold text-slate-500 uppercase tracking-wide">Active Node</label>
                    <select
                      value={simCameraId}
                      onChange={(e) => setSimCameraId(e.target.value)}
                      className="w-full mt-1 bg-[#0f1224] border border-[#23294c] text-xs text-white rounded-lg p-2 focus:border-indigo-500/40"
                    >
                      <option value="CAM-01">CAM-01 (Stadium Zone B)</option>
                      <option value="CAM-02">CAM-02 (Gate A Entry)</option>
                      <option value="CAM-03">CAM-03 (VIP Suite Escalator)</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-[9px] font-bold text-slate-500 uppercase tracking-wide">Mean Velocity</label>
                    <div className="flex items-center gap-2 mt-1.5 bg-[#0f1224] px-2 py-1.5 border border-[#23294c] rounded-lg">
                      <Zap className="w-3 h-3 text-indigo-400" />
                      <span className="text-xs text-white font-mono font-bold">{simVelocity} m/s</span>
                    </div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-[10px] font-bold text-slate-400">Divergence Index (spatial spread)</span>
                    <span className="text-[10px] font-mono font-bold text-indigo-400">{simDivergence} PSI</span>
                  </div>
                  <input
                    type="range"
                    min="0.1"
                    max="10.0"
                    step="0.1"
                    value={simDivergence}
                    onChange={(e) => {
                      setSimDivergence(e.target.value);
                      // Update velocity dynamically based on divergence logic
                      setSimVelocity((parseFloat(e.target.value) * 0.2 + 0.3).toFixed(2));
                    }}
                    className="w-full h-1 bg-[#141830] rounded-lg appearance-none cursor-pointer accent-indigo-500"
                  />
                  <div className="flex justify-between text-[8px] font-bold text-slate-500 uppercase tracking-wider mt-1">
                    <span>Laminar Flow</span>
                    <span>Turbulent Surge</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-[10px] font-bold text-slate-400">Camera Crowd Headcount</span>
                    <span className="text-[10px] font-mono font-bold text-indigo-400">{simPersonCount} Persons</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="250"
                    value={simPersonCount}
                    onChange={(e) => setSimPersonCount(e.target.value)}
                    className="w-full h-1 bg-[#141830] rounded-lg appearance-none cursor-pointer accent-indigo-500"
                  />
                  <div className="flex justify-between text-[8px] font-bold text-slate-500 uppercase tracking-wider mt-1">
                    <span>Sparse</span>
                    <span>Extreme Density</span>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: Audio Mic Inputs */}
            {selectedSensorType === 'audio' && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-[9px] font-bold text-slate-500 uppercase tracking-wide">Audio Source</label>
                    <select
                      value={simSensorId}
                      onChange={(e) => setSimSensorId(e.target.value)}
                      className="w-full mt-1 bg-[#0f1224] border border-[#23294c] text-xs text-white rounded-lg p-2 focus:border-indigo-500/40"
                    >
                      <option value="MIC-01">MIC-01 (Stadium Zone B)</option>
                      <option value="MIC-02">MIC-02 (South Grandstand)</option>
                    </select>
                  </div>

                  {/* Screaming Toggle (Very important coverage) */}
                  <div>
                    <label className="text-[9px] font-bold text-slate-500 uppercase tracking-wide">Panic Signature</label>
                    <button
                      onClick={() => {
                        const nextScream = !simScreaming;
                        setSimScreaming(nextScream);
                        if (nextScream) {
                          setSimDecibel(92.4);
                          setSimStressDrift(0.85);
                        } else {
                          setSimDecibel(54.2);
                          setSimStressDrift(0.04);
                        }
                      }}
                      className={`w-full mt-1 py-1.5 border rounded-lg text-xs font-bold transition-all ${simScreaming
                        ? 'bg-red-500/10 border-red-500 text-red-400 shadow shadow-red-500/10'
                        : 'bg-[#0f1224] border-[#23294c] text-slate-400 hover:text-white'
                        }`}
                    >
                      {simScreaming ? '🚨 SCREAMING DETECTED' : '🔊 STABLE ACOUSTICS'}
                    </button>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-[10px] font-bold text-slate-400">Microphone DB Level</span>
                    <span className="text-[10px] font-mono font-bold text-emerald-400">{simDecibel} dB</span>
                  </div>
                  <input
                    type="range"
                    min="30.0"
                    max="115.0"
                    step="0.5"
                    value={simDecibel}
                    onChange={(e) => setSimDecibel(e.target.value)}
                    className="w-full h-1 bg-[#141830] rounded-lg appearance-none cursor-pointer accent-emerald-400"
                  />
                  <div className="flex justify-between text-[8px] font-bold text-slate-500 uppercase tracking-wider mt-1">
                    <span>Silent Ambient</span>
                    <span>High Amplitude Wave</span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-[10px] font-bold text-slate-400">Vocal Stress Factor (Pitch Drift)</span>
                    <span className="text-[10px] font-mono font-bold text-emerald-400">{simStressDrift} Index</span>
                  </div>
                  <input
                    type="range"
                    min="0.01"
                    max="1.00"
                    step="0.01"
                    value={simStressDrift}
                    onChange={(e) => setSimStressDrift(e.target.value)}
                    className="w-full h-1 bg-[#141830] rounded-lg appearance-none cursor-pointer accent-emerald-400"
                  />
                  <div className="flex justify-between text-[8px] font-bold text-slate-500 uppercase tracking-wider mt-1">
                    <span>Monotone Conversational</span>
                    <span>Acute Panic Vocal</span>
                  </div>
                </div>
              </div>
            )}

            {/* Send Ingestion trigger */}
            <button
              onClick={handleSendIngest}
              className="mt-4 w-full py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs uppercase tracking-wide flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/10 active:scale-[0.98] transition-all"
            >
              <Send className="w-3.5 h-3.5" />
              Ingest Simulated Telemetry
            </button>
          </div>

          {/* Anticipatory Dispatch Center */}
          <div className="glass-panel border border-[#272f45]/50 flex flex-col p-5">
            <div className="flex items-center justify-between mb-3 pb-3 border-b border-slate-900">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <HeartHandshake className="w-4 h-4 text-indigo-400" />
                Anticipatory Emergency Dispatch
              </h3>
              <span className="text-[8px] bg-red-500/10 border border-red-500/20 text-red-400 font-bold px-2 py-0.5 rounded tracking-wide">
                DEMO CONTROLS
              </span>
            </div>

            <p className="text-slate-400 text-[10.5px] leading-relaxed mb-4">
              Manually override crowd indices and dispatch units to demonstrate predictive emergency cascading logic.
            </p>

            <div className="flex flex-wrap gap-2.5">
              <button
                onClick={() => handleDispatch('YELLOW')}
                disabled={demoTriggering}
                className="flex-1 px-3 py-2 rounded-lg bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 font-bold text-[10px] uppercase tracking-wider transition-all disabled:opacity-50"
              >
                TEST WARNING
              </button>
              <button
                onClick={() => handleDispatch('ORANGE')}
                disabled={demoTriggering}
                className="flex-1 px-3 py-2 rounded-lg bg-orange-500/10 hover:bg-orange-500/20 border border-orange-500/30 text-orange-400 font-bold text-[10px] uppercase tracking-wider transition-all disabled:opacity-50"
              >
                TEST SERIOUS
              </button>
              <button
                onClick={() => handleDispatch('RED')}
                disabled={demoTriggering}
                className="flex-1 px-3 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 font-bold text-[10px] uppercase tracking-wider transition-all disabled:opacity-50 animate-pulse"
              >
                TEST CRITICAL
              </button>
            </div>

            {/* Active Dispatches List */}
            <div className="mt-5 pt-4 border-t border-slate-900">
              <h4 className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                <Navigation className="w-3.5 h-3.5 text-indigo-400" />
                Active Emergency Units Routing
              </h4>
              <div className="space-y-3 max-h-[160px] overflow-y-auto pr-1">
                {data.dispatches.map((d, index) => (
                  <div key={index} className="bg-[#0f1224]/80 border border-[#23294c]/60 rounded-xl p-3 text-xs shadow-sm hover:border-indigo-500/20 transition-all">
                    <div className="flex justify-between items-center font-bold mb-1.5">
                      <span className="text-white text-xs font-mono">{d.dispatch_id}</span>
                      <span className={`px-2 py-0.5 rounded text-[8.5px] uppercase font-bold ${d.alert_level === 'RED'
                        ? 'bg-red-500/10 border border-red-500/25 text-red-400'
                        : d.alert_level === 'ORANGE'
                          ? 'bg-orange-500/10 border border-orange-500/25 text-orange-400'
                          : 'bg-yellow-500/10 border border-yellow-500/25 text-yellow-400'
                        }`}>
                        {d.alert_level} ALERT
                      </span>
                    </div>
                    <div className="grid grid-cols-3 text-slate-300 gap-1.5 text-[10px] font-semibold font-mono bg-black/40 p-2 rounded-lg border border-[#23294c]/20 my-2">
                      <span className="flex items-center gap-1">👮 Police: <span className="text-white">{d.allocated_police_units}</span></span>
                      <span className="flex items-center gap-1">🚑 Medical: <span className="text-white">{d.allocated_medical_units}</span></span>
                      <span className="flex items-center gap-1">🚒 Fire: <span className="text-white">{d.allocated_fire_units}</span></span>
                    </div>
                    <div className="flex flex-col gap-0.5 text-[9px] text-slate-500 font-mono">
                      <span>Coordinates: <span className="text-slate-400">{d.triage_zone.lat.toFixed(6)}N, {d.triage_zone.lng.toFixed(6)}E</span></span>
                      <span>Hospitals alerted: <span className="text-indigo-400 font-semibold">{d.notified_hospitals.join(', ')}</span></span>
                    </div>
                  </div>
                ))}
                {data.dispatches.length === 0 && (
                  <p className="text-slate-500 text-center text-xs py-3 bg-[#0a0d1d]/40 rounded-xl border border-dashed border-[#23294c]/30">No active response cascades. Gateway idle.</p>
                )}
              </div>
            </div>
          </div>

          {/* Alarm History & Causal Analysis */}
          <div className="glass-panel border border-[#272f45]/50 flex-1 flex flex-col p-5">
            <h3 className="text-sm font-bold text-white mb-3 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-indigo-400" />
              Intelligence Broadcast Stream
            </h3>

            <div className="space-y-2.5 max-h-[140px] overflow-y-auto pr-1 flex-1 font-mono text-[10.5px]">
              {data.recent_alerts.map((a, i) => (
                <div key={i} className="flex gap-3 text-left border-b border-slate-900 pb-2 last:border-b-0 leading-relaxed">
                  <span className="text-slate-500 select-none font-bold whitespace-nowrap">{a.timestamp}</span>
                  <p className="text-slate-300">
                    <span className={`font-black mr-2 uppercase ${a.level === 'RED' ? 'text-red-400' : a.level === 'ORANGE' ? 'text-orange-400' : 'text-amber-400'
                      }`}>
                      [{a.level}]
                    </span>
                    {a.message}
                  </p>
                </div>
              ))}
              {data.recent_alerts.length === 0 && (
                <p className="text-slate-500 text-xs py-3 text-center">Awaiting central intelligence logs...</p>
              )}
            </div>
          </div>

        </section>
      </main>

      {/* Footer */}
      <footer className="relative z-10 mt-auto px-6 md:px-8 py-5 border-t border-slate-900 bg-[#070913]/90 flex flex-col md:flex-row justify-between items-center text-[10.5px] text-slate-500 gap-4">
        <p>© 2026 PRECIS & NEURAL-SHIELD R&D Consortium. Government-Grade Crowd Stability Operations.</p>
        <p className="flex items-center gap-2 font-semibold tracking-wide uppercase">
          <Cpu className="w-4 h-4 text-indigo-500" />
          Neural Processor Edge Nodes: <span className="text-emerald-400">12/12 ACTIVE</span>
        </p>
      </footer>
    </div>
  );
}
