import { PropsWithChildren } from 'react';

import { colors, typography } from '../tokens';

export type TextTone = 'primary' | 'secondary' | 'muted' | 'danger';
export type TextSize = keyof typeof typography.sizes;

export interface TextProps {
  as?: keyof JSX.IntrinsicElements;
  tone?: TextTone;
  size?: TextSize;
  weight?: 400 | 500 | 600 | 700;
  align?: 'left' | 'center' | 'right';
  uppercase?: boolean;
}

export function Text({
  as: Component = 'p',
  tone = 'primary',
  size = 'base',
  weight = 500,
  align = 'left',
  uppercase,
  children
}: PropsWithChildren<TextProps>) {
  const style: React.CSSProperties = {
    color: mapToneToColor(tone),
    fontSize: typography.sizes[size],
    lineHeight: typography.lineHeights.normal,
    fontWeight: weight,
    textAlign: align,
    textTransform: uppercase ? 'uppercase' : undefined,
  };

  return <Component style={style}>{children}</Component>;
}

function mapToneToColor(tone: TextTone) {
  switch (tone) {
    case 'secondary':
      return colors.textSecondary;
    case 'muted':
      return colors.textMuted;
    case 'danger':
      return colors.danger;
    default:
      return colors.textPrimary;
  }
}
