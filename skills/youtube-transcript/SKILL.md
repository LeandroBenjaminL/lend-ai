---
name: youtube-transcript
description: >
  Extracción y análisis de transcripciones de videos de YouTube.
  Obtiene el texto completo de subtítulos/CC, lo procesa y genera resúmenes.
  Trigger: Cuando necesitás entender el contenido de un video de YouTube,
  extraer su texto, o generar un resumen estructurado.
license: Apache-2.0
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: YouTube Transcript

Extraé el texto de cualquier video de YouTube y analizalo con IA.

## Trigger

- Cuando te pasan un link de YouTube y necesitás entender su contenido
- Cuando querés extraer el texto de subtítulos/transcripción
- Cuando necesitás un resumen estructurado del video
- Cuando querés analizar el contenido sin ver el video

## Por qué existe

Los modelos de lenguaje no pueden ver videos. Esta skill resuelve eso extrayendo
la transcripción (subtítulos) del video para que el contenido pueda ser procesado,
analizado y resumido como cualquier otro texto.

## Herramientas disponibles

### Opción A — YouTube Transcript API (recomendada, rápida)
Usa la librería Python `youtube_transcript_api`. Es la más confiable porque
obtiene los subtítulos directamente de YouTube sin necesidad de navegador.

```python
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
transcript = api.fetch("VIDEO_ID", languages=["es", "en"])

# Cada segmento tiene: text, start (segundos), duration
for seg in transcript:
    print(f"[{seg.start:.1f}s] {seg.text}")
```

**Ventajas**: Rápido, no requiere navegador, funciona en headless
**Desventajas**: Depende de que el video tenga subtítulos/CC generados
**Requiere**: `pip install youtube_transcript_api`

### Opción B — Puppeteer + youtubetranscript.com
Navega a `https://youtubetranscript.com/?v=VIDEO_ID` con Puppeteer y extrae
el contenido renderizado.

**Ventajas**: No requiere instalar librerías Python
**Desventajas**: Más lento, requiere navegador, la página carga con JS
**Requiere**: Puppeteer MCP

### Opción C — Invidious API
Usa instancias de Invidious (frontend público de YouTube):
`https://invidious.snopyta.org/api/v1/videos/VIDEO_ID?fields=title,description,subtitleText`

**Ventajas**: Sin dependencias, solo HTTP
**Desventajas**: Depende de una instancia pública, puede rate-limit

## Flujo de trabajo recomendado

### 1. Extraer el transcript
```python
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url: str) -> str:
    """Extrae el ID de un video de YouTube de cualquier formato de URL."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"No se pudo extraer ID de: {url}")

api = YouTubeTranscriptApi()
video_id = extract_video_id(url)
transcript = api.fetch(video_id, languages=["es", "en"])
```

### 2. Procesar el texto
- Uní todos los segmentos en un texto continuo
- Cada segmento tiene timestamp, usalo para referencias
- Limpiá saltos de línea innecesarios y caracteres especiales

### 3. Analizar con IA (T4/T5 para videos complejos)
Pasá el texto completo a un modelo LLM para:
- **Resumen ejecutivo**: 3-5 líneas de qué trata el video
- **Puntos clave**: las ideas principales en orden
- **Conceptos técnicos**: frameworks, herramientas, arquitecturas que menciona
- **Conclusiones**: qué aprendió/compartió el autor
- **Timestamp references**: enlazá momentos clave con su timestamp

### 4. Guardar en Engram
```python
engram_mem_save(
    title=f"YouTube: {titulo_del_video}",
    type="learning",
    content=f"**What**: Resumen del video '{titulo}'\n
             **Key points**: {puntos_clave}\n
             **Source**: {url}\n
             **Transcript length**: {len(transcript)} segmentos"
)
```

## Alternativas y cuándo usarlas

| Situación | Herramienta | Por qué |
|-----------|------------|---------|
| El video tiene CC/subtítulos | `youtube_transcript_api` | Más rápido, directo, sin navegador |
| No tiene subtítulos | ❌ No se puede extraer texto | Necesitás ver el video o esperar CC |
| Necesitás metadatos (título, descripción) | Invidious API | Da más info que solo el transcript |
| Query rápida sin instalar nada | webfetch a invidious | Sin dependencias |

## Anti-patrones

- ❌ Intentar descargar el video completo para extraer audio y pasarlo a texto (muy pesado)
- ❌ Usar Puppeteer si la API de Python funciona (es más lento y frágil)
- ❌ Pasar el transcript crudo sin procesar a un modelo T1/T2 (gasta tokens al pedo si está sucio)
- ❌ No verificar que el video tenga subtítulos antes de intentar extraerlos

## Limitaciones

- Solo funciona con videos que tienen subtítulos/CC generados por YouTube o subidos por el creador
- Videos en vivo o streams pueden no tener transcript disponible inmediatamente
- Videos muy largos (>3 horas) pueden tener transcripts muy grandes (>100K tokens)
- YouTube puede rate-limit si hacés demasiadas requests seguidas
- No puede extraer información visual del video (solo texto)
