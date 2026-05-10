# Network Engineer — Patterns

### Nginx reverse proxy
```nginx
server {
    listen 443 ssl;
    server_name app.example.com;

    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Caddy (auto TLS)
```
app.example.com {
    reverse_proxy localhost:3000
}
```

### TLS best practices
- TLS 1.3 only (o 1.2+)
- HSTS header
- OCSP Stapling
- Auto-renewal con acme.sh o certbot
