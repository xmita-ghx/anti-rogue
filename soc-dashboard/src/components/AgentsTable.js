import React from "react";

const statusConfig = {
  Active: {
    bgColor: "bg-soc-normal-dim",
    textColor: "text-soc-normal",
    dotColor: "bg-soc-normal",
    label: "Active",
  },
  Suspicious: {
    bgColor: "bg-soc-warning-dim",
    textColor: "text-soc-warning",
    dotColor: "bg-soc-warning",
    label: "Suspicious",
  },
  Disabled: {
    bgColor: "bg-soc-critical-dim",
    textColor: "text-soc-critical",
    dotColor: "bg-soc-critical",
    label: "Disabled",
  },
};

function StatusBadge({ status }) {
  const config = statusConfig[status] || statusConfig.Active;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${config.bgColor} ${config.textColor}`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${config.dotColor} ${status === "Suspicious" ? "animate-pulse" : ""
          }`}
      ></span>
      {config.label}
    </span>
  );
}

function AgentsTable({ agents, onDisableAgent }) {
  return (
    <div className="soc-panel">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-soc-text flex items-center gap-2">
          <span className="text-soc-accent">▸</span>
          Active Agents
        </h2>
        <span className="text-xs text-soc-text-dim bg-soc-bg rounded-md px-2 py-1">
          {agents.filter((a) => a.status !== "Disabled").length} online
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-soc-border">
              <th className="text-left py-3 px-4 text-xs font-medium text-soc-text-dim uppercase tracking-wider">
                Agent ID
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-soc-text-dim uppercase tracking-wider">
                Status
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-soc-text-dim uppercase tracking-wider">
                API Calls
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-soc-text-dim uppercase tracking-wider">
                Permissions
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-soc-text-dim uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-soc-border/50">
            {agents.map((agent) => (
              <tr
                key={agent.id}
                className={`transition-colors duration-200 hover:bg-soc-panel-light/50 ${agent.status === "Suspicious"
                    ? "bg-soc-warning-dim/30"
                    : agent.status === "Disabled"
                      ? "bg-soc-critical-dim/20"
                      : ""
                  }`}
              >
                <td className="py-3 px-4">
                  <span className="font-mono text-soc-accent font-medium">
                    {agent.id}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <StatusBadge status={agent.status} />
                </td>
                <td className="py-3 px-4">
                  <span
                    className={`font-mono ${agent.apiCalls > 200
                        ? "text-soc-critical font-bold"
                        : "text-soc-text"
                      }`}
                  >
                    {agent.apiCalls.toLocaleString()}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span
                    className={`text-sm ${agent.permissions === "Admin"
                        ? "text-soc-critical font-semibold"
                        : agent.permissions === "None"
                          ? "text-soc-text-dim"
                          : "text-soc-text"
                      }`}
                  >
                    {agent.permissions}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <button
                    type="button"
                    className="bg-soc-critical/20 hover:bg-soc-critical/40 text-soc-critical border border-soc-critical/30 hover:border-soc-critical/60 rounded-lg px-3 py-1.5 text-xs font-medium transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-soc-critical/20 disabled:hover:border-soc-critical/30"
                    onClick={() =>
                      onDisableAgent ? onDisableAgent(agent.id) : undefined
                    }
                    disabled={agent.status === "Disabled"}
                  >
                    {agent.status === "Disabled" ? "Disabled" : "Disable"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AgentsTable;
