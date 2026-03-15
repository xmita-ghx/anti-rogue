import React from "react";

const severityConfig = {
  critical: {
    icon: "🔴",
    bgColor: "bg-soc-critical-dim",
    borderColor: "border-soc-critical/30",
    textColor: "text-soc-critical",
    label: "CRITICAL",
  },
  warning: {
    icon: "🟡",
    bgColor: "bg-soc-warning-dim",
    borderColor: "border-soc-warning/30",
    textColor: "text-soc-warning",
    label: "WARNING",
  },
  info: {
    icon: "🔵",
    bgColor: "bg-soc-accent-dim",
    borderColor: "border-soc-accent/30",
    textColor: "text-soc-accent",
    label: "INFO",
  },
};

function AlertsPanel({ alerts }) {
  const hasAlerts = alerts && alerts.length > 0;

  return (
    <div className="soc-panel h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-soc-text flex items-center gap-2">
          <span className="text-soc-warning">▸</span>
          Security Alerts
        </h2>
        {hasAlerts && (
          <span className="bg-soc-critical text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center">
            {alerts.length}
          </span>
        )}
      </div>

      {!hasAlerts && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl mb-2 opacity-40">🛡️</div>
            <p className="text-soc-text-dim text-sm">No active alerts</p>
            <p className="text-soc-text-dim/60 text-xs mt-1">All systems nominal</p>
          </div>
        </div>
      )}

      {hasAlerts && (
        <div className="flex-1 overflow-y-auto space-y-2 max-h-72 pr-1">
          {[...alerts].reverse().map((alert, index) => {
            const alertObj =
              typeof alert === "string"
                ? { severity: "warning", message: alert, timestamp: "" }
                : alert;
            const config =
              severityConfig[alertObj.severity] || severityConfig.warning;

            return (
              <div
                key={index}
                className={`alert-entry ${config.bgColor} border ${config.borderColor} rounded-lg px-3 py-2.5`}
              >
                <div className="flex items-start gap-2">
                  <span className="text-sm mt-0.5 flex-shrink-0">
                    {config.icon}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span
                        className={`text-[10px] font-bold tracking-wider ${config.textColor}`}
                      >
                        [{config.label}]
                      </span>
                      {alertObj.timestamp && (
                        <span className="text-[10px] text-soc-text-dim font-mono">
                          {alertObj.timestamp}
                        </span>
                      )}
                    </div>
                    <p className="text-soc-text text-xs leading-relaxed">
                      {alertObj.message}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default AlertsPanel;
