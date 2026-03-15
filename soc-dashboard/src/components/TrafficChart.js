import React, { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

function TrafficChart({ dataPoints }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;

    if (!canvas) {
      return;
    }

    const ctx = canvas.getContext("2d");

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    // Create gradient fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 280);
    gradient.addColorStop(0, "rgba(6, 182, 212, 0.3)");
    gradient.addColorStop(0.5, "rgba(6, 182, 212, 0.08)");
    gradient.addColorStop(1, "rgba(6, 182, 212, 0)");

    chartRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: dataPoints.map((_, index) => `${index + 1}s`),
        datasets: [
          {
            label: "Requests/sec",
            data: dataPoints,
            borderColor: "#06b6d4",
            backgroundColor: gradient,
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#06b6d4",
            pointHoverBorderColor: "#0f172a",
            pointHoverBorderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 400,
          easing: "easeInOutQuart",
        },
        interaction: {
          intersect: false,
          mode: "index",
        },
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            enabled: true,
            backgroundColor: "#1e293b",
            titleColor: "#e2e8f0",
            bodyColor: "#94a3b8",
            borderColor: "#334155",
            borderWidth: 1,
            padding: 10,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              title: (items) => `Time: ${items[0].label}`,
              label: (item) => `Requests: ${item.formattedValue}`,
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Time (seconds)",
              color: "#64748b",
              font: {
                size: 11,
                family: "'Inter', sans-serif",
              },
            },
            ticks: {
              color: "#64748b",
              font: {
                size: 10,
                family: "'Inter', sans-serif",
              },
              maxTicksLimit: 10,
            },
            grid: {
              color: "rgba(51, 65, 85, 0.4)",
              drawBorder: false,
            },
            border: {
              display: false,
            },
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Requests",
              color: "#64748b",
              font: {
                size: 11,
                family: "'Inter', sans-serif",
              },
            },
            ticks: {
              color: "#64748b",
              font: {
                size: 10,
                family: "'Inter', sans-serif",
              },
              padding: 8,
            },
            grid: {
              color: "rgba(51, 65, 85, 0.3)",
              drawBorder: false,
            },
            border: {
              display: false,
            },
          },
        },
      },
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
        chartRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (!chartRef.current) {
      return;
    }

    const chart = chartRef.current;
    const ctx = chart.ctx;

    // Rebuild gradient on update
    const gradient = ctx.createLinearGradient(0, 0, 0, 280);

    // Change gradient color based on traffic level
    const maxVal = Math.max(...dataPoints);
    if (maxVal > 200) {
      gradient.addColorStop(0, "rgba(239, 68, 68, 0.35)");
      gradient.addColorStop(0.5, "rgba(239, 68, 68, 0.1)");
      gradient.addColorStop(1, "rgba(239, 68, 68, 0)");
      chart.data.datasets[0].borderColor = "#ef4444";
    } else {
      gradient.addColorStop(0, "rgba(6, 182, 212, 0.3)");
      gradient.addColorStop(0.5, "rgba(6, 182, 212, 0.08)");
      gradient.addColorStop(1, "rgba(6, 182, 212, 0)");
      chart.data.datasets[0].borderColor = "#06b6d4";
    }

    chart.data.datasets[0].backgroundColor = gradient;
    chart.data.labels = dataPoints.map((_, index) => `${index + 1}s`);
    chart.data.datasets[0].data = dataPoints;
    chart.update("none");
  }, [dataPoints]);

  return (
    <div className="h-72">
      <canvas ref={canvasRef} />
    </div>
  );
}

export default TrafficChart;
