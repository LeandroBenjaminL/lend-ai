# Workflow: Go Testing

## Flujo principal

```
Orchestrator → [1. Analizar código] → [2. Elegir patrón de test] → [3. Escribir tests] → [4. Verificar cobertura] → [5. Integrar golden files] → [6. Validar] → Orchestrator
```

## Paso a paso

### 1. Analizar el código a testear

Antes de escribir un test, entendés qué estás testeando y cómo se comporta.

- **¿Es una función pura?** (misma entrada → misma salida, sin side effects) → table-driven test simple.
- **¿Tiene side effects?** (llama a DB, filesystem, API externa) → necesitás interfaces y mocks.
- **¿Devuelve error?** → test de success + error case para cada input relevante.
- **¿Es un modelo de TUI Bubbletea?** → test de state transitions, key handlers, view rendering.
- **¿Es lógica compleja?** → partila en funciones más chicas y testeables primero.

_"Si una función es difícil de testear, el problema no es el test — es la función. Partila en funciones más chicas, cada una con una responsabilidad clara."_

### 2. Elegir el patrón de test

Usás el árbol de decisión para elegir el patrón:

```
Testing a function?
├── Pure function? → Table-driven test
├── Has side effects? → Mock dependencies via interfaces
├── Returns error? → Test both success and error cases
└── Complex logic? → Break into smaller testable units

Testing TUI component?
├── State change? → Test Model.Update() directly
├── Full flow? → Use teatest.NewTestModel()
├── Visual output? → Use golden file testing
└── Key handling? → Send tea.KeyMsg

Testing system/exec?
├── Mock os/exec? → Interface + mock
├── Real commands? → Integration test with -short skip
└── File operations? → Use t.TempDir()
```

**Tabla de patrones:**

| Patrón | Cuándo | Herramienta |
|--------|--------|-------------|
| Table-driven | Funciones puras con múltiples casos | `testing.T` + `t.Run()` |
| Mock con interfaces | Dependencias externas | Interfaces de 1-2 métodos |
| Golden file | Output visual (vistas, renders) | `testdata/*.golden` + `-update` flag |
| teatest | Flujos completos de TUI | `charmbracelet/teatest` |
| State transition | Modelos que cambian de estado | `Model.Update()` directo |
| Integration | Operaciones reales de sistema | `testing.Short()` skip |

### 3. Escribir los tests

**Table-driven tests (el pan de cada día):**

```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {
            name:     "valid input",
            input:    "hello",
            expected: "HELLO",
            wantErr:  false,
        },
        {
            name:     "empty input",
            input:    "",
            expected: "",
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := ProcessInput(tt.input)

            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if result != tt.expected {
                t.Errorf("got %q, want %q", result, tt.expected)
            }
        })
    }
}
```

**Reglas del table-driven:**
- Cada test case tiene un `name` descriptivo.
- Los campos mínimos son `name`, `input`, `expected`, y `wantErr` (si aplica).
- Usá `t.Run()` para cada caso — así cuando falla, sabés EXACTAMENTE qué caso falló.
- El `wantErr` se evalúa con `(err != nil) != tt.wantErr` — no comparés strings de error.
- Cubrí: caso feliz, caso borde, caso de error, caso límite.

**Mocking con interfaces:**

```go
// En producción
type FileReader interface {
    Read(path string) ([]byte, error)
}

// En tests
type mockReader struct {
    data []byte
    err  error
}

func (m *mockReader) Read(path string) ([]byte, error) {
    return m.data, m.err
}
```

**Reglas de mocking:**
- Interfaces de 1-2 métodos — si tu interfaz tiene 10 métodos, está mal diseñada.
- Mock manual en el archivo de test — no frameworks mágicos.
- El mock es la representación más simple posible de la dependencia.

**Tests de Bubbletea:**

```go
func TestModelUpdate(t *testing.T) {
    m := NewModel()

    // Simular key press
    newModel, _ := m.Update(tea.KeyMsg{Type: tea.KeyEnter})
    m = newModel.(Model)

    if m.Screen != ScreenMainMenu {
        t.Errorf("expected ScreenMainMenu, got %v", m.Screen)
    }
}
```

**Reglas de TUI testing:**
- Probá state transitions individuales con `Model.Update()`.
- Probá renders con golden files (no assertés strings literales largos).
- Probá flujos completos con `teatest.NewTestModel()`.
- No probés timing o animaciones exactas.

**Tests con teatest (flujos completos):**

```go
func TestInteractiveFlow(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m)

    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
    tm.Send(tea.KeyMsg{Type: tea.KeyDown})
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})

    tm.WaitFinished(t, teatest.WithDuration(time.Second))

    finalModel := tm.FinalModel(t).(Model)

    if finalModel.Screen != ExpectedScreen {
        t.Errorf("wrong screen: got %v", finalModel.Screen)
    }
}
```

### 4. Verificar cobertura y completitud

Después de escribir los tests, verificás:

- [ ] **Cobertura de casos base:** ¿El caso feliz está cubierto?
- [ ] **Cobertura de errores:** ¿Cada error posible tiene un test case?
- [ ] **Cobertura de bordes:** ¿Input vacío, nil, máximo, mínimo?
- [ ] **Casos de regresión:** Si esto es un fix, ¿el test falla sin el fix?
- [ ] **Nombres descriptivos:** ¿Cada test case tiene un nombre que explica QUÉ prueba?
- [ ] **Sin t.Fatal() en goroutines:** Usá `t.Error()` en vez de `t.Fatal()` cuando puedas seguir.
- [ ] **Parallel cuando aplica:** `t.Parallel()` para tests independientes.

**Qué NO verificar:**
- No obsesionarse con % de cobertura (80% está bien, 100% es sospechoso).
- No testear getters/setters triviales.
- No testear código de terceros.
- No testear lo que el compilador ya verifica (tipos, sintaxis).

### 5. Golden file testing (para renders y outputs)

Cuando el output es un string largo (como una vista de TUI), usás golden files:

```go
func TestViewGolden(t *testing.T) {
    m := NewModel()
    m.Screen = ScreenOSSelect
    m.Width = 80
    m.Height = 24

    output := m.View()

    golden := filepath.Join("testdata", "TestViewGolden.golden")

    if *update {
        os.WriteFile(golden, []byte(output), 0644)
    }

    expected, _ := os.ReadFile(golden)
    if output != string(expected) {
        t.Errorf("output doesn't match golden file")
    }
}
```

**Reglas de golden files:**
- Los archivos van en `testdata/` (Go ignora ese directorio en builds).
- El flag `-update` regenera los golden files cuando el comportamiento cambia INTENCIONALMENTE.
- Siempre commit actualización de golden files junto con el cambio de comportamiento.
- Si el golden cambia sin que cambies el comportamiento, algo está mal.

### 6. Organizar y validar

**Estructura de archivos de test:**

```
internal/tui/
├── model.go
├── model_test.go           # Tests de modelo
├── update.go
├── update_test.go          # Tests de update handler
├── view.go
├── view_test.go            # Tests de view rendering
├── teatest_test.go         # Tests de integración TUI
└── testdata/
    ├── TestOSSelectGolden.golden
    └── TestViewGolden.golden
```

**Reglas de organización:**
- Cada archivo `_test.go` al lado del archivo que testea, en el mismo package.
- Los golden files en `testdata/` (subdirectorio).
- Si un archivo de test pasa de 200 líneas, partilo por tema.
- Los helpers van al final del archivo o en un `helpers_test.go` separado.

**Comandos de verificación:**

```bash
go test ./...                           # Todos los tests
go test -v ./internal/tui/...          # Tests de un paquete
go test -run TestCursorNavigation       # Test específico
go test -cover ./...                    # Con cobertura
go test -update ./...                   # Actualizar golden files
go test -short ./...                    # Saltar integración
```

### Output final

Tu entregable al orchestrator es:

1. **Archivos de test** escritos con el patrón correcto según cada caso
2. **Golden files** si hay renders o outputs visuales
3. **Instrucciones de ejecución** (`go test ./...`, `go test -update` si aplica)

_"Un buen test no es el que pasa siempre. Es el que cuando falla, te dice exactamente qué función se rompió, con qué input, y qué esperabas."_
