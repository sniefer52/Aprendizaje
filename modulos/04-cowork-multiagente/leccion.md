# Módulo 4 — COWORK: Colaboración Multi-Agente

> **Nivel:** Intermedio-Avanzado | **Duración estimada:** 60 minutos
> **Objetivo:** Entender y aplicar el modelo de colaboración multi-agente: orquestadores, sub-agentes, patrones de paralelismo y cuándo usar cada uno.

---

## 4.1 ¿Qué es un Agente?

Un **agente** es una instancia de Claude que puede:
1. Recibir una tarea
2. Planificar los pasos necesarios
3. Usar herramientas (Read, Bash, Edit, WebSearch...)
4. Devolver un resultado

```
┌──────────────────────────────────────────┐
│                 AGENTE                   │
│                                          │
│  Entrada: "Encuentra todos los bugs      │
│            de seguridad en src/"         │
│                   │                      │
│                   ▼                      │
│  Planifica:                              │
│    1. Listar archivos en src/            │
│    2. Leer cada archivo                  │
│    3. Buscar patrones inseguros          │
│    4. Reportar hallazgos                 │
│                   │                      │
│                   ▼                      │
│  Ejecuta usando:  Read, Bash, WebSearch  │
│                   │                      │
│                   ▼                      │
│  Salida: "Encontré 3 vulnerabilidades:   │
│           [lista detallada]"             │
└──────────────────────────────────────────┘
```

---

## 4.2 ¿Qué es COWORK?

COWORK es el patrón donde **un agente principal (orquestador)** lanza y coordina **múltiples sub-agentes** para completar una tarea compleja.

```
PROBLEMA: "Audita toda mi aplicación: seguridad,
           rendimiento y calidad de código"
                        │
                        ▼
           ┌────────────────────────┐
           │   AGENTE PRINCIPAL     │
           │     (Orquestador)      │
           │                        │
           │  Divide en 3 tareas    │
           │  independientes        │
           └──────────┬─────────────┘
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
 ┌──────────┐   ┌──────────┐  ┌──────────┐
 │Sub-Agente│   │Sub-Agente│  │Sub-Agente│
 │Seguridad │   │Rendimiento│  │ Calidad  │
 │          │   │          │  │          │
 │Analiza   │   │Perfila   │  │Revisa    │
 │vulnera-  │   │tiempos de│  │estilo y  │
 │bilidades │   │respuesta │  │tests     │
 └────┬─────┘   └────┬─────┘  └────┬─────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
                     ▼
           ┌─────────────────┐
           │  Orquestador    │
           │  recoge todos   │
           │  los resultados │
           │  y genera el    │
           │  informe final  │
           └─────────────────┘
```

---

## 4.3 Tipos de Agentes Especializados

Claude Code viene con tipos de agentes predefinidos, cada uno optimizado para un tipo de tarea:

| Tipo | Especialidad | Cuándo usarlo |
|------|-------------|---------------|
| `Explore` | Búsqueda y exploración del codebase | Cuando necesitas encontrar archivos, funciones o patrones |
| `Plan` | Diseño de arquitectura e implementación | Cuando necesitas planificar una solución compleja |
| `general-purpose` | Investigación y tareas multi-paso | Para tareas complejas que no encajan en los anteriores |
| `claude-code-guide` | Preguntas sobre Claude Code y el SDK | Cuando tienes dudas sobre la herramienta en sí |

```
¿Qué tipo de agente usar?

   ¿Necesitas encontrar código?    → Explore
              │
   ¿Necesitas diseñar solución?   → Plan
              │
   ¿Es una tarea larga compleja?  → general-purpose
              │
   ¿Preguntas sobre Claude Code?  → claude-code-guide
```

---

## 4.4 Patrones de Colaboración

### Patrón 1: Secuencial (una tarea depende de la anterior)

```
CUÁNDO: El resultado de A es entrada necesaria de B

[Agente A]
Explorar el código
    │
    │ resultado: estructura del proyecto
    ▼
[Agente B]
Planificar la migración
(necesita saber la estructura primero)
    │
    │ resultado: plan detallado
    ▼
[Agente C]
Implementar según el plan
(necesita el plan de B)
    │
    ▼
Resultado final
```

**Ejemplo de código:**
```python
# SECUENCIAL: esperar a que cada agente termine
resultado_explorar = Agent({
    "description": "Explorar estructura del proyecto",
    "subagent_type": "Explore",
    "prompt": "Mapea la estructura completa del proyecto src/"
})

# Esperamos a que explore termine ANTES de planificar
resultado_planificar = Agent({
    "description": "Planificar migración",
    "subagent_type": "Plan",
    "prompt": f"Diseña un plan de migración basado en: {resultado_explorar}"
})
```

### Patrón 2: Paralelo (tareas independientes al mismo tiempo)

```
CUÁNDO: Las tareas no dependen entre sí

                  [Orquestador]
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
    [Agente A]   [Agente B]   [Agente C]
    Analiza      Analiza      Analiza
    src/auth/    src/api/     src/db/
          │            │            │
          └────────────┼────────────┘
                       │
                  Todos terminan
                  (el más lento
                   marca el tiempo)
                       │
                       ▼
              [Orquestador recoge
               y combina resultados]
```

**Ejemplo de código:**
```python
# PARALELO: todos empiezan al mismo tiempo
# Se lanzan en el mismo mensaje (una sola llamada)

# Lanzar los 3 agentes en paralelo:
agente_auth = Agent({
    "description": "Analizar módulo de autenticación",
    "subagent_type": "Explore",
    "prompt": "Analiza src/auth/ y reporta issues de seguridad",
    "run_in_background": True    # ← clave para paralelismo
})

agente_api = Agent({
    "description": "Analizar módulo de API",
    "subagent_type": "Explore",
    "prompt": "Analiza src/api/ y reporta issues de seguridad",
    "run_in_background": True
})

agente_db = Agent({
    "description": "Analizar módulo de base de datos",
    "subagent_type": "Explore",
    "prompt": "Analiza src/db/ y reporta issues de seguridad",
    "run_in_background": True
})

# Los 3 corren simultáneamente → el tiempo total es el del más lento
# (no la suma de los 3)
```

### Comparativa de Patrones

```
SECUENCIAL:           PARALELO:
                      
[A] → [B] → [C]      [A]  [B]  [C]  ← todos al mismo tiempo
                       ↘   ↓   ↙
Tiempo = A + B + C    [resultado]
                      
                      Tiempo = max(A, B, C)
```

---

## 4.5 Cuándo Usar COWORK vs Un Solo Agente

```
¿La tarea requiere COWORK?

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  USAR UN SOLO AGENTE cuando:                            │
│  ─────────────────────────                              │
│  • La tarea es puntual y acotada                        │
│    ("Refactoriza esta función")                         │
│  • El contexto cabe en una sola conversación            │
│  • No hay tareas independientes que paralelizar         │
│  • Es más rápido explicarlo que orquestarlo             │
│                                                         │
│  USAR COWORK cuando:                                    │
│  ─────────────────────────                              │
│  • La tarea es demasiado grande para un contexto        │
│    ("Analiza los 200 archivos del proyecto")            │
│  • Hay sub-tareas independientes → paralelizar          │
│    ("Analiza cada módulo por separado")                 │
│  • Necesitas perspectivas especializadas                │
│    ("Uno explora, otro planifica, otro implementa")     │
│  • La tarea tiene muchos pasos con dependencias claras  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> ⚠️ **Aviso:** No uses COWORK para todo. Añadir sub-agentes tiene un coste: más tiempo de coordinación, más tokens consumidos y más complejidad. Para tareas simples, un solo agente es más eficiente.

---

## 4.6 Aislamiento de Sub-Agentes (Worktrees)

Cuando un sub-agente necesita hacer cambios en el código, puede trabajar en una **copia aislada** (worktree) para no interferir con el trabajo del orquestador.

```
SIN AISLAMIENTO:                  CON AISLAMIENTO (worktree):

[Orquestador] trabaja             [Orquestador] trabaja
en el repositorio                 en el repositorio

[Sub-Agente] también              [Sub-Agente] trabaja en
trabaja en el mismo               una COPIA SEPARADA del repo
repositorio                       (su propio worktree)

→ Riesgo de conflictos            → Sin interferencia
  y sobreescrituras                 Los cambios se integran
                                    al final si se aprueba
```

---

## 4.7 El Flujo Completo de COWORK

Veamos un ejemplo real de extremo a extremo:

```
TAREA: "Revisa toda mi aplicación y dame un informe
        completo de seguridad con fixes aplicados"

PASO 1: Orquestador recibe la tarea
        │
        ▼
PASO 2: Orquestador analiza el proyecto (qué módulos hay)
        │
        ▼
PASO 3: Orquestador lanza sub-agentes en paralelo:
        ├── Sub-Agente "auth": analiza autenticación
        ├── Sub-Agente "api": analiza endpoints
        └── Sub-Agente "db": analiza queries SQL
        │
        ▼
PASO 4: Cada sub-agente trabaja de forma independiente
        y devuelve su reporte al orquestador
        │
        ▼
PASO 5: Orquestador combina los reportes y lanza un
        sub-agente "implementador" para aplicar los fixes
        │
        ▼
PASO 6: Orquestador verifica los fixes y presenta
        el informe final al usuario
```

---

## 4.8 Comunicación entre Agentes

Los sub-agentes se comunican solo a través del orquestador. No hay comunicación directa entre sub-agentes.

```
CORRECTO:                         INCORRECTO:

[Orquestador]                     [Sub-A] ──→ [Sub-B]
   │      │                       
   ▼      ▼                       Los sub-agentes NO se
[Sub-A] [Sub-B]                   hablan directamente.
   │      │                       
   ▼      ▼                       
[Orquestador recoge]              
```

---

## 4.9 Buenas Prácticas COWORK

```
✅ HAZ ESTO:
   • Prompts de sub-agentes auto-contenidos
     (incluyen todo el contexto necesario)
   • Especifica exactamente qué debe devolver cada sub-agente
   • Usa background=True para tareas verdaderamente paralelas
   • Describe el sub-agente en 3-5 palabras (campo description)

⚠️  EVITA ESTO:
   • No crees sub-agentes para tareas triviales
   • No asumas que el sub-agente recuerda tu conversación
     (¡no la ve! Debes pasarle todo en el prompt)
   • No delegues la síntesis al sub-agente
     ("basándote en tus hallazgos, implementa...")
     Tú decides; el sub-agente investiga
```

---

## 4.10 Resumen Visual

```
╔═══════════════════════════════════════════════════════════════╗
║               COWORK MULTI-AGENTE — RESUMEN                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  CONCEPTOS CLAVE:                                             ║
║  • Agente: instancia de Claude que usa herramientas           ║
║  • Orquestador: agente principal que coordina                 ║
║  • Sub-agente: agente secundario con tarea específica         ║
║  • Worktree: copia aislada del repositorio para sub-agentes   ║
║                                                               ║
║  TIPOS DE AGENTES:                                            ║
║  Explore → buscar/analizar código                             ║
║  Plan    → diseñar arquitectura                               ║
║  general-purpose → tareas complejas multi-paso                ║
║                                                               ║
║  PATRONES:                                                    ║
║  Secuencial → A termina, luego empieza B                      ║
║  Paralelo   → A, B y C corren simultáneamente                 ║
║                                                               ║
║  CUÁNDO USAR COWORK:                                          ║
║  • Tarea demasiado grande para un solo contexto              ║
║  • Hay sub-tareas independientes paralelizables               ║
║  • Se necesitan perspectivas especializadas                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Siguiente Paso

**→ [Autoevaluación del Módulo 4](autoevaluacion.md)**

**→ [Módulo 5: Proyecto Final](../05-proyecto-final/leccion.md)** — aplica todo lo aprendido en un proyecto real
