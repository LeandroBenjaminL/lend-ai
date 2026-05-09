---
name: go-testing
description: >
  Patrones de testing en Go para Gentleman.Dots, incluyendo TUI con Bubbletea.
  Trigger: Cuando escribís tests en Go, usás teatest, o agregás cobertura.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T3-balanced
---

# Skill: go-testing

Escribir tests en Go que sean rápidos, legibles y que prueben lo correcto.

## Trigger

- Estás escribiendo tests unitarios en Go.
- Probás componentes TUI de Bubbletea.
- Necesitás table-driven tests, golden files o teatest.

## Por qué existe

Los tests en Go tienen una cultura muy definida: tablas, subtests, sin
frameworks mágicos. Si los escribís con la estructura correcta desde el
principio, son fáciles de leer, mantener y extender. Si no, terminás con
tests frágiles que nadie entiende.

## Workflow para cada test

```
1. Identificá qué estás probando: ¿función pura, side effect, o TUI?
2. Función pura → table-driven test con casos: normal, edge, error
3. Side effects → mockeá dependencias, testéá estados
4. TUI → probá Model.Update() directo o teatest para flujos completos
5. Output visual → golden file testing
6. Corré: go test ./...
```

## Patrones

### 1. Table-driven tests (para funciones puras)

```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {name: "válido", input: "hola", expected: "HOLA", wantErr: false},
        {name: "vacío", input: "", expected: "", wantErr: true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test logic
        })
    }
}
```

**Por qué**: un test por caso con `t.Run()` da reports claros de qué falló.
Agregar un caso nuevo es agregar una línea a la tabla, no copiar todo el test.

### 2. Bubbletea: test de modelo directo

Probá transiciones de estado sin levantar la TUI:

```go
func TestScreenTransitions(t *testing.T) {
    m := Model{Screen: ScreenWelcome}
    newM, _ := m.Update(tea.KeyMsg{Type: tea.KeyEnter})
    m = newM.(Model)
    if m.Screen != ScreenMainMenu {
        t.Errorf("screenshot = %v, want MainMenu", m.Screen)
    }
}
```

**Por qué**: testear `Model.Update()` directamente es más rápido y predecible
que una integración con teatest. Usalo para lógica de estado pura.

### 3. Teatest (para flujos completos)

```go
func TestFullFlow(t *testing.T) {
    tm := teatest.NewTestModel(t, NewModel())
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
    tm.WaitFinished(t, teatest.WithDuration(time.Second))
    final := tm.FinalModel(t).(Model)
    // assert final state
}
```

**Por qué**: teatest simula al usuario. Usalo para flujos completos, no para
cada transición individual.

### 4. Golden files (para output visual)

```go
func TestViewGolden(t *testing.T) {
    m := Model{Width: 80, Height: 24}
    output := m.View()
    golden := filepath.Join("testdata", t.Name()+".golden")
    if *update { os.WriteFile(golden, []byte(output), 0644) }
    expected, _ := os.ReadFile(golden)
    if output != string(expected) {
        t.Errorf("output no coincide con golden file")
    }
}
```

**Por qué**: comparar contra un archivo guardado evita tener strings enormes
en el código del test. El flag `-update` regenera los golden files cuando
cambiás intencionalmente el output.

## Organización de archivos

```
internal/tui/
├── model.go / model_test.go     # Tests de modelo
├── update.go / update_test.go   # Tests de update handlers
├── view.go / view_test.go       # Golden tests de view
├── teatest_test.go              # Integración TUI completa
├── testdata/
│   ├── TestOSSelectGolden.golden
│   └── TestViewGolden.golden
└── trainer/
    ├── types_test.go
    └── exercises_test.go
```

## Comandos

```bash
go test ./...                    # Todo
go test -v -run TestScreen       # Test específico
go test -update ./...            # Regenerar golden files
go test -short ./...             # Saltar integración
go test -cover ./...             # Con cobertura
```

## Anti-patrones

- Testear implementación en vez de comportamiento → tests frágiles que rompen
  con cualquier refactor.
- Un solo test enorme sin subtests → cuando falla, no sabés qué caso falló.
- No testear casos de error → el código vive en un mundo ideal.
- Usar teatest para todo → es más lento y frágil que testear `Model.Update()` directo.
- Poner golden files en el mismo directorio que el código → mezcla test data con source.
- No usar `-short` para tests de integración → nadie va a esperar 30 segundos
  para correr tests unitarios.
