# Patterns: Go Testing

> _Si no está testeado, no funciona. Punto._

## Tabla de decisión: qué patrón de test usar

| Situación | Patrón | Herramienta | Ejemplo |
|-----------|--------|-------------|---------|
| Función pura (misma entrada = misma salida) | **Table-driven** | `testing.T` + `t.Run()` | `func TestSum(t *testing.T)` |
| Función con errores | **Table-driven + wantErr** | `(err != nil) != tt.wantErr` | `func TestParse(t *testing.T)` |
| Dependencia externa (DB, API, FS) | **Interface + Mock** | Interface de 1-2 métodos + mock manual | `type Storage interface` + `mockStorage` |
| State transition de Bubbletea | **Update directo** | `Model.Update(msg)` | `m.Update(tea.KeyMsg{Type: tea.KeyEnter})` |
| Render de vista Bubbletea | **Golden file** | `testdata/*.golden` + `-update` flag | `m.View()` vs golden |
| Flujo completo de TUI | **teatest** | `teatest.NewTestModel()` | `tm.Send(tea.KeyMsg{...})` |
| Archivos temporales | **t.TempDir()** | Directorio auto-limpio | `tmpDir := t.TempDir()` |
| Operación de sistema | **Integration + -short** | `testing.Short()` skip | `if testing.Short() { t.Skip() }` |

## Patrón table-driven: estructura completa

```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {name: "valid input", input: "hello", expected: "HELLO", wantErr: false},
        {name: "empty input", input: "", expected: "", wantErr: true},
        {name: "whitespace input", input: "   ", expected: "", wantErr: false},
        {name: "special chars", input: "héllo", expected: "HÉLLO", wantErr: false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := ProcessInput(tt.input)

            if (err != nil) != tt.wantErr {
                t.Errorf("ProcessInput() error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if result != tt.expected {
                t.Errorf("ProcessInput() = %q, want %q", result, tt.expected)
            }
        })
    }
}
```

**Reglas:**
- `name` descriptivo: "valid input", no "case 1"
- `wantErr` se evalúa con `(err != nil) != tt.wantErr`
- `t.Run()` para cada caso — fallo aislado, nombre visible
- `t.Errorf()` no `t.Fatal()` — seguí ejecutando otros cases
- Cubrí al menos: caso feliz, caso borde, caso error

## Bubbletea testing: state transitions

```go
func TestCursorNavigation(t *testing.T) {
    tests := []struct {
        name       string
        startPos   int
        key        tea.KeyMsg
        endPos     int
        numOptions int
    }{
        {name: "down from 0",        startPos: 0, key: key('j'), endPos: 1, numOptions: 5},
        {name: "up from 1",          startPos: 1, key: key('k'), endPos: 0, numOptions: 5},
        {name: "down at bottom",     startPos: 4, key: key('j'), endPos: 4, numOptions: 5},
        {name: "up at top",          startPos: 0, key: key('k'), endPos: 0, numOptions: 5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            m := NewModel()
            m.Cursor = tt.startPos

            newModel, _ := m.Update(tt.key)
            m = newModel.(Model)

            if m.Cursor != tt.endPos {
                t.Errorf("cursor = %d, want %d", m.Cursor, tt.endPos)
            }
        })
    }
}

func key(r rune) tea.KeyMsg {
    return tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune{r}}
}
```

**Reglas de Bubbletea testing:**
- State transitions: `m.Update(msg)` directamente, sin teatest
- Screen transitions: probá cada combinación de screen + input
- Cursor navigation: probá boundaries (top, bottom, middle)
- View rendering: golden files para output visual

## Anti-patrones de testing

| Anti-patrón | Cómo se ve | Problema | Solución |
|-------------|------------|----------|----------|
| **Test sin assert** | `TestX(t) { fn(); }` | No testea nada, pasa siempre | Agregar `if got != want` |
| **Test duplicado** | 4 bloques if con código casi igual | Mantenimiento horrible | Refactorizar a table-driven |
| **Test frágil** | Assert de string exacto para output con timestamps | Falla cada vez que cambia la fecha | Usar regex, contains, o golden files |
| **Mock complejo** | `mockService` con 10 métodos | El mock es más difícil de mantener que el código real | Partir la interfaz |
| **Test de implementation** | Testea métodos privados o estructura interna | Se rompe con cada refactor | Testeá comportamiento público, no implementación |
| **t.Fatal en loop** | `for ... { t.Fatal() }` | Mata el test en el primer error | Usar `t.Error()` para seguir ejecutando |
| **Sleep en tests** | `time.Sleep(100 * time.Millisecond)` | Test lento y flaky | Usar `time.Now()` mockeable, o `require.Eventually()` |
| **Test sin cleanup** | Crea archivos, DBs, goroutines y no limpia | Estado contaminado entre tests | `t.Cleanup()`, `t.TempDir()`, `defer` |

## Checklist de completitud de tests

- [ ] **Caso feliz:** el camino principal funciona con input válido
- [ ] **Caso de error:** cada error posible tiene un test case
- [ ] **Casos borde:** nil, vacío, máximo, mínimo, caracteres especiales
- [ ] **Casos de regresión:** si es un fix, el test falla sin el fix
- [ ] **Nombres descriptivos:** cada `t.Run()` tiene un nombre que explica el caso
- [ ] **Sin t.Fatal en loop:** usás `t.Error()` para continuar ejecutando
- [ ] **t.Parallel():** tests independientes corren en paralelo
- [ ] **Sin sleeps:** evitás `time.Sleep()`, preferís mocks de tiempo
- [ ] **Sin test de implementation:** testeás comportamiento público
- [ ] **Cobertura mínima:** las funciones críticas están cubiertas (no obsesionarse con %)

## Organización de archivos de test

```
internal/tui/
├── model.go
├── model_test.go           # Tests de modelo y estado
├── update.go
├── update_test.go          # Tests de update handler
├── view.go
├── view_test.go            # Tests de view rendering + golden
├── teatest_test.go         # Tests de integración teatest
└── testdata/
    ├── TestOSSelectGolden.golden
    ├── TestViewMainMenu.golden
    └── TestViewHelp.golden
```

**Reglas:**
- `_test.go` al lado del archivo que testea, mismo package
- `testdata/` para golden files (Go lo ignora en builds)
- Partir archivos de test si pasan 200 líneas
- Helpers van al final o en `helpers_test.go`

## Principios fundamentales

1. **Un test que no falla cuando debería no sirve.** Si no probaste que falla sin el fix, no sabés si el fix funciona.
2. **El nombre del test es la documentación.** `TestSumWithNegativeNumbers` es mejor que `TestSum3`.
3. **Table-driven no es opcional.** Es el estándar de Go para tests con múltiples casos.
4. **Los golden files son para renders.** No assertés strings largos en el test — comp contra archivo.
5. **Las TUIs se testean como modelos, no como cajas negras.** State transition + golden file para render.

> _Un buen test no es el que pasa siempre. Es el que cuando falla, te dice exactamente qué función se rompió, con qué input, y qué esperabas. Si tenés que debuggear el test para entender por qué falló, el test está mal diseñado._
