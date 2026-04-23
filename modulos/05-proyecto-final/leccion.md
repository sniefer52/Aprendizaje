# Módulo 5 — Proyecto Final: El Asistente de Code Review

> **Nivel:** Avanzado | **Duración estimada:** 90 minutos
> **Objetivo:** Aplicar TODO lo aprendido en un proyecto real: usar Claude Code para construir un sistema de revisión de código automática con COWORK.

---

## 5.1 Descripción del Proyecto

Vas a crear un **sistema de revisión de código automático** que:

1. Analiza un repositorio completo
2. Detecta problemas de seguridad, calidad y rendimiento
3. Genera un informe detallado en Markdown
4. Aplica algunos fixes automáticamente
5. Usa COWORK para hacerlo de forma paralela y eficiente

```
┌──────────────────────────────────────────────────────────────┐
│           SISTEMA DE CODE REVIEW AUTOMÁTICO                  │
│                                                              │
│  INPUT:   Un directorio con código Python                    │
│                                                              │
│  PROCESO: COWORK multi-agente                                │
│    ├── Agente 1: Análisis de seguridad                       │
│    ├── Agente 2: Análisis de calidad de código               │
│    ├── Agente 3: Búsqueda de tests faltantes                 │
│    └── Agente 4: Verificación de documentación               │
│                                                              │
│  OUTPUT:  report.md con hallazgos y recomendaciones          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 5.2 Fases del Proyecto

### Fase 1: Preparación del Entorno

**Lo que harás:**

```bash
# 1. Crea el directorio del proyecto
mkdir mi-code-reviewer
cd mi-code-reviewer

# 2. Inicia Claude Code
claude
```

**Dentro de Claude Code:**
```
> Crea la estructura inicial del proyecto:
  - Un directorio "proyecto-ejemplo/" con 3 archivos Python
    con código intencionalmente imperfecto (bugs de seguridad,
    falta de tests, código sin documentar)
  - Un archivo CLAUDE.md que describe el proyecto
  - Un archivo .claude/settings.json con los permisos necesarios
```

Claude creará un proyecto de ejemplo para que puedas practicar la revisión.

---

### Fase 2: Configurar el Entorno

**settings.json a crear en `.claude/`:**

```json
{
  "permissions": {
    "allow": [
      "Bash(find *)",
      "Bash(grep *)",
      "Bash(python *)",
      "Bash(pytest *)",
      "Read(**)",
      "Write(*.md)",
      "Write(proyecto-ejemplo/**)"
    ]
  },
  "env": {
    "PYTHONPATH": ".",
    "REVIEW_OUTPUT": "report.md"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '✅ Revisión completada. Consulta report.md'"
          }
        ]
      }
    ]
  }
}
```

**CLAUDE.md a crear:**

```markdown
# Code Reviewer Automático

## Descripción
Sistema que analiza código Python y genera informes de revisión.

## Proyecto de Ejemplo
El directorio `proyecto-ejemplo/` contiene código Python con
problemas intencionales para practicar la revisión.

## Cómo Ejecutar la Revisión
Pide a Claude: "Lanza la revisión completa del proyecto-ejemplo/"

## Output Esperado
El resultado se guarda en report.md
```

---

### Fase 3: El Código de Ejemplo (Con Problemas Intencionales)

Pide a Claude que cree estos archivos con problemas intencionales:

**`proyecto-ejemplo/auth.py`** — Con vulnerabilidades de seguridad:
```python
import sqlite3
import hashlib

def login(username, password):
    # BUG: SQL Injection vulnerability
    conn = sqlite3.connect('users.db')
    query = f"SELECT * FROM users WHERE username='{username}'"
    result = conn.execute(query)
    
    # BUG: Weak hashing (MD5)
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    # BUG: No manejo de errores
    user = result.fetchone()
    return user

def get_admin_panel(user_id):
    # BUG: Sin verificación de permisos
    conn = sqlite3.connect('users.db')
    return conn.execute("SELECT * FROM admin_config").fetchall()
```

**`proyecto-ejemplo/processing.py`** — Con problemas de calidad:
```python
# Sin docstrings ni type hints
def p(d, t):  # Nombres de variables crípticos
    r = []
    for i in d:
        if i > t:  # Magic number sin constante
            r.append(i * 1.21)  # ¿Qué es 1.21?
    return r

def calcular(x):
    try:
        return 100 / x
    except:  # BUG: Except demasiado amplio
        return None

def big_function(data):  # Función de 60+ líneas sin dividir
    # ... (lógica muy larga)
    pass
```

**`proyecto-ejemplo/api.py`** — Sin tests ni documentación:
```python
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    # Sin validación de entrada
    data = request.json
    result = process(data['value'])  # KeyError posible
    return jsonify({'result': result})

def process(value):
    return value * 2
```

---

### Fase 4: Lanzar la Revisión COWORK

Este es el corazón del proyecto. Pide a Claude:

```
> Lanza una revisión completa con COWORK de la carpeta
  proyecto-ejemplo/. Usa agentes paralelos para:
  1. Encontrar vulnerabilidades de seguridad
  2. Analizar calidad del código (nombres, complejidad, docstrings)
  3. Identificar tests faltantes
  4. Revisar manejo de errores
  
  Al final, combina todos los hallazgos en report.md
```

Claude orquestará 4 sub-agentes en paralelo y luego combinará los resultados.

---

### Fase 5: Interpretar el Informe

El `report.md` generado tendrá esta estructura:

```markdown
# Informe de Code Review — proyecto-ejemplo/

## Resumen Ejecutivo
| Categoría    | Problemas encontrados | Severidad |
|-------------|----------------------|-----------|
| Seguridad    | 3                    | CRÍTICO   |
| Calidad      | 5                    | MEDIO     |
| Tests        | 2                    | ALTO      |
| Documentación| 4                    | BAJO      |

## Seguridad — Problemas Críticos

### 1. SQL Injection en auth.py:7
**Severidad:** CRÍTICO
**Descripción:** Concatenación directa de input de usuario en SQL
**Fix recomendado:** Usar consultas parametrizadas

### 2. Hashing débil (MD5) en auth.py:11
...

## Calidad de Código
...

## Tests Faltantes
...

## Recomendaciones Generales
...
```

---

### Fase 6: Aplicar Fixes Automáticos

Para los problemas que Claude puede solucionar automáticamente:

```
> Aplica los siguientes fixes en proyecto-ejemplo/:
  1. Corrige el SQL Injection en auth.py usando consultas parametrizadas
  2. Cambia MD5 por bcrypt para el hashing de contraseñas
  3. Añade type hints y docstrings a processing.py
  4. Añade validación de entrada en api.py
```

Claude editará los archivos directamente y mostrará los diffs para tu revisión.

---

### Fase 7: Verificación Final

```
> Revisa los cambios que hiciste y confirma:
  1. ¿Los fixes no rompieron ninguna funcionalidad existente?
  2. ¿Hay tests que cubran los casos corregidos?
  3. Actualiza report.md con el estado final (problemas resueltos vs pendientes)
```

---

## 5.3 Checklist de Completitud

Usa esta lista para verificar que completaste el proyecto:

```
PREPARACIÓN:
[ ] Directorio mi-code-reviewer creado
[ ] Proyecto de ejemplo creado con código imperfecto
[ ] CLAUDE.md configurado
[ ] settings.json configurado con permisos correctos

EJECUCIÓN COWORK:
[ ] 4 sub-agentes lanzados en paralelo
[ ] Cada agente analizó su área
[ ] Orquestador combinó resultados
[ ] report.md generado correctamente

FIXES:
[ ] SQL Injection corregido
[ ] Hashing débil reemplazado
[ ] Type hints añadidos
[ ] Validación de entrada implementada

VERIFICACIÓN:
[ ] report.md actualizado con estado final
[ ] Los fixes no introdujeron nuevos bugs
```

---

## 5.4 Lo que Practicaste en Este Proyecto

```
╔═══════════════════════════════════════════════════════════╗
║        HABILIDADES APLICADAS EN EL PROYECTO FINAL         ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Módulo 1:  Instalación y primer uso                      ║
║    ✅ Iniciaste Claude Code en un proyecto nuevo           ║
║    ✅ Creaste CLAUDE.md con contexto del proyecto          ║
║                                                           ║
║  Módulo 2:  Funcionalidades core                          ║
║    ✅ Leíste y analizaste archivos de código               ║
║    ✅ Debuggeaste vulnerabilidades                         ║
║    ✅ Editaste código existente (fixes)                    ║
║                                                           ║
║  Módulo 3:  Características avanzadas                     ║
║    ✅ Configuraste settings.json con permisos              ║
║    ✅ Usaste hooks para notificación de fin                ║
║                                                           ║
║  Módulo 4:  COWORK multi-agente                           ║
║    ✅ Orquestaste 4 agentes en paralelo                    ║
║    ✅ Combinaste resultados de múltiples agentes           ║
║    ✅ Usaste agentes especializados (Explore, Plan)        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 5.5 Extensiones del Proyecto (Opcional)

Si quieres ir más lejos, prueba estas extensiones:

**Extensión 1:** Integración con GitHub
```
> Configura el MCP de GitHub y haz que el sistema
  cree automáticamente issues en GitHub para cada
  vulnerabilidad encontrada
```

**Extensión 2:** Slash Command personalizado
```
Crea .claude/commands/review.md para que puedas
hacer /review en cualquier proyecto futuro
```

**Extensión 3:** Hook de pre-commit
```
Configura un hook PostToolUse en Bash que ejecute
automáticamente el code reviewer antes de cada commit
```

---

## Siguiente Paso

**→ [Ver la solución comentada](solucion.md)** — si te atascas en algún punto

**¡Felicidades por completar el curso!** Ahora tienes las herramientas para usar Claude Code y COWORK de forma productiva en tus proyectos reales.
