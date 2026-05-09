# Web Performance

## Descripción
Optimización de performance web. Core Web Vitals, Lighthouse, bundle optimization, lazy loading, caching, y patrones de renderizado eficiente.

## Métricas Core Web Vitals

| Métrica | Qué mide | Bueno | Malo |
|---------|----------|-------|------|
| **LCP** | Carga del contenido principal | ≤2.5s | >4s |
| **FID / INP** | Interactividad | ≤100ms | >300ms |
| **CLS** | Estabilidad visual | ≤0.1 | >0.25 |

## Patrones clave

### Lazy Loading de imágenes
```tsx
// Nativo del browser — sin librerías
<img src="hero.webp" loading="lazy" decoding="async" />

// Con next/image o @astrojs/image
<Image src="/hero.jpg" width={1200} height={600} loading="lazy" />
```

### Code Splitting con React.lazy
```tsx
const Dashboard = lazy(() => import('./Dashboard'));

<Suspense fallback={<Skeleton />}>
  <Dashboard />
</Suspense>
```

### Preload de recursos críticos
```html
<link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin />
<link rel="preload" href="/hero.webp" as="image" />
<link rel="preconnect" href="https://api.example.com" />
```

### Bundle Analysis
```bash
# Vite
npx vite-bundle-analyzer

# Webpack
npx webpack-bundle-analyzer dist/stats.json
```

### Técnicas de optimización

| Técnica | Impacto | Esfuerzo |
|---------|---------|----------|
| Imágenes WebP/AVIF | Alto | Bajo |
| Code splitting | Alto | Medio |
| Tree shaking | Medio | Bajo |
| Critical CSS | Alto | Medio |
| Font display swap | Medio | Bajo |
| CDN + caching | Alto | Bajo |
| Preconnect a origins | Medio | Bajo |

## Herramientas
- **Lighthouse**: Audit automático en Chrome DevTools
- **PageSpeed Insights**: Lighthouse desde servers de Google
- **Web Vitals Library**: Medir en producción (JS)
- **BundlePhobia**: Costo de agregar una dependencia
- **Calibre / SpeedCurve**: Monitoreo continuo

## Consideraciones
- Medí antes de optimizar — no optimices lo que no sabés que es problema
- El mayor impacto suele venir de imágenes y fonts
- Third-party scripts (analytics, ads, chat) son la causa #1 de performance pobre
- Performance es feature, no afterthought
