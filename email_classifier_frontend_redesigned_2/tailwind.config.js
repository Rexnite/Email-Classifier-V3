/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        base: '#020617',
        panel: '#0F172A',
        line: 'rgba(255,255,255,0.10)',
        ink: '#F8FAFC',
        mute: '#94A3B8',
        signal: '#38BDF8',
        live: '#34D399',
        warn: '#F59E0B',
        danger: '#FB7185',
      },
      boxShadow: {
        soft: '0 18px 60px rgba(0, 0, 0, 0.28)',
        glow: '0 0 36px rgba(56, 189, 248, 0.22)',
      },
      fontFamily: {
        display: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        body: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
}
