import { ButtonHTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';

import { colors, radii, shadows, spacing, typography } from '../tokens';

export type ButtonVariant = 'primary' | 'ghost' | 'danger';

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  fullWidth?: boolean;
};

const baseStyle: React.CSSProperties = {
  backgroundColor: colors.accent,
  border: 'none',
  borderRadius: radii.pill,
  color: colors.background,
  padding: `${spacing.sm} ${spacing.lg}`,
  fontSize: typography.sizes.sm,
  lineHeight: typography.lineHeights.snug,
  fontWeight: 600,
  cursor: 'pointer',
  transition: `transform ${shadows.focus} ease, box-shadow 180ms ease`,
};

const variantClass: Record<ButtonVariant, string> = {
  primary: 'dompet-btn--primary',
  ghost: 'dompet-btn--ghost',
  danger: 'dompet-btn--danger',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', fullWidth, className, ...props }, ref) => (
    <button
      ref={ref}
      className={clsx('dompet-btn', variantClass[variant], className, {
        'dompet-btn--full': fullWidth,
      })}
      style={baseStyle}
      {...props}
    />
  )
);

Button.displayName = 'Button';
