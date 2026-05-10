# Infra SRE — Patterns

### The Four Golden Signals
- Latency: tiempo de respuesta
- Traffic: requests por segundo
- Errors: tasa de error
- Saturation: qué tan lleno está el sistema

### Alert severity
```
P0: Servicio caído → responder en 5 min
P1: Degradación severa → responder en 15 min
P2: Degradación menor → responder en 1 hora
P3: Warning → siguiente día hábil
```

### Prometheus recording rules
```yaml
groups:
  - name: sli
    rules:
      - record: sli:requests_total:rate5m
        expr: rate(http_requests_total[5m])
```
