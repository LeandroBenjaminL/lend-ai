# TypeScript

## Descripción
TypeScript avanzado para frontend. Tipado estricto, genéricos, utility types, branded types, type inference, y patrones de tipos para React.

## Tecnologías
- TypeScript 5.x
- strict mode
- satisfies, const type parameters
- Template literal types
- Conditional types, mapped types

## Configuración recomendada

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "target": "ES2022"
  }
}
```

## Patrones clave

### Branded Types para IDs
```ts
type UserId = string & { __brand: 'UserId' };
type PostId = string & { __brand: 'PostId' };
function getUser(id: UserId) { /* ... */ }
// getUser(postId) → ERROR en compilación
```

### Discriminated Unions para estado
```ts
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };
```

### satisfies para inferencia precisa
```ts
const config = {
  api: 'https://api.example.com',
  timeout: 5000,
} satisfies Record<string, string | number>;
// config.api → string, no string | number
```

### Utility Types para componentes
```ts
type PropsWithChildren<T = {}> = T & { children?: React.ReactNode };
type OmitAndMerge<T, K extends keyof T, Overrides> = Omit<T, K> & Overrides;
```

## Alternativas
- **JSDoc**: Tipado sin compilación, útil para JS puro
- **Flow**: De Facebook, prácticamente muerto
- **PureScript/ReasonML**: Funcional, no mainstream

## Consideraciones
- strict mode NO es negociable
- Evitá `any` — usá `unknown` y después type narrowing
- Los `as` casts son necesarios a veces pero siempre intentá type narrowing primero
- TypeScript es inversión: más tiempo ahora, menos bugs después
