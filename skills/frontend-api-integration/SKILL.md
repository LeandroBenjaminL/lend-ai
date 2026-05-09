# API Integration

## Descripción
Consumo de APIs desde el frontend. Fetching de datos, caché, revalidación, optimistic updates, manejo de errores, y patrones de integración con backend.

## Tecnologías
- **TanStack Query (React Query)**: Caché automática, refetch, paginación, infinite scroll
- **fetch nativo**: Sin dependencias, suficiente para casos simples
- **Axios**: Interceptors, cancelación, progreso de upload
- **SWR**: Estrategia stale-while-revalidate, más liviano que TanStack Query
- **RTK Query**: Integrado con Redux Toolkit

## Cuándo usar qué

| Biblioteca | Cuándo | Ventaja |
|------------|--------|---------|
| TanStack Query | Apps con datos del server | Caché, refetch, devtools |
| fetch + hooks | Apps simples, SSR | 0 dependencias |
| Axios | Necesitás interceptors | Request/response transforms |
| SWR | Priorizás velocidad sobre features | Liviano, simple |

## Patrones clave

### Custom Hook con TanStack Query
```ts
function usePosts() {
  return useQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('/api/posts').then(r => r.json()),
    staleTime: 5 * 60 * 1000, // 5 min
  });
}
```

### Optimistic Update
```ts
const mutation = useMutation({
  mutationFn: (newPost) => fetch('/api/posts', { method: 'POST', body: JSON.stringify(newPost) }),
  onMutate: async (newPost) => {
    await queryClient.cancelQueries({ queryKey: ['posts'] });
    const previous = queryClient.getQueryData(['posts']);
    queryClient.setQueryData(['posts'], (old) => [...old, newPost]);
    return { previous };
  },
  onError: (err, newPost, context) => {
    queryClient.setQueryData(['posts'], context.previous);
  },
});
```

### Estados del request
```ts
function PostList() {
  const { data, isLoading, isError, error } = usePosts();
  if (isLoading) return <Spinner />;
  if (isError) return <Error message={error.message} />;
  return <List items={data} />;
}
```

## Alternativas
- **tRPC**: APIs end-to-end type-safe, TypeScript en front y back
- **OpenAPI Generator**: Genera clientes desde spec OpenAPI
- **GraphQL**: Apollo, urql (cubierto en skill graphql)

## Consideraciones
- Siempre mostrá loading, error y success states
- Caché bien configurada reduce requests un 80%
- Optimistic updates mejoran UX pero requieren manejo de errores
- Los endpoints del backend deberían ser versionados (/api/v1/)
