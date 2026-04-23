# Solución Comentada — Proyecto Final

> Esta solución es una guía de referencia, no la única respuesta correcta.
> Hay múltiples formas válidas de resolver el mismo problema.

---

## Paso a Paso: Cómo Debería Haber Ido

### Fase 1 y 2: Preparación

El prompt correcto para crear el proyecto de ejemplo:

```
> Crea la siguiente estructura de proyecto para practicar code review:

  proyecto-ejemplo/
  ├── auth.py       (con SQL injection y MD5 débil)
  ├── processing.py (con nombres crípticos y sin type hints)
  └── api.py        (sin validación de entrada)

  También crea:
  - CLAUDE.md que explique el propósito del proyecto
  - .claude/settings.json con permisos para leer todo
    y escribir en *.md y proyecto-ejemplo/**
```

**Por qué funciona:** Ser específico sobre la estructura y el tipo de problemas que quieres guía a Claude a crear exactamente lo que necesitas.

---

### Fase 4: Prompt de Orquestación COWORK

El prompt más efectivo para lanzar la revisión:

```
> Lanza una revisión completa de proyecto-ejemplo/ usando el
  siguiente plan de COWORK:

  1. Lanza SIMULTÁNEAMENTE (en paralelo) estos 3 agentes Explore:
     - Agente A: Lee auth.py. Reporta TODOS los problemas de
       seguridad con: nombre del problema, línea, severidad (CRÍTICO/ALTO/MEDIO)
       y fix recomendado.
     - Agente B: Lee processing.py. Reporta problemas de calidad:
       nombres crípticos, falta de type hints, complejidad,
       magic numbers, docstrings faltantes.
     - Agente C: Lee api.py. Reporta: falta de validación,
       posibles excepciones no controladas, endpoints sin documentar.

  2. Cuando los 3 terminen, combina sus resultados en report.md
     con la estructura:
     - Resumen ejecutivo (tabla)
     - Problemas críticos primero
     - Cada problema con: descripción, ubicación, fix

  3. Informa cuántos problemas encontró cada agente.
```

**Por qué funciona:** El prompt especifica exactamente qué debe reportar cada agente (auto-contenido), ordena el paralelismo explícitamente y define el formato del output.

---

### Análisis de los Problemas en el Código de Ejemplo

#### auth.py — Problemas Esperados

```
PROBLEMA 1: SQL Injection
Línea: 6
Código malo:
  query = f"SELECT * FROM users WHERE username='{username}'"
  
Por qué es peligroso:
  Si username = "admin'--", la query se convierte en:
  SELECT * FROM users WHERE username='admin'--'
  Lo que omite la verificación de contraseña.

Fix correcto:
  query = "SELECT * FROM users WHERE username = ?"
  result = conn.execute(query, (username,))

─────────────────────────────────────────────────

PROBLEMA 2: Hashing débil (MD5)
Línea: 10
Código malo:
  hashed = hashlib.md5(password.encode()).hexdigest()

Por qué es peligroso:
  MD5 es criptográficamente roto. Las contraseñas MD5
  pueden crackearse en segundos con tablas rainbow.

Fix correcto:
  import bcrypt
  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

─────────────────────────────────────────────────

PROBLEMA 3: Sin control de acceso
Línea: 16
Código malo:
  def get_admin_panel(user_id):
      # Sin verificación de permisos

Fix correcto:
  def get_admin_panel(user_id):
      if not is_admin(user_id):
          raise PermissionError("Acceso denegado")
      ...
```

#### processing.py — Problemas Esperados

```
PROBLEMA 1: Nombres crípticos
  p(d, t) → debería ser filtrar_y_aplicar_iva(datos, umbral)
  r → resultado
  i → elemento

PROBLEMA 2: Magic numbers
  i * 1.21 → IVA = 1.21; i * IVA

PROBLEMA 3: Except genérico
  except: → except ZeroDivisionError:

PROBLEMA 4: Sin type hints ni docstrings
  def p(d, t): →
  def filtrar_y_aplicar_iva(datos: list[float], umbral: float) -> list[float]:
      """Filtra valores por encima del umbral y aplica IVA (21%)."""
```

#### api.py — Problemas Esperados

```
PROBLEMA 1: Sin validación de entrada
  data = request.json
  result = process(data['value'])  # KeyError si 'value' no existe

Fix correcto:
  if not request.json or 'value' not in request.json:
      return jsonify({'error': 'Campo value requerido'}), 400
  data = request.json

PROBLEMA 2: Sin documentación de endpoints
  @app.route('/data', methods=['POST'])
  # Sin docstring, sin descripción del contrato de la API
```

---

### Los Fixes Correctos

#### Fix completo de auth.py

```python
import sqlite3
import bcrypt


def login(username: str, password: str) -> dict | None:
    """Autentica un usuario. Devuelve el usuario o None."""
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username = ?"
    result = conn.execute(query, (username,))
    user = result.fetchone()
    
    if user is None:
        return None
    
    stored_hash = user['password_hash'].encode()
    if bcrypt.checkpw(password.encode(), stored_hash):
        return user
    return None


def get_admin_panel(user_id: int) -> list:
    """Devuelve la configuración de admin. Solo para administradores."""
    if not _is_admin(user_id):
        raise PermissionError(f"Usuario {user_id} no tiene permisos de admin")
    
    conn = sqlite3.connect('users.db')
    return conn.execute("SELECT * FROM admin_config").fetchall()


def _is_admin(user_id: int) -> bool:
    """Verifica si el usuario tiene rol de administrador."""
    conn = sqlite3.connect('users.db')
    result = conn.execute(
        "SELECT role FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return result is not None and result['role'] == 'admin'
```

#### Fix completo de processing.py

```python
IVA_RATE = 1.21


def filtrar_y_aplicar_iva(datos: list[float], umbral: float) -> list[float]:
    """
    Filtra valores por encima del umbral y aplica IVA del 21%.
    
    Args:
        datos: Lista de precios antes de IVA
        umbral: Solo procesa precios mayores a este valor
    
    Returns:
        Lista de precios filtrados con IVA aplicado
    """
    resultado = []
    for elemento in datos:
        if elemento > umbral:
            resultado.append(elemento * IVA_RATE)
    return resultado


def dividir_seguro(dividendo: float, divisor: float) -> float | None:
    """Divide dos números. Devuelve None si el divisor es cero."""
    try:
        return dividendo / divisor
    except ZeroDivisionError:
        return None
```

---

### Cómo Debería Verse el report.md Final

```markdown
# Informe de Code Review — proyecto-ejemplo/

**Fecha:** 2026-04-23
**Archivos revisados:** 3
**Total de problemas:** 10

## Resumen Ejecutivo

| Categoría     | Problemas | Severidad Máxima |
|--------------|-----------|-----------------|
| Seguridad     | 3         | CRÍTICO          |
| Calidad       | 4         | MEDIO            |
| Validación    | 2         | ALTO             |
| Documentación | 1         | BAJO             |

## Problemas Críticos de Seguridad

### 1. SQL Injection — auth.py:6
**Severidad:** CRÍTICO
**Descripción:** Input de usuario concatenado directamente en SQL.
**Fix aplicado:** Consultas parametrizadas con `?`.

### 2. Hashing débil (MD5) — auth.py:10
**Severidad:** CRÍTICO
**Fix aplicado:** Reemplazado por bcrypt con salt automático.

### 3. Sin control de acceso — auth.py:16
**Severidad:** CRÍTICO
**Fix aplicado:** Verificación de rol antes de acceder a datos admin.

## Problemas de Calidad

### 4. Nombres crípticos — processing.py:3
**Fix aplicado:** Renombradas variables y función.

### 5. Magic numbers — processing.py:6
**Fix aplicado:** Constante IVA_RATE = 1.21 definida.

[... continúa ...]

## Estado Final

| Problema | Estado |
|---------|--------|
| SQL Injection | RESUELTO |
| MD5 débil | RESUELTO |
| Sin permisos | RESUELTO |
| Nombres crípticos | RESUELTO |
| Magic numbers | RESUELTO |
| Except genérico | RESUELTO |
| Sin type hints | RESUELTO |
| Sin validación API | RESUELTO |
| Sin docstrings | PARCIAL |
| Sin tests | PENDIENTE |
```

---

## Lecciones Clave del Proyecto

```
1. ESPECIFICIDAD → Prompts específicos = resultados precisos
   "Analiza seguridad" es peor que
   "Busca: SQL injection, XSS, IDOR, weak crypto en auth.py"

2. CONTEXTO EN SUB-AGENTES → Cada sub-agente necesita su contexto
   No asumas que "sabe" lo que está haciendo el orquestador

3. PARALELISMO CUANDO APLICA → Las 3 revisiones eran independientes
   → paralelo. La combinación dependía de las 3 → secuencial

4. REVISA SIEMPRE LOS DIFFS → Claude puede equivocarse
   Especialmente en fixes de seguridad, SIEMPRE revisa el código

5. COWORK NO ES MAGIA → Úsalo para lo que sirve:
   tareas grandes, paralelas, especializadas.
   Para 3 archivos pequeños, 1 agente hubiera bastado también.
```

---

## ¡Felicidades!

Has completado el curso completo de Claude Code y COWORK.

```
╔══════════════════════════════════════════════════════════╗
║            DIPLOMA DE COMPLETITUD                        ║
║                                                          ║
║   Has aprendido:                                         ║
║   ✅ Instalación y configuración de Claude Code          ║
║   ✅ Funcionalidades core: leer, editar, debuggear       ║
║   ✅ Características avanzadas: Hooks, MCP, Settings     ║
║   ✅ COWORK: orquestación multi-agente                   ║
║   ✅ Proyecto real aplicando todo lo anterior            ║
║                                                          ║
║   Recursos para seguir aprendiendo:                      ║
║   • Documentación oficial de Claude Code                 ║
║   • Repositorio de ejemplos de MCP Servers               ║
║   • Comunidad de Claude Code en Discord                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

**→ Volver al [Índice del Curso](../../README.md)**
