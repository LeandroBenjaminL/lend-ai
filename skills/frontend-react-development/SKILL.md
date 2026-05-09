# React Development

## Descripción
Desarrollo de interfaces con React. Componentes, hooks, patrones de composición, Server Components, Suspense, y mejores prácticas del ecosistema React.

## Tecnologías
- React 18/19
- React Hooks (useState, useEffect, useCallback, useMemo, useRef, useContext, useReducer, custom hooks)
- Server Components (React 19)
- Suspense y Transitions
- Patrones: Compound Components, Render Props, Higher-Order Components

## Frameworks relacionados
- **Next.js** → SSR, SSG, ISR, App Router
- **Astro** → Islas de interactividad con React
- **Vite** → Build tool recomendado

## Cuándo usar React
- Apps interactivas con estado complejo
- Dashboards y paneles de administración
- Aplicaciones que necesitan ecosistema maduro de librerías
- Equipos grandes que necesitan estructura

## Alternativas
- **Vue 3** → Más fácil de aprender, template-based
- **Svelte 5** → Menos boilerplate, compilado
- **Solid** → Más performante, sin virtual DOM
- **Preact** → Misma API que React, 3KB

## Patrones clave

### Composición sobre herencia
```tsx
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
}
```

### Custom Hooks para lógica reutilizable
```tsx
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

### Error Boundaries
```tsx
class ErrorBoundary extends React.Component<{ fallback: React.ReactNode }, { hasError: boolean }> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  render() { return this.state.hasError ? this.props.fallback : this.props.children; }
}
```

## Consideraciones
- Preferí Server Components para datos, Client Components para interactividad
- Evitá useEffect para sincronizar estado — preferí useSyncExternalStore o librerías de estado
- Usá React.memo solo cuando haya re-renders medibles, no por default
- TypeScript es obligatorio en proyectos React modernos
