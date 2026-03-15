/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        'soc-bg': '#0f172a',
        'soc-panel': '#1e293b',
        'soc-panel-light': '#273548',
        'soc-text': '#e2e8f0',
        'soc-text-dim': '#94a3b8',
        'soc-border': '#334155',
        'soc-accent': '#06b6d4',
        'soc-accent-dim': 'rgba(6, 182, 212, 0.15)',
        'soc-critical': '#ef4444',
        'soc-critical-dim': 'rgba(239, 68, 68, 0.15)',
        'soc-warning': '#f59e0b',
        'soc-warning-dim': 'rgba(245, 158, 11, 0.15)',
        'soc-normal': '#22c55e',
        'soc-normal-dim': 'rgba(34, 197, 94, 0.15)',
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', '"Fira Code"', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'fade-in': 'fade-in 0.3s ease-out',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(-4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
