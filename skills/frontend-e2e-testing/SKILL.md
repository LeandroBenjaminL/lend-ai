# E2E Testing

## Descripción
Testing End-to-End de aplicaciones frontend. Pruebas de flujos completos multi-página con navegador real.

## Tecnologías
- **Playwright**: Multi-browser (Chromium, Firefox, WebKit), mobile emulation, network intercept
- **Cypress**: Developer-friendly, time travel debugging, menos browsers

## Por qué Playwright sobre Cypress
- Soporta 3 browsers (Chrome, Firefox, Safari)
- Mobile emulation real (no solo viewport)
- Network intercept más potente
- Más rápido en CI
- Mismo equipo que Puppeteer (Google → Microsoft)

## Patrones clave

### Test E2E básico
```ts
import { test, expect } from '@playwright/test';

test('user can login and see dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page.locator('h1')).toHaveText('Dashboard');
});
```

### Mock de API
```ts
await page.route('**/api/users', async (route) => {
  await route.fulfill({ json: [{ id: 1, name: 'Test' }] });
});
```

## Consideraciones
- E2E tests son lentos — solo para flujos críticos
- Usá data-testid en lugar de clases CSS frágiles
- Corré en CI contra un entorno controlado
- Parallel execution para acelerar
