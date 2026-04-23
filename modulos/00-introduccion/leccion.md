# Módulo 0 — Introducción: El Ecosistema de Claude

> **Nivel:** Principiante absoluto | **Duración estimada:** 20 minutos
> **Objetivo:** Entender qué es Claude Code y COWORK, para qué sirven y cómo encajan en el ecosistema de IA.

---

## 0.1 ¿Dónde estamos?

Antes de aprender *cómo* usar Claude Code, necesitamos entender *qué* es y *por qué* existe.

Imagina que tienes un asistente de programación superinteligente. Puedes hablar con él en lenguaje natural, pedirle que lea tu código, lo edite, lo ejecute, busque errores, etc. Eso es exactamente lo que es Claude Code.

```
Sin Claude Code:            Con Claude Code:
                            
Tú ──→ Terminal             Tú ──→ Claude Code ──→ Terminal
Tú ──→ Editor               Tú ──→ Claude Code ──→ Editor
Tú ──→ Buscador            Tú ──→ Claude Code ──→ Internet
Tú ──→ Documentación       Tú ──→ Claude Code ──→ Docs

(Tú haces todo)             (Claude hace el trabajo técnico,
                             tú supervisas y guías)
```

---

## 0.2 El Ecosistema Completo

```
╔═══════════════════════════════════════════════════════════════╗
║                  ECOSISTEMA DE CLAUDE                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌─────────────────────────────────────────────────────┐     ║
║  │                  ANTHROPIC                          │     ║
║  │  Crea y entrena los modelos Claude (la IA)          │     ║
║  └─────────────────────────┬───────────────────────────┘     ║
║                            │                                  ║
║                  ┌─────────▼─────────┐                       ║
║                  │   ANTHROPIC API   │                       ║
║                  │  (puerta de acceso│                       ║
║                  │   a Claude)       │                       ║
║                  └─────────┬─────────┘                       ║
║                            │                                  ║
║         ┌──────────────────┼──────────────────┐              ║
║         │                  │                  │              ║
║  ┌──────▼──────┐  ┌────────▼───────┐  ┌──────▼──────┐      ║
║  │ Claude.ai   │  │  Claude Code   │  │ Tu propia   │      ║
║  │ (web chat)  │  │  (CLI / SDK)   │  │ app con API │      ║
║  └─────────────┘  └───────┬────────┘  └─────────────┘      ║
║                            │                                  ║
║                   ┌────────▼────────┐                        ║
║                   │     COWORK      │                        ║
║                   │ (multi-agente)  │                        ║
║                   └─────────────────┘                        ║
╚═══════════════════════════════════════════════════════════════╝
```

### Los tres niveles:

| Nivel | Herramienta | ¿Para quién? | ¿Qué puedes hacer? |
|-------|------------|--------------|---------------------|
| 1 | **Claude.ai** (web) | Cualquier persona | Chatear con Claude |
| 2 | **Claude Code** (CLI) | Desarrolladores | Programar con IA asistida |
| 3 | **COWORK** (multi-agente) | Avanzado | Orquestar equipos de IA |

---

## 0.3 ¿Qué es Claude Code exactamente?

Claude Code es un **CLI** (programa de línea de comandos) que instalas en tu ordenador. Cuando lo abres, puedes:

1. **Hablar con Claude** en lenguaje natural
2. **Claude lee tu código** automáticamente cuando se lo pides
3. **Claude edita archivos** directamente en tu proyecto
4. **Claude ejecuta comandos** en tu terminal
5. **Claude busca** en internet cuando lo necesita

```
┌────────────────────────────────────────────────┐
│              TU TERMINAL                        │
│                                                 │
│  $ claude                                       │
│                                                 │
│  > Hola, ¿puedes revisar el archivo main.py    │
│    y decirme si tiene errores?                  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Claude lee main.py...                   │  │
│  │  Encontré 2 problemas:                   │  │
│  │  1. Línea 15: variable sin definir       │  │
│  │  2. Línea 32: división por cero posible  │  │
│  │  ¿Quieres que los corrija?               │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  > Sí, corrígelos por favor                     │
│                                                 │
│  [Claude edita main.py directamente]            │
└────────────────────────────────────────────────┘
```

---

## 0.4 ¿Qué es COWORK?

COWORK es la capacidad de Claude Code de crear **equipos de agentes** que trabajan juntos. Es como tener un equipo de programadores IA, cada uno especializado en algo.

```
                     TÚ
                      │
                      ▼
          ┌───────────────────────┐
          │  AGENTE PRINCIPAL     │
          │  (Orquestador)        │
          │  "El jefe de equipo"  │
          └──────────┬────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Agente  │  │ Agente  │  │ Agente  │
   │Explorar │  │Planificar│  │Ejecutar │
   │"Busca   │  │"Diseña  │  │"Escribe │
   │el bug"  │  │la fix"  │  │el código│
   └─────────┘  └─────────┘  └─────────┘
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
               Resultado final
```

### ¿Por qué es útil?

| Situación | Sin COWORK | Con COWORK |
|-----------|-----------|-----------|
| Analizar 100 archivos | Claude lee uno a uno | Múltiples agentes en paralelo |
| Tarea larga compleja | Un agente puede "olvidar" el inicio | El orquestador mantiene el hilo |
| Revisión de código | Una perspectiva | Múltiples perspectivas especializadas |
| Investigar + implementar | Secuencial, lento | Simultáneo, rápido |

---

## 0.5 ¿Cómo se relacionan Claude Code y COWORK?

```
CLAUDE CODE  es la herramienta base
     │
     ├── Puedes usarlo solo (1 agente)
     │     → Para tareas cotidianas de programación
     │
     └── Puedes activar COWORK (múltiples agentes)
           → Para tareas complejas que requieren
             paralelismo o especialización
```

> 💡 **Analogía:** Claude Code es como tener un asistente. COWORK es como tener un equipo entero. Usas el equipo cuando la tarea es demasiado grande para una sola persona.

---

## 0.6 Casos de Uso Reales

### Claude Code (un solo agente):
- "Refactoriza esta función para que sea más legible"
- "Añade tests unitarios a este módulo"
- "Explícame qué hace este código"
- "Hay un bug en producción, encuéntralo y arréglalo"

### COWORK (multi-agente):
- "Revisa toda mi aplicación y dame un informe de seguridad"
- "Migra este proyecto de JavaScript a TypeScript"
- "Implementa esta nueva feature grande desde cero"
- "Analiza el rendimiento de mi app y optimízala"

---

## 0.7 Resumen Visual del Módulo

```
╔═══════════════════════════════════════════════════╗
║              LO QUE APRENDISTE HOY                ║
╠═══════════════════════════════════════════════════╣
║                                                   ║
║  Anthropic                                        ║
║    └── Crea Claude (el modelo de IA)              ║
║                                                   ║
║  Claude.ai                                        ║
║    └── Interfaz web para chatear                  ║
║                                                   ║
║  Claude Code (CLI)                                ║
║    └── Programa para programar con IA             ║
║    └── Lee, edita y ejecuta código                ║
║    └── Se usa desde la terminal                   ║
║                                                   ║
║  COWORK (multi-agente)                            ║
║    └── Equipos de agentes especializados          ║
║    └── Para tareas grandes y complejas            ║
║    └── Paralelo y eficiente                       ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

---

## Siguiente Paso

Ahora que entiendes el panorama general, es hora de ponerse manos a la obra.

**→ [Autoevaluación del Módulo 0](autoevaluacion.md)** — comprueba que entendiste los conceptos

**→ [Módulo 1: Primeros Pasos](../01-primeros-pasos/leccion.md)** — instala Claude Code y úsalo por primera vez
