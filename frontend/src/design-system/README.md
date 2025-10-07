# Dompet Design System

The Dompet design system emphasises calm, CFP-grade communication with crisp contrast and thoughtful spacing inspired by Ollama's progressive disclosure.

## Principles

1. **Clarity first** – Typography scales anchored to 4pt rhythm, ensuring primary actions stand out without overwhelming.
2. **Ambient surfaces** – Low-contrast containers (`surface`, `surfaceSubtle`) keep attention on content while providing depth via soft shadows.
3. **Conversational cues** – Components like `Card`, `Text`, and `AppShell` encourage narrative flows that match the financial copilot voice.

## Usage

```tsx
import { AppShell, Button, Card, Text } from '@/design-system';

export default function Dashboard() {
  return (
    <AppShell
      headerTitle="Your CFP in the pocket"
      subheader="Track cashflow, automate savings, and chat with the Dompet agent."
    >
      <Card>
        <Text size="lg">Net Cashflow</Text>
        <Text tone="secondary">RM 1,250 in May</Text>
        <Button style={{ marginTop: '1rem' }}>See breakdown</Button>
      </Card>
    </AppShell>
  );
}
```

Include `src/design-system/styles.css` at the app entry point to ensure base tokens cascade across the experience.
