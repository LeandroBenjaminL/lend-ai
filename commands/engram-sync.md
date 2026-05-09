# Engram Sync — Sincronizar memoria entre máquinas vía git

## Descripción
Sincroniza tu memoria de Engram entre varias máquinas (PC escritorio, laptop, etc.)
**sin pisar ni perder datos**, usando chunks exportados en vez del binario crudo.

Engram guarda toda tu memoria (decisiones, bugs, descubrimientos) en `~/.engram/`.
Este sistema usa `engram sync` para exportar solo **lo nuevo** como chunks comprimidos
y los sincroniza vía git. El `.db` binario nunca toca git → **no hay conflictos**.

## Uso Rápido

```bash
# Tu mejor amigo:
engram-smart-sync auto     # Pull + push en un solo comando

# O paso a paso:
engram-smart-sync pull     # Antes de trabajar (trae lo de otras máquinas)
engram-smart-sync push     # Después de trabajar (sube lo tuyo)
engram-smart-sync status   # Ver estado del sync

# Desde OpenCode:
@data-analyst /engram-sync
```

## Cómo funciona

```
                    ┌─────────────────────┐
                    │  ~/.engram/engram.db │
                    │  (tu memoria local)  │
                    └──────┬──────────────┘
                           │
               ┌───────────┴───────────┐
               │  engram sync --all    │
               │  (exporta chunks)     │
               └───────────┬───────────┘
                           │
                    ┌──────┴──────┐
                    │  .engram/   │
                    │  chunks/    │  ← Archivos mergeables por git
                    │  manifest   │
                    └──────┬──────┘
                           │
               ┌───────────┴───────────┐
               │  git push/pull        │
               │  (solo chunks, no .db)│
               └───────────────────────┘
```

## Setup inicial (solo la primera vez)

### En tu máquina principal (la que tiene toda la memoria)
```bash
# 1. Crear repo privado en GitHub
gh repo crear engram-data --private

# 2. Configurar el remote en ~/.engram
cd ~/.engram
git remote add origin https://github.com/TU_USUARIO/engram-data.git

# 3. Ignorar el .db binario (solo trackear chunks)
echo "engram.db" >> .gitignore
git rm --cached engram.db
git add .gitignore
git commit -m "config: ignore engram.db"

# 4. Exportar chunks y subir
engram sync --all
git add .engram/
git commit -m "sync inicial: chunks de memoria"
git push -u origin main
```

### En la otra máquina (laptop, etc.)
```bash
# 1. Clonar el repo en ~/.engram
git clone https://github.com/TU_USUARIO/engram-data.git ~/.engram

# 2. Importar los chunks al .db local
cd ~/.engram
engram sync --import
```

## Flujo diario

### 🟢 Antes de trabajar (en cualquier máquina)
```bash
engram-smart-sync pull
# Esto hace:
#   1. git pull (baja chunks de otras máquinas)
#   2. engram sync --import (los mete a tu .db local)
```

### 🔴 Después de trabajar
```bash
engram-smart-sync push
# Esto hace:
#   1. engram sync --all (exporta lo nuevo a chunks)
#   2. git add/commit/push (sube chunks a GitHub)
```

### 🔵 Todo automático
```bash
engram-smart-sync auto
# = pull + push en secuencia
```

## Por qué NO hay conflictos

| Archivo | ¿En git? | ¿Se mergea? | Problema |
|---------|----------|-------------|----------|
| `engram.db` (binario) | ❌ No (en .gitignore) | ❌ No aplica | Si estuviera, git no podría mergearlo |
| `.engram/chunks/*.jsonl.gz` (texto) | ✅ Sí | ✅ Sí | Git mergea sin drama |

## Automatización recomendada
Agregá al final de tu `~/.bashrc` o `~/.zshrc`:

```bash
# Engram auto-sync al abrir terminal
if command -v engram-smart-sync &>/dev/null && [ -d "$HOME/.engram/.git" ]; then
    engram-smart-sync pull 2>/dev/null || true
fi
```

## Requisitos
- Engram CLI instalado (`engram --version`)
- Git configurado
- Repo git configurado en `~/.engram/`
- (Opcional) `engram-smart-sync` instalado en el PATH
