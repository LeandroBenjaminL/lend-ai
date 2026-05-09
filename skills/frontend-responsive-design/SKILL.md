# Responsive Design

## Descripción
Diseño adaptable a múltiples dispositivos y tamaños de pantalla. Mobile-first, breakpoints, container queries, y patrones de layout responsivo.

## Tecnologías
- **CSS Media Queries**: Breakpoints tradicionales
- **CSS Container Queries**: Responsive por contenedor, no por viewport
- **CSS Grid + Flexbox**: Layouts adaptativos sin frameworks
- **clamp()**: Tamaños fluidos sin media queries
- **Viewport units**: vw, vh, dvw, dvh, lvh, svh

## Enfoque Mobile-First

```css
/* Base: mobile */
.card { padding: 1rem; }

/* Tablet+ */
@media (min-width: 768px) {
  .card { padding: 1.5rem; }
}

/* Desktop+ */
@media (min-width: 1024px) {
  .card { padding: 2rem; }
}
```

## Patrones clave

### Tamaños fluidos con clamp()
```css
/* Título: 2rem en mobile, 4rem en desktop */
h1 { font-size: clamp(2rem, 5vw, 4rem); }

/* Padding fluido */
.container { padding-inline: clamp(1rem, 5vw, 3rem); }
```

### Container Queries (responsive por componente)
```css
.product-card {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .product-card { flex-direction: row; }
  .product-card img { width: 200px; }
}
```

### Grid responsivo sin media queries
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
```

## Breakpoints recomendados
```css
/* 480px  — mobile grande  */
/* 640px  — tablet chica    */
/* 768px  — tablet           */
/* 1024px — desktop          */
/* 1280px — desktop grande   */
/* 1536px — ultra-wide       */
```

## Consideraciones
- Mobile-first: base mobile, media queries para más grande
- No uses breakpoints de dispositivos específicos, usá contenido
- Container Queries son el futuro del responsive component-level
- Probá en dispositivos reales, no solo en devtools
- Touch targets mínimos: 44x44px (WCAG)
