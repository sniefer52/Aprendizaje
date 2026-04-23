# Módulo 3 — Características Avanzadas de Claude Code

> **Nivel:** Intermedio | **Duración estimada:** 50 minutos
> **Objetivo:** Dominar Hooks, Slash Commands, MCP Servers, Settings y la integración con IDEs.

---

## 3.1 Visión General del Módulo

```
┌──────────────────────────────────────────────────────────────┐
│             CARACTERÍSTICAS AVANZADAS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  HOOKS          →  Acciones automáticas en respuesta a       │
│                    eventos de Claude Code                    │
│                                                              │
│  SLASH COMMANDS →  Comandos especiales con /                 │
│                    para control rápido                       │
│                                                              │
│  MCP SERVERS    →  Conectar Claude a servicios externos      │
│                    (GitHub, Slack, bases de datos...)        │
│                                                              │
│  SETTINGS       →  Personalizar permisos, entorno           │
│                    y comportamiento                          │
│                                                              │
│  IDE INTEGRATION →  Usar Claude Code dentro de              │
│                     VS Code o JetBrains                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 3.2 Hooks — Automatizaciones en Respuesta a Eventos

### ¿Qué son los hooks?

Los hooks son **scripts que se ejecutan automáticamente** cuando Claude Code hace algo. Son como "gatillos" o "disparadores" — si ocurre el evento X, ejecuta el comando Y.

```
EVENTO OCURRE                        HOOK SE EJECUTA
     │                                      │
     ▼                                      ▼
Claude va a usar Bash  ──[PreToolUse]──→  echo "Ejecutando comando"
Claude termina Bash    ──[PostToolUse]──→  ejecuta_validaciones.sh
Claude termina mensaje ──[Stop]──────────→ notifica_en_slack.sh
```

### Ciclo de Vida de los Hooks

```
┌─────────────────────────────────────────────────────────────┐
│                 CICLO DE VIDA DE CLAUDE CODE                │
│                                                             │
│  Usuario escribe mensaje                                    │
│           │                                                 │
│           ▼                                                 │
│     Claude planifica                                        │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  PreToolUse      │ ← Hook ANTES de usar una herramienta │
│  └──────────────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│   Claude usa la herramienta (Read, Bash, Edit...)           │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  PostToolUse     │ ← Hook DESPUÉS de usar herramienta   │
│  └──────────────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│     Claude responde                                         │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  Stop            │ ← Hook cuando Claude TERMINA          │
│  └──────────────────┘                                       │
│           │                                                 │
│  ┌──────────────────┐                                       │
│  │  Notification    │ ← Hook cuando Claude envía notif.    │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

### Configurar Hooks en settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[LOG] Claude va a ejecutar un comando Bash'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "git add -A && git status"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '✅ Claude terminó su respuesta'"
          }
        ]
      }
    ]
  }
}
```

### Casos de Uso Prácticos de Hooks

| Evento | Hook útil | Para qué sirve |
|--------|-----------|---------------|
| `PreToolUse(Bash)` | Registrar en log | Auditar qué comandos ejecuta Claude |
| `PostToolUse(Write)` | `git add` automático | Que los cambios queden staged automáticamente |
| `PostToolUse(Edit)` | Ejecutar linter | Validar formato del código tras editar |
| `Stop` | Notificación de Slack | Avisar que Claude terminó una tarea larga |
| `Notification` | Sonido o vibración | Alerta cuando Claude necesita atención |

> 💡 **Tip:** Los hooks son ejecutados por el sistema, no por Claude. Esto significa que Claude no puede "saltárselos" — son una capa de control externa.

---

## 3.3 Slash Commands — Control Rápido

Los slash commands son comandos especiales disponibles dentro de Claude Code. Empiezan siempre con `/`.

### Comandos Esenciales

| Comando | Descripción | Cuándo usarlo |
|---------|-------------|--------------|
| `/help` | Muestra ayuda con todos los comandos disponibles | Cuando no recuerdas algo |
| `/clear` | Limpia la pantalla del terminal | Para tener más espacio visual |
| `/compact` | Comprime el historial para liberar contexto | Sesiones largas o lentas |
| `/status` | Muestra modelo activo, versión y estado de sesión | Para verificar configuración |
| `/init` | Genera `CLAUDE.md` automáticamente analizando el proyecto | Al empezar en un proyecto nuevo |
| `/review` | Lanza revisión multi-agente del branch actual (COWORK) | Antes de hacer un PR |
| `/fast` | Activa modo rápido (Opus en modo acelerado) | Para respuestas más veloces |

### Slash Commands de Usuario (Personalizados)

Puedes crear tus propios slash commands en `.claude/commands/`:

```
.claude/
└── commands/
    ├── deploy.md        →  /deploy
    ├── run-tests.md     →  /run-tests
    └── check-style.md   →  /check-style
```

Ejemplo de `deploy.md`:
```markdown
# Deploy a producción

Ejecuta los siguientes pasos para hacer deploy:
1. Asegúrate de que los tests pasan: `pytest`
2. Construye el proyecto: `npm run build`
3. Sube a producción: `git push heroku main`
4. Verifica que el servicio esté up: `curl https://mi-app.com/health`
```

Ahora puedes usar `/deploy` en cualquier sesión de Claude Code y él ejecutará ese flujo.

---

## 3.4 MCP Servers — Conectar Claude al Mundo

### ¿Qué es MCP?

MCP (Model Context Protocol) es un estándar que permite a Claude conectarse a servicios externos. Es como darle a Claude acceso a herramientas adicionales.

```
SIN MCP:                           CON MCP:
                                   
Claude solo puede:                 Claude puede:
- Leer archivos locales            - Leer archivos locales
- Ejecutar comandos                - Ejecutar comandos
- Buscar en internet               - Buscar en internet
                                   - Crear issues en GitHub
                                   - Enviar mensajes en Slack
                                   - Consultar tu base de datos
                                   - Acceder a Google Drive
                                   - Ver calendarios
                                   - Y mucho más...
```

### Arquitectura de MCP

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Claude Code                                           │
│       │                                                 │
│       ├──[MCP]──→ GitHub MCP Server                    │
│       │               └── Herramientas: create_issue,  │
│       │                   list_PRs, merge_PR...         │
│       │                                                 │
│       ├──[MCP]──→ Slack MCP Server                     │
│       │               └── Herramientas: send_message,  │
│       │                   list_channels...              │
│       │                                                 │
│       ├──[MCP]──→ Google Drive MCP Server              │
│       │               └── Herramientas: read_file,     │
│       │                   list_files, create_file...   │
│       │                                                 │
│       └──[MCP]──→ Tu MCP Server personalizado          │
│                       └── Herramientas: lo que quieras │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Configurar un MCP Server

En tu `settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_tutoken..."
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-tutoken..."
      }
    }
  }
}
```

### Usar MCP en la Conversación

Una vez configurado, simplemente pides:

```
Tú:    "Crea un issue en GitHub en el repositorio mi-org/mi-repo
        con el título 'Bug en login' y el body [descripción del bug]"

Claude: [Usa la herramienta mcp__github__create_issue]
        
        "Issue creado exitosamente:
         URL: https://github.com/mi-org/mi-repo/issues/42"
```

---

## 3.5 Settings — Configuración Detallada

El archivo `settings.json` controla el comportamiento de Claude Code.

### Dónde viven los settings

```
JERARQUÍA DE CONFIGURACIÓN (de más general a más específico):

~/
└── .claude/
    └── settings.json   ← Configuración GLOBAL (afecta a todos tus proyectos)

tu-proyecto/
└── .claude/
    └── settings.json   ← Configuración LOCAL (solo afecta a este proyecto)

El archivo LOCAL tiene prioridad sobre el GLOBAL.
```

### Estructura Completa de settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Bash(pytest *)",
      "Read(**)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  },

  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint --fix"
          }
        ]
      }
    ]
  },

  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    }
  },

  "env": {
    "NODE_ENV": "development",
    "DEBUG": "true"
  }
}
```

### Sistema de Permisos

```
FORMATO DE PERMISO:  HerramientaNombre(patrón)

Ejemplos:
  "Read(**)"             →  Permitir leer CUALQUIER archivo
  "Read(src/**)"         →  Solo leer archivos dentro de src/
  "Bash(npm *)"          →  Solo comandos npm
  "Bash(git add *)"      →  Solo git add
  "Write(*.md)"          →  Solo escribir archivos .md

  "deny": ["Bash(rm *)"] →  NUNCA ejecutar rm
```

---

## 3.6 Integración con IDEs

Claude Code puede usarse directamente dentro de tu editor favorito.

### VS Code

```
Instalación:
1. Abre VS Code
2. Ve a Extensions (Ctrl+Shift+X)
3. Busca "Claude Code"
4. Instala la extensión oficial de Anthropic

Una vez instalada:
- Abre el panel de Claude Code con Ctrl+Shift+C
- Claude tiene acceso a tu workspace abierto
- Puedes seleccionar código y preguntarle sobre él
- Claude puede editar directamente los archivos abiertos
```

### JetBrains (IntelliJ, PyCharm, WebStorm...)

```
Instalación:
1. Ve a File → Settings → Plugins
2. Busca "Claude Code" en el marketplace
3. Instala y reinicia el IDE

Uso:
- Panel de Claude en la barra lateral
- Clic derecho en código → "Ask Claude"
- Acceso a contexto del proyecto completo
```

### Ventajas de la integración con IDE

```
Sin integración:                Con integración:
                                
Terminal ←─ Claude ─→ Editor   Claude DENTRO del editor
                                
- Cambias constantemente        - Todo en una sola ventana
  entre ventanas                - Claude ve el código
- Copias y pegas código           que tienes seleccionado
- Menos contexto visual         - Integración con debugger
                                - Acceso al árbol de archivos
```

---

## 3.7 Atajos de Teclado Personalizados

Puedes personalizar los atajos de teclado en `~/.claude/keybindings.json`:

```json
[
  {
    "key": "ctrl+shift+enter",
    "command": "submit"
  },
  {
    "key": "ctrl+k",
    "command": "clear"
  },
  {
    "key": "escape",
    "command": "interrupt"
  }
]
```

---

## 3.8 Resumen Visual

```
╔═══════════════════════════════════════════════════════════╗
║         CARACTERÍSTICAS AVANZADAS — RESUMEN               ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  HOOKS                                                    ║
║    PreToolUse  → Antes de que Claude use una herramienta  ║
║    PostToolUse → Después de usar la herramienta           ║
║    Stop        → Cuando Claude termina                    ║
║    Notification→ Cuando Claude notifica                   ║
║    Configurados en: settings.json > "hooks"               ║
║                                                           ║
║  SLASH COMMANDS                                           ║
║    /help /clear /compact /status /init /review /fast     ║
║    Personalizados en: .claude/commands/*.md               ║
║                                                           ║
║  MCP SERVERS                                              ║
║    Conectan Claude a servicios externos                   ║
║    GitHub, Slack, Drive, bases de datos, etc.             ║
║    Configurados en: settings.json > "mcpServers"          ║
║                                                           ║
║  SETTINGS                                                 ║
║    Global:  ~/.claude/settings.json                       ║
║    Local:   .claude/settings.json (tiene prioridad)       ║
║    Controla: permisos, hooks, MCPs, env vars              ║
║                                                           ║
║  IDE INTEGRATION                                          ║
║    VS Code y JetBrains via extensión/plugin               ║
║    Claude dentro de tu editor favorito                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Siguiente Paso

**→ [Autoevaluación del Módulo 3](autoevaluacion.md)**

**→ [Módulo 4: COWORK Multi-Agente](../04-cowork-multiagente/leccion.md)** — el poder de los agentes colaborativos
