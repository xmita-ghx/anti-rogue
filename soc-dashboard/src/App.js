import React, { useState, useEffect, useCallback, useMemo } from "react";
import TrafficChart from "./components/TrafficChart";
import AgentsTable from "./components/AgentsTable";
import AlertsPanel from "./components/AlertsPanel";
import LogsPanel from "./components/LogsPanel";

function getRandomTraffic(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getTimestamp() {
  const now = new Date();
  return now.toLocaleTimeString("en-US", { hour12: false });
}

function App() {
  const [trafficData, setTrafficData] = useState(() => {
    const initial = [];
    for (let i = 0; i < 20; i += 1) {
      initial.push(getRandomTraffic(50, 120));
    }
    return initial;
  });

  const [agents, setAgents] = useState([
    { id: "A12", status: "Active", apiCalls: 45, permissions: "User" },
    { id: "A17", status: "Active", apiCalls: 50, permissions: "User" },
    { id: "A24", status: "Active", apiCalls: 48, permissions: "User" },
  ]);

  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([
    { timestamp: getTimestamp(), message: "System monitoring started." },
    { timestamp: getTimestamp(), message: "Monitoring system active" },
  ]);
  const [sentinelAlert, setSentinelAlert] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTrafficData((prev) => {
        const nextValue = getRandomTraffic(50, 120);
        const updated = [...prev, nextValue];
        if (updated.length > 20) {
          return updated.slice(updated.length - 20);
        }
        return updated;
      });
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const triggerRogueAgent = useCallback(() => {
    const ts = getTimestamp();

    setAgents((prevAgents) =>
      prevAgents.map((agent) =>
        agent.id === "A17"
          ? { ...agent, status: "Suspicious", apiCalls: 1200, permissions: "Admin" }
          : agent
      )
    );

    setAlerts((prevAlerts) => [
      ...prevAlerts,
      {
        severity: "critical",
        message: "Suspicious AI agent activity detected: A17",
        timestamp: ts,
      },
      {
        severity: "warning",
        message: "Agent A17 privilege escalation to Admin",
        timestamp: ts,
      },
    ]);

    setLogs((prevLogs) => [
      { timestamp: ts, message: "Agent A17 privilege escalation detected" },
      { timestamp: ts, message: "Abnormal API traffic spike detected" },
      { timestamp: ts, message: "API traffic anomaly detected" },
      ...prevLogs,
    ]);

    setTrafficData(() => {
      const spikeData = [];
      for (let i = 0; i < 20; i += 1) {
        spikeData.push(getRandomTraffic(300, 600));
      }
      return spikeData;
    });
  }, []);

  const handleDisableAgent = useCallback((agentId) => {
    const ts = getTimestamp();

    setAgents((prevAgents) =>
      prevAgents.map((agent) =>
        agent.id === agentId
          ? { ...agent, status: "Disabled", apiCalls: 0, permissions: "None" }
          : agent
      )
    );

    setLogs((prevLogs) => [
      { timestamp: ts, message: `Agent ${agentId} has been quarantined by Sentinel AI.` },
      ...prevLogs,
    ]);

    setAlerts((prevAlerts) => [
      ...prevAlerts,
      {
        severity: "warning",
        message: `Agent ${agentId} disabled due to suspicious activity.`,
        timestamp: ts,
      },
    ]);
  }, []);

  const startSentinelAlert = useCallback(() => {
    const ts = getTimestamp();

    // Trigger the rogue agent scenario
    triggerRogueAgent();

    // Show the sentinel alert banner
    setSentinelAlert(true);

    // Add sentinel monitoring log entry
    setLogs((prevLogs) => [
      { timestamp: ts, message: "SENTINEL monitoring detected critical threat" },
      ...prevLogs,
    ]);
  }, [triggerRogueAgent]);

  useEffect(() => {
    window.triggerRogueAgent = triggerRogueAgent;
    window.startSentinelAlert = startSentinelAlert;
    return () => {
      if (window.triggerRogueAgent === triggerRogueAgent) {
        delete window.triggerRogueAgent;
      }
      if (window.startSentinelAlert === startSentinelAlert) {
        delete window.startSentinelAlert;
      }
    };
  }, [triggerRogueAgent, startSentinelAlert]);

  // Derived metrics
  const activeAgentCount = agents.filter((a) => a.status === "Active").length;
  const alertCount = alerts.length;
  const avgTraffic = Math.round(
    trafficData.reduce((sum, v) => sum + v, 0) / trafficData.length
  );

  const threatLevel = useMemo(() => {
    const hasCriticalAlert = alerts.some((a) => a.severity === "critical");
    const hasSuspiciousAgent = agents.some((a) => a.status === "Suspicious");
    const highTraffic = avgTraffic > 200;

    if (hasCriticalAlert || hasSuspiciousAgent) return "Critical";
    if (highTraffic || alertCount > 0) return "Elevated";
    return "Normal";
  }, [alerts, agents, avgTraffic, alertCount]);

  const threatColor = {
    Normal: "text-soc-normal",
    Elevated: "text-soc-warning",
    Critical: "text-soc-critical",
  }[threatLevel];

  const threatBg = {
    Normal: "bg-soc-normal-dim",
    Elevated: "bg-soc-warning-dim",
    Critical: "bg-soc-critical-dim",
  }[threatLevel];

  const threatDot = {
    Normal: "bg-soc-normal",
    Elevated: "bg-soc-warning",
    Critical: "bg-soc-critical",
  }[threatLevel];

  return (
    <div className="min-h-screen bg-soc-bg text-soc-text">
      {/* ─── HEADER ─── */}
      <header className="border-b border-soc-border bg-soc-panel/60 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-wide text-soc-text flex items-center gap-3">
              <span className="text-soc-accent">◈</span>
              Sentinel AI Security Operations Center
            </h1>
            <p className="text-soc-text-dim mt-1 text-sm sm:text-base tracking-wider uppercase">
              Autonomous AI Threat Monitoring
            </p>
          </div>
          <div className="flex items-center gap-3 bg-soc-normal-dim border border-soc-normal/30 rounded-lg px-4 py-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-soc-normal opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-soc-normal"></span>
            </span>
            <span className="text-soc-normal font-semibold text-sm tracking-wide">
              SYSTEM ONLINE
            </span>
          </div>
        </div>
      </header>

      {/* ─── SENTINEL ALERT BANNER ─── */}
      {sentinelAlert && (
        <div className="sentinel-alert-banner bg-soc-critical/20 border-b-2 border-soc-critical">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center gap-4">
            <span className="text-3xl animate-pulse">⚠</span>
            <div>
              <h2 className="text-xl font-bold text-soc-critical tracking-wide">
                SENTINEL ALERT
              </h2>
              <p className="text-soc-text text-sm mt-0.5">
                Critical threat detected — Agent A17 suspicious activity
              </p>
            </div>
            <button
              type="button"
              className="ml-auto text-soc-text-dim hover:text-soc-text text-lg px-2"
              onClick={() => setSentinelAlert(false)}
              aria-label="Dismiss alert"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* ─── METRICS ROW ─── */}
        <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Active Agents */}
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-soc-text-dim text-xs uppercase tracking-wider font-medium">Active Agents</span>
              <span className="text-soc-accent text-lg">⬡</span>
            </div>
            <p className="text-3xl font-bold text-soc-text">{activeAgentCount}</p>
            <p className="text-soc-text-dim text-xs mt-1">{agents.length} total registered</p>
          </div>

          {/* Security Alerts */}
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-soc-text-dim text-xs uppercase tracking-wider font-medium">Security Alerts</span>
              <span className="text-soc-warning text-lg">⚠</span>
            </div>
            <p className={`text-3xl font-bold ${alertCount > 0 ? 'text-soc-critical' : 'text-soc-text'}`}>
              {alertCount}
            </p>
            <p className="text-soc-text-dim text-xs mt-1">
              {alertCount === 0 ? "All clear" : "Requires attention"}
            </p>
          </div>

          {/* API Requests/sec */}
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-soc-text-dim text-xs uppercase tracking-wider font-medium">API Requests/sec</span>
              <span className="text-soc-accent text-lg">⟐</span>
            </div>
            <p className={`text-3xl font-bold ${avgTraffic > 200 ? 'text-soc-critical' : 'text-soc-accent'}`}>
              {avgTraffic}
            </p>
            <p className="text-soc-text-dim text-xs mt-1">
              {avgTraffic > 200 ? "Anomalous traffic" : "Normal range"}
            </p>
          </div>

          {/* Threat Level */}
          <div className={`metric-card ${threatBg} border-${threatLevel === 'Critical' ? 'soc-critical' : threatLevel === 'Elevated' ? 'soc-warning' : 'soc-border'}/30`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-soc-text-dim text-xs uppercase tracking-wider font-medium">Threat Level</span>
              <span className={`h-2.5 w-2.5 rounded-full ${threatDot} ${threatLevel === 'Critical' ? 'animate-pulse' : ''}`}></span>
            </div>
            <p className={`text-3xl font-bold uppercase tracking-wider ${threatColor}`}>
              {threatLevel}
            </p>
            <p className="text-soc-text-dim text-xs mt-1">
              {threatLevel === 'Normal' ? 'No threats detected' : threatLevel === 'Elevated' ? 'Monitoring closely' : 'Immediate action needed'}
            </p>
          </div>
        </section>

        {/* ─── TRAFFIC + ALERTS ROW ─── */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 soc-panel">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-soc-text flex items-center gap-2">
                <span className="text-soc-accent">▸</span>
                Real-Time API Traffic
              </h2>
              <span className="text-xs text-soc-text-dim bg-soc-bg rounded-md px-2 py-1">
                LIVE
                <span className="inline-block w-1.5 h-1.5 bg-soc-critical rounded-full ml-1.5 animate-pulse"></span>
              </span>
            </div>
            <TrafficChart dataPoints={trafficData} />
          </div>

          <div className="lg:col-span-1">
            <AlertsPanel alerts={alerts} />
          </div>
        </section>

        {/* ─── AGENTS TABLE ─── */}
        <section>
          <AgentsTable agents={agents} onDisableAgent={handleDisableAgent} />
        </section>

        {/* ─── SYSTEM LOGS ─── */}
        <section>
          <LogsPanel logs={logs} />
        </section>
      </main>

      {/* ─── FOOTER ─── */}
      <footer className="border-t border-soc-border mt-8 py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between text-xs text-soc-text-dim">
          <span>Sentinel AI SOC v2.0</span>
          <span>© 2026 Sentinel Security Systems</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
