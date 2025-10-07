import { forwardRef, InputHTMLAttributes } from 'react';

import { colors, radii, shadows, spacing, typography } from '../tokens';

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  helperText?: string;
};

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, helperText, id, ...props }, ref) => {
    const resolvedId = id || props.name;
    const field = (
      <input
        id={resolvedId}
        ref={ref}
        style={{
          width: '100%',
          backgroundColor: colors.surface,
          color: colors.textPrimary,
          borderRadius: radii.md,
          border: '1px solid rgba(255, 255, 255, 0.08)',
          padding: `${spacing.sm} ${spacing.md}`,
          fontSize: typography.sizes.base,
          lineHeight: typography.lineHeights.normal,
          outline: 'none',
          transition: `box-shadow ${shadows.focus} ease`,
        }}
        {...props}
      />
    );

    return (
      <label style={{ display: 'block', width: '100%' }}>
        {label && (
          <span
            style={{
              display: 'block',
              marginBottom: spacing.xs,
              color: colors.textSecondary,
              fontSize: typography.sizes.sm,
            }}
          >
            {label}
          </span>
        )}
        {field}
        {helperText && (
          <span
            style={{
              display: 'block',
              marginTop: spacing.xs,
              color: colors.textMuted,
              fontSize: typography.sizes.xs,
            }}
          >
            {helperText}
          </span>
        )}
      </label>
    );
  }
);

Input.displayName = 'Input';
