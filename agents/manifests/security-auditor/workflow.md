# Security Auditor — Workflow

1. Escanear dependencias (vulnerabilidades conocidas)
2. Escanear código (SAST - bandit, semgrep)
3. Escanear contenedores (trivy)
4. Verificar secrets en git (gitleaks)
5. Revisar configuración (hardening)
6. Reportar findings con severidad
7. Recomendar fixes priorizados
