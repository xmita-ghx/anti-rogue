import React from "react";

function LogsPanel({ logs }) {
  return (
    <div className="soc-panel">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-soc-text flex items-center gap-2">
          <span className="text-soc-accent">▸</span>
          System Event Log
        </h2>
        <span className="text-xs text-soc-text-dim bg-soc-bg rounded-md px-2 py-1">
          {logs.length} events
        </span>
      </div>

      <div className="max-h-64 overflow-y-auto rounded-lg bg-soc-bg/80 border border-soc-border/50">
        {logs.length === 0 && (
          <p className="text-sm text-soc-text-dim px-4 py-3 font-mono">
            No system events recorded.
          </p>
        )}

        {logs.map((log, index) => {
          const logObj =
            typeof log === "string"
              ? { timestamp: "", message: log }
              : log;

          // Detect keywords for color coding
          const isError =
            logObj.message.toLowerCase().includes("escalation") ||
            logObj.message.toLowerCase().includes("quarantine") ||
            logObj.message.toLowerCase().includes("spike") ||
            logObj.message.toLowerCase().includes("anomaly");
          const isSystem =
            logObj.message.toLowerCase().includes("monitoring") ||
            logObj.message.toLowerCase().includes("system") ||
            logObj.message.toLowerCase().includes("started");

          return (
            <div
              key={index}
              className={`log-entry flex items-start gap-3 px-4 py-2 text-xs font-mono border-b border-soc-border/30 last:border-b-0 ${isError
                  ? "text-soc-critical/90"
                  : isSystem
                    ? "text-soc-normal/80"
                    : "text-soc-text-dim"
                }`}
            >
              {logObj.timestamp && (
                <span className="text-soc-text-dim/60 flex-shrink-0 select-all">
                  {logObj.timestamp}
                </span>
              )}
              <span className="text-soc-border flex-shrink-0">│</span>
              <span className="flex-1">{logObj.message}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default LogsPanel;
