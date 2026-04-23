# ⚡ Cheatsheet — Referencia Rápida Claude Code & COWORK

> Una sola página con todo lo que necesitas recordar.

---

## 🖥️ Comandos de Instalación y Arranque

```bash
# Instalar Claude Code
npm install -g @anthropic-ai/claude-code

# Configurar tu API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# Iniciar Claude Code (modo interactivo)
claude

# Iniciar en un directorio específico
claude --dir /ruta/a/tu/proyecto

# Una sola pregunta sin modo interactivo
claude -p "¿Qué hace este archivo?"

# Ver versión
claude --version

# Ver ayuda
claude --help
```

---

## 💬 Slash Commands (dentro de Claude Code)

| Comando | Qué hace |
|---------|----------|
| `/help` | Muestra la ayuda |
| `/clear` | Limpia la pantalla |
| `/compact` | Comprime el historial para liberar contexto |
| `/status` | Muestra el estado actual del modelo y sesión |
| `/review` | Lanza una revisión multi-agente del branch actual |
| `/init` | Crea un archivo `CLAUDE.md` con documentación del proyecto |
| `/fast` | Activa el modo rápido (Claude Opus en modo acelerado) |

---

## 🔧 Herramientas (Tools) que usa Claude

| Herramienta | Acción |
|-------------|--------|
| `Read` | Lee un archivo |
| `Write` | Crea o sobreescribe un archivo |
| `Edit` | Edita partes específicas de un archivo |
| `Bash` | Ejecuta comandos de terminal |
| `WebSearch` | Busca en internet |
| `WebFetch` | Descarga el contenido de una URL |
| `Agent` | Lanza un sub-agente (COWORK) |
| `TodoWrite` | Crea y gestiona lista de tareas |

---

## 📁 Archivos Clave de Configuración

```
Tu directorio de trabajo/
├── CLAUDE.md              ← Instrucciones del proyecto para Claude
└── .claude/
    └── settings.json      ← Configuración local del proyecto

Tu home (~)/
└── .claude/
    ├── settings.json      ← Configuración global de usuario
    └── keybindings.json   ← Atajos de teclado personalizados
```

---

## ⚙️ settings.json — Estructura

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Read(**)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Ejecutando comando...'"
          }
        ]
      }
    ]
  },
  "env": {
    "MI_VARIABLE": "valor"
  }
}
```

---

## 🔗 Hooks — Eventos Disponibles

| Evento | Cuándo se dispara |
|--------|--------------------|
| `PreToolUse` | Antes de que Claude use cualquier herramienta |
| `PostToolUse` | Después de que Claude use una herramienta |
| `Notification` | Cuando Claude envía una notificación al usuario |
| `Stop` | Cuando Claude termina de responder |

---

## 🤖 COWORK — Tipos de Agentes Especializados

| Tipo de Agente | Especialidad |
|----------------|--------------|
| `Explore` | Explorar y buscar en el codebase rápidamente |
| `Plan` | Diseñar arquitectura e implementación |
| `general-purpose` | Investigación y tareas multi-paso |
| `claude-code-guide` | Preguntas sobre Claude Code y el SDK |

---

## 🤖 COWORK — Cómo Lanzar un Sub-Agente

```python
# Desde Python usando el SDK de Anthropic
Agent({
  "description": "Descripción breve de la tarea",
  "subagent_type": "Explore",   # o Plan, general-purpose, etc.
  "prompt": "Instrucciones detalladas del trabajo...",
  "run_in_background": False    # True para ejecutar en paralelo
})
```

---

## 🔄 Patrones COWORK

```
SECUENCIAL (una tarea depende de la anterior):
[Agente A] ──→ resultado ──→ [Agente B] ──→ resultado ──→ [Agente C]

PARALELO (tareas independientes al mismo tiempo):
                    ┌──→ [Agente A]
[Orquestador] ──→ ──┼──→ [Agente B]  (todos al mismo tiempo)
                    └──→ [Agente C]
                         │
                    [Recoge resultados]
```

---

## 🌐 Variables de Entorno Importantes

| Variable | Descripción |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Tu clave de API de Anthropic |
| `ANTHROPIC_BASE_URL` | URL base alternativa (proxies) |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Límite de tokens en respuestas |

---

## ⌨️ Atajos de Teclado (dentro de Claude Code)

| Atajo | Acción |
|-------|--------|
| `Ctrl+C` | Interrumpir la respuesta actual |
| `Ctrl+L` | Limpiar la pantalla |
| `↑` / `↓` | Navegar historial de mensajes |
| `Shift+Enter` | Nueva línea sin enviar |
| `Enter` | Enviar mensaje |

---

## 🏷️ Modelos Claude (más recientes)

| Modelo | Velocidad | Capacidad | Uso ideal |
|--------|-----------|-----------|-----------|
| `claude-opus-4-7` | Lento | Máxima | Tareas complejas |
| `claude-sonnet-4-6` | Medio | Alta | Uso general |
| `claude-haiku-4-5` | Rápido | Buena | Tareas simples |

---

## 💡 Tips Rápidos

```
✅ Sé específico en tus instrucciones → mejores resultados
✅ Usa CLAUDE.md para dar contexto permanente del proyecto
✅ /compact cuando la sesión se vuelve lenta (contexto lleno)
✅ Usa sub-agentes para tareas grandes e independientes
✅ Revisa siempre los cambios antes de confirmar (git diff)
⚠️  Nunca pongas tu API key en archivos que subirás a git
⚠️  Configura permisos mínimos necesarios en settings.json
```

---

*Para más detalle sobre cualquier tema: ver los módulos del curso.*
