import { CSSProperties } from 'react';

import { colors, radii, typography } from '../tokens';

export interface AvatarProps {
  name: string;
  size?: number;
}

export function Avatar({ name, size = 40 }: AvatarProps) {
  const initials = name
    .split(' ')
    .filter(Boolean)
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  const style: CSSProperties = {
    width: size,
    height: size,
    borderRadius: radii.pill,
    background: 'linear-gradient(135deg, #1f2230 0%, #2a2f3f 100%)',
    color: colors.textSecondary,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: typography.sizes.sm,
    fontWeight: 600,
  };

  return <span style={style}>{initials}</span>;
}
