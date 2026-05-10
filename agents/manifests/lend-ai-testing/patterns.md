# Lend.Ai Testing — Patterns

## Patrón de test unitario (Python)

```python
def test_calcular_total_con_descuento():
    items = [Item(price=100), Item(price=200)]
    result = calcular_total(items, descuento=10)

    assert result == 270.0
```

## Patrón de test con fixture (pytest)

```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()

def test_usuario_creado(db_session):
    usuario = Usuario(nombre="test")
    db_session.add(usuario)
    db_session.commit()
    assert db_session.query(Usuario).count() == 1
```

## Patrón de test frontend (Testing Library)

```tsx
describe("LoginForm", () => {
  it("muestra error si el email es inválido", () => {
    render(<LoginForm />)
    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "invalido" },
    })
    fireEvent.click(screen.getByText("Ingresar"))
    expect(screen.getByText("Email inválido")).toBeInTheDocument()
  })
})
```

## Patrón de GitHub Actions (completo con lint + test + security)

```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install ruff
      - run: ruff check .

  test:
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}" }
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements*') }}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=src --cov-fail-under=80 --cov-report=xml
      - uses: codecov/codecov-action@v4
        with: { files: ./coverage.xml }

  security:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: pip-audit
```

## Patrón de workflow simple (para proyectos chicos)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: pytest --cov=src --cov-fail-under=80
```

## Anti-patrones

- Tests que no afirman nada (no `assert True`)
- Mockear todo hasta que el test no pruebe nada real
- Tests que dependen del orden de ejecución
- Snapshots gigantes que nadie revisa
- Coverage bajo sin justificación
- CI con `continue-on-error: true` permanentemente
- Un solo job gigante que mezcla lint + test + deploy
- No cachear dependencias (cada run baja todo de nuevo)
