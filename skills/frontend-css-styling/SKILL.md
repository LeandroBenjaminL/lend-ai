# CSS Styling

## Descripción
Estilos para interfaces web modernas. CSS nativo, Tailwind CSS, CSS Modules, sistemas de diseño, responsive, temas, y animaciones.

## Tecnologías
- **CSS Moderno**: Grid, Flexbox, Container Queries, Custom Properties, :has(), nesting
- **Tailwind CSS**: Utility-first, configuración, plugins, JIT
- **CSS Modules**: Scoped styles, composición
- **CSS-in-JS**: styled-components, Emotion (menos recomendado hoy)

## Cuándo usar cada enfoque

| Enfoque | Cuándo | Por qué |
|---------|--------|---------|
| Tailwind CSS | Proyectos nuevos, equipos chicos | Rápido, consistente, sin naming |
| CSS Modules | Componentes críticos, librerías | Scope real, sin runtime |
| CSS-in-JS | Legado o casos muy específicos | Runtime cost, mejor evitarlo |
| Vanilla CSS | Proyectos simples, prototipos | Sin dependencias |

## Patrones clave

### Layout con Grid
```css
.layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

### Container Queries (responsive por componente)
```css
.card-container { container-type: inline-size; }
@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

### Temas con Custom Properties
```css
:root {
  --color-primary: #3b82f6;
  --color-surface: #ffffff;
  --spacing-unit: 0.25rem;
}
[data-theme="dark"] {
  --color-primary: #60a5fa;
  --color-surface: #1e1e2e;
}
```

## Alternativas
- **SCSS/Sass**: Preprocesador con nesting, mixins, variables (hoy CSS nativo tiene casi todo)
- **UnoCSS**: Alternativa a Tailwind, bajo demanda, más rápido
- **Open Props**: Custom Properties pre-hechas, sin clases

## Consideraciones
- Mobile-first siempre: `min-width` en media queries
- Evitá `!important` — es olor a diseño no encapsulado
- Preferí lógica CSS (Grid, Container Queries) sobre frameworks de grilla
- CSS tiene 25+ nuevas features en los últimos 3 años — mantenete actualizado
