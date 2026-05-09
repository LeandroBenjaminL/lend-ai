# State Management

## Descripción
Manejo de estado en aplicaciones frontend. Estado global vs local, librerías de estado, persistencia, y patrones de sincronización.

## Tecnologías
- **Zustand**: Liviano, simple, sin boilerplate, middleware
- **Redux Toolkit**: Estructurado, devtools, RTK Query integrado
- **React Context**: Built-in, para estado simple/theme/auth
- **Jotai**: Atómico, similar a Recoil pero más simple
- **TanStack Query**: Para estado del servidor (ver api-integration)

## Cuándo usar qué

| Librería | Cuándo | Ventaja |
|----------|--------|---------|
| React Context | Tema, auth, idioma | Sin dependencias |
| Zustand | Apps medianas, equipo chico | Mínimo boilerplate |
| Redux Toolkit | Apps grandes, equipo grande | Estructura, devtools, middlewares |
| Jotai | Estado atómico, performance | Re-renders precisos |

## Patrones clave

### Zustand — Store simple
```ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartStore {
  items: string[];
  addItem: (item: string) => void;
  removeItem: (item: string) => void;
  total: number;
}

const useCart = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) => set((state) => ({ items: [...state.items, item] })),
      removeItem: (item) => set((state) => ({
        items: state.items.filter((i) => i !== item),
      })),
      get total() { return get().items.length; }, // 👎 no hacer, mejor computed selector
    }),
    { name: 'cart-storage' }
  )
);
```

### Redux Toolkit — Slice
```ts
const cartSlice = createSlice({
  name: 'cart',
  initialState: { items: [] as string[] },
  reducers: {
    addItem: (state, action: PayloadAction<string>) => {
      state.items.push(action.payload); // immer: mutable syntax
    },
    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(i => i !== action.payload);
    },
  },
});
```

### Regla de oro: Estado local > Context > Librería
1. ¿Lo usa solo este componente? → `useState`
2. ¿Lo usan 2-3 componentes cercanos? → `useState` + props
3. ¿Lo usan varios componentes lejanos? → Context
4. ¿Muchos componentes, muchas actualizaciones? → Zustand/Redux

## Alternativas
- **Pinia** (Vue) → El Vuex reemplazado
- **Svelte stores** → Built-in en Svelte
- **Signals** (Solid, Preact, Angular) → Modelo atómico moderno

## Consideraciones
- No pongas TODO en estado global — solo lo que realmente se comparte
- Los selectores mal hechos causan re-renders innecesarios
- Preferí selectores atómicos (un valor a la vez)
- Estado del servidor NO va en estado global — va en TanStack Query
