import { PropsWithChildren } from 'react';

import { colors, radii, shadows, spacing } from '../tokens';

export type CardProps = PropsWithChildren<{
  padding?: keyof typeof spacing;
  subdued?: boolean;
}>;

export function Card({ children, padding = 'lg', subdued }: CardProps) {
  const style: React.CSSProperties = {
    backgroundColor: subdued ? colors.surfaceSubtle : colors.surface,
    borderRadius: radii.md,
    padding: spacing[padding],
    boxShadow: shadows.soft,
    border: '1px solid rgba(255, 255, 255, 0.04)'
  };

  return <section style={style}>{children}</section>;
}
