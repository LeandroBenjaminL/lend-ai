# Docker Engineer — Patterns

### Image optimization
- Alpine-based images (más pequeñas, menos vulns)
- `--no-cache` en apk/apk del
- Multi-stage: build en etapa 1, runtime en etapa 2
- `.dockerignore` para excluir node_modules, .git, etc

### Security
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### Layer caching
```
COPY package*.json ./
RUN npm ci
COPY . .
```
