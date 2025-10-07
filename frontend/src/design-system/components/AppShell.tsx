import { PropsWithChildren, ReactNode } from 'react';

import { colors, spacing, typography } from '../tokens';
import { Text } from './Text';

export interface AppShellProps {
  sidebar?: ReactNode;
  headerTitle?: string;
  subheader?: string;
}

export function AppShell({
  sidebar,
  headerTitle = 'Dompet',
  subheader,
  children
}: PropsWithChildren<AppShellProps>) {
  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: sidebar ? '320px 1fr' : '1fr',
        minHeight: '100vh',
        backgroundColor: colors.background,
      }}
    >
      {sidebar && (
        <aside
          style={{
            padding: spacing.lg,
            borderRight: '1px solid rgba(255,255,255,0.04)',
            display: 'flex',
            flexDirection: 'column',
            gap: spacing.lg,
          }}
        >
          {sidebar}
        </aside>
      )}
      <main
        style={{
          padding: `${spacing.lg} clamp(1.5rem, 4vw, 4rem)`,
          display: 'flex',
          flexDirection: 'column',
          gap: spacing.lg,
        }}
      >
        <header>
          <Text as="h1" size="display" weight={700}>
            {headerTitle}
          </Text>
          {subheader && (
            <p
              style={{
                marginTop: spacing.sm,
                color: colors.textSecondary,
                fontSize: typography.sizes.lg,
                maxWidth: '56ch',
              }}
            >
              {subheader}
            </p>
          )}
        </header>
        <div style={{ display: 'grid', gap: spacing.lg }}>{children}</div>
      </main>
    </div>
  );
}
