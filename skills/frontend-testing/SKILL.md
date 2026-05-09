# Frontend Testing

## Descripción
Testing de aplicaciones frontend. Tests unitarios, de componentes, de integración y E2E. Pirámide de testing, mocks, y mejores prácticas.

## Tecnologías
- **Vitest**: Test runner rápido (Vite native), compatible con Jest API
- **Testing Library**: Tests desde la perspectiva del usuario
- **Playwright**: E2E, multi-browser, mobile emulation
- **MSW** (Mock Service Worker): Mock de APIs en service worker
- **Cypress**: Alternativa E2E, buen debugging visual

## Pirámide de testing

```
    ⬆️  E2E (Playwright)  — flujos críticos
   ⬆️⬆️  Integración      — componentes + API
  ⬆️⬆️⬆️  Unitarios        — hooks, utils, lógica pura
⬆️⬆️⬆️⬆️  Estático         — TypeScript, ESLint
```

## Patrones clave

### Test de componente (desde el usuario)
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';

import Counter from './Counter';

describe('Counter', () => {
  it('increments when clicked', async () => {
    const user = userEvent.setup();
    render(<Counter initial={0} />);
    
    const button = screen.getByRole('button', { name: /increment/i });
    await user.click(button);
    
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});
```

### Mock de API con MSW
```ts
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'Leandro' }]);
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Test de hook
```ts
import { renderHook, act } from '@testing-library/react';
import useCounter from './useCounter';

describe('useCounter', () => {
  it('should increment', () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });
});
```

## Alternativas
- **Jest**: El anterior estándar, migrando a Vitest
- **Cypress**: Bueno para E2E, menos rápido que Playwright
- **Testing Library**: Para React, Vue, Svelte, Angular — misma API

## Consideraciones
- Probá comportamiento, no implementación
- No tests de snapshot a menos que sean críticos
- Un test que toca el DOM lento es mejor que un test que no existe
- CI debe ejecutar tests en cada PR
