# 📖 Glosario — Claude Code & COWORK

> Aquí encontrarás todos los términos técnicos usados en el curso, explicados en lenguaje sencillo.

---

## A

### Agent (Agente)
Un programa autónomo que usa un modelo de IA para tomar decisiones y ejecutar acciones. En Claude Code, los agentes pueden leer archivos, escribir código, buscar en internet y colaborar con otros agentes.

```
┌─────────────────────────────┐
│           AGENTE            │
│                             │
│  Recibe tarea               │
│      │                      │
│      ▼                      │
│  Planifica pasos            │
│      │                      │
│      ▼                      │
│  Ejecuta con herramientas   │
│      │                      │
│      ▼                      │
│  Devuelve resultado         │
└─────────────────────────────┘
```

### Agent SDK (Kit de Desarrollo de Agentes)
Conjunto de herramientas y APIs que permiten construir y orquestar agentes de IA. Claude Code lo usa internamente para su sistema multi-agente (COWORK).

### API (Application Programming Interface)
Interfaz que permite que dos programas se comuniquen. La API de Anthropic es la "puerta de entrada" para hablar con Claude desde cualquier aplicación.

### API Key (Clave de API)
Contraseña secreta que identifica tu cuenta al usar la API de Anthropic. Nunca la compartas públicamente.

```
Usuario ──[API Key]──→ Anthropic API ──→ Claude
```

---

## B

### Bash
La terminal de comandos de Linux/Mac. Claude Code se ejecuta dentro de Bash.

---

## C

### CLI (Command Line Interface)
Interfaz de línea de comandos. Se usa escribiendo texto en la terminal. Claude Code es un CLI.

```
Editor gráfico  ←→  Interfaz visual (clics, botones)
Claude Code     ←→  Interfaz de texto (comandos escritos)
```

### Claude Code
El CLI oficial de Anthropic que te permite interactuar con Claude directamente desde la terminal para tareas de desarrollo de software.

### Context (Contexto)
La información que Claude tiene disponible durante una conversación: los mensajes anteriores, los archivos leídos, el historial de herramientas usadas.

### COWORK
Modelo de trabajo colaborativo donde múltiples agentes de Claude trabajan juntos. Un agente "orquestador" delega sub-tareas a agentes especializados.

```
┌─────────────────────────────────────────┐
│           COWORK OVERVIEW               │
│                                         │
│  [Agente Principal / Orquestador]       │
│         │           │         │         │
│         ▼           ▼         ▼         │
│   [Sub-Agente]  [Sub-Agente] [Sub-Agente]│
│   Explorar      Planificar   Ejecutar   │
└─────────────────────────────────────────┘
```

---

## D

### Diff
La diferencia entre dos versiones de un archivo. Claude Code muestra diffs cuando edita código para que puedas ver exactamente qué cambió.

---

## E

### Environment Variable (Variable de Entorno)
Variable configurada en el sistema operativo que los programas pueden leer. `ANTHROPIC_API_KEY` es el ejemplo más común en Claude Code.

---

## F

### Fork
Copia de un repositorio. En el contexto de agentes, un "worktree" es similar: una copia aislada donde el agente trabaja sin afectar el código principal.

---

## G

### Git
Sistema de control de versiones que rastrea cambios en archivos. Claude Code lo usa frecuentemente para gestionar código.

### GLOB Pattern
Patrón para encontrar archivos. Por ejemplo: `src/**/*.ts` significa "todos los archivos `.ts` dentro de `src/` y sus subcarpetas".

---

## H

### Hook
Función que se ejecuta automáticamente cuando ocurre un evento específico en Claude Code. Permite personalizar el comportamiento de Claude.

```
Eventos disponibles:
├── PreToolUse    → Antes de que Claude use una herramienta
├── PostToolUse   → Después de que Claude use una herramienta
├── Notification  → Cuando Claude envía una notificación
└── Stop          → Cuando Claude termina de responder
```

---

## I

### IDE (Integrated Development Environment)
Entorno de desarrollo integrado. VS Code y JetBrains son ejemplos. Claude Code puede integrarse con ellos.

---

## J

### JSON (JavaScript Object Notation)
Formato de texto para representar datos estructurados. El archivo `settings.json` de Claude Code usa este formato.

```json
{
  "clave": "valor",
  "número": 42,
  "lista": ["a", "b", "c"]
}
```

---

## L

### LLM (Large Language Model)
Modelo de Lenguaje Grande. Claude es un LLM. Son modelos de IA entrenados con enormes cantidades de texto.

---

## M

### MCP (Model Context Protocol)
Protocolo estándar que permite a Claude conectarse con herramientas y servicios externos (bases de datos, APIs, aplicaciones).

```
Claude Code
    │
    ├──[MCP]──→ GitHub (leer/escribir issues, PRs)
    ├──[MCP]──→ Base de datos (ejecutar consultas)
    ├──[MCP]──→ Slack (enviar mensajes)
    └──[MCP]──→ Google Drive (acceder a documentos)
```

### MCP Server (Servidor MCP)
El programa que implementa el protocolo MCP y expone las herramientas de un servicio externo a Claude.

### Modelo
La versión específica del sistema de IA. Ejemplos: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`.

---

## O

### Orquestador
El agente principal que divide un trabajo grande en sub-tareas y las delega a sub-agentes especializados.

---

## P

### Permission Mode (Modo de Permisos)
Configuración que controla qué acciones puede hacer Claude automáticamente sin pedirte confirmación.

### Prompt
El texto que le envías a Claude como instrucción o pregunta.

---

## R

### REPL (Read-Eval-Print Loop)
Modo interactivo donde escribes un comando, el programa lo evalúa y muestra el resultado. Claude Code funciona como un REPL conversacional.

### Repository (Repositorio)
Carpeta gestionada por Git que contiene tu proyecto y su historial de cambios.

---

## S

### Session (Sesión)
Una conversación completa con Claude Code, desde que la inicias hasta que la terminas. El contexto se mantiene durante la sesión.

### Settings (Configuración)
Archivo `settings.json` donde puedes personalizar el comportamiento de Claude Code: permisos, hooks, variables de entorno, etc.

### Slash Command
Comando especial que empieza con `/` dentro de Claude Code. Ejemplo: `/help`, `/clear`, `/compact`.

### Sub-Agente
Agente secundario creado por el orquestador para realizar una tarea específica. Opera de forma aislada y reporta sus resultados al orquestador.

---

## T

### Tool (Herramienta)
Capacidad específica que Claude puede usar: leer archivos (`Read`), ejecutar comandos (`Bash`), editar código (`Edit`), buscar en la web (`WebSearch`), etc.

### Token
Unidad básica de texto que procesa el LLM. Aproximadamente 1 token = 0.75 palabras en inglés. Los modelos tienen límites de tokens por conversación.

---

## W

### Worktree
Copia aislada de un repositorio Git donde un agente puede trabajar sin afectar la rama principal. Se usa en el modo de aislamiento del Agent SDK.

### Workspace
El directorio de trabajo actual de Claude Code. Todo lo que Claude ve y puede editar está dentro del workspace.

---

*¿Falta algún término? Busca en la lección correspondiente o abre un issue en el repositorio.*
