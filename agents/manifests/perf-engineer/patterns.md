# Performance Engineer — Patterns

### k6 load test
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  const res = http.get('http://localhost:3000/api/health');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

### Performance checklist
- [ ] DB queries tienen índices
- [ ] N+1 queries eliminados
- [ ] Cache implementado (Redis/CDN)
- [ ] Static assets comprimidos
- [ ] Lazy loading aplicado
- [ ] Bundle size optimizado
- [ ] Conexiones pooled
- [ ] Timeouts configurados
