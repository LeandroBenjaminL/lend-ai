---
name: devops-patterns
description: "Patrones y mejores prácticas del ecosistema DevOps."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# DevOps Mentor — Patterns

## Patrones de delegación

### 1. Derivación a sub-agentes
Cuando el usuario pide algo de infraestructura, CI/CD, seguridad o cloud:
- Cargá el sub-agente correcto (`@docker-engineer`, `@ci-cd-pilot`, etc.)
- Pasale el contexto completo
- Esperá su resolución

### 2. Derivación a skills transversales
Cuando la tarea es transversal (commits, docs, tests):
- Usá el agente correspondiente (`@commits-real`, `@lend-ai-docs`, etc.)
- No intentes resolverlo vos mismo

## Patrones de infraestructura

### 3. Docker-first
- Preferí contenedores sobre VMs
- Usá multi-stage builds
- Imágenes minimalistas (Alpine, distroless)

### Docker multi-stage
```
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### 4. GitOps
- Estado del sistema en git = source of truth
- Pull requests para cambios de infra
- Automatización de reconciliación

### CI/CD trunk-based
- Commits directos a main (con feature flags)
- PRs para cambios grandes
- Deploy automático en cada push a main

### 5. Seguridad en capas
- Firewall → WAF → Auth → App
- Principio de mínimo privilegio
- Escaneo continuo de vulnerabilidades

### 6. Cloud resource tagging
- `Project`, `Environment`, `ManagedBy`, `CostCenter`
- Consistent naming: `{project}-{env}-{resource}-{region}`

### 7. Secrets management
- Nunca en git
- Usar vault / secrets manager / env vars
- Rotación automática
