export const colors = {
  background: '#0f1115',
  surface: '#15171c',
  surfaceSubtle: '#1c1f26',
  accent: '#00c2a8',
  accentMuted: '#33d4be',
  textPrimary: '#f8fafc',
  textSecondary: '#9ba4b5',
  textMuted: '#6d7684',
  danger: '#ff6b6b'
} as const;

export const typography = {
  fontFamily: `'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`,
  sizes: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.5rem',
    display: '2.25rem'
  },
  lineHeights: {
    tight: 1.2,
    snug: 1.35,
    normal: 1.5
  }
} as const;

export const spacing = {
  none: '0',
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem'
} as const;

export const radii = {
  sm: '0.375rem',
  md: '0.75rem',
  pill: '999px'
} as const;

export const shadows = {
  soft: '0 12px 32px rgba(15, 17, 21, 0.45)',
  focus: '0 0 0 2px rgba(0, 194, 168, 0.4)'
} as const;

export const durations = {
  fast: '120ms',
  normal: '200ms',
  slow: '320ms'
} as const;
