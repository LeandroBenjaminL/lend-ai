# YouTube — Extraer y analizar transcripción de videos

## Descripción
Toma un link de YouTube, extrae su transcripción (subtítulos) y la analiza con IA para generar un resumen estructurado.

## Uso
```
@data-analyst youtube https://www.youtube.com/watch?v=VIDEO_ID
@data-analyst pasame el transcript de este video: https://youtu.be/VIDEO_ID
@data-analyst resumime este video: https://www.youtube.com/watch?v=VIDEO_ID
```

## Cómo funciona
1. Extrae el ID del video de cualquier formato de URL
2. Usa `youtube_transcript_api` para obtener los subtítulos
3. Procesa el texto con un modelo T4/T5 para resumir
4. Devuelve: resumen ejecutivo + puntos clave + conceptos técnicos + timestamps
5. Guarda el resultado en Engram para referencia futura

## Requisitos
- `youtube_transcript_api` instalado (pip)
- El video debe tener subtítulos/CC disponibles

## Output
- ✅ Transcripción completa con timestamps
- 📋 Resumen estructurado en markdown
- 🔍 Puntos clave y conceptos técnicos
- 💾 Guardado automático en Engram
