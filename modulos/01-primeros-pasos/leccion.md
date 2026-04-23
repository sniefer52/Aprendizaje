# Módulo 1 — Primeros Pasos con Claude Code

> **Nivel:** Principiante | **Duración estimada:** 30 minutos
> **Objetivo:** Instalar Claude Code, configurarlo y tener tu primera conversación productiva.

---

## 1.1 Requisitos del Sistema

Antes de instalar, comprueba que tienes todo lo necesario:

```
┌──────────────────────────────────────────────────────────┐
│                  CHECKLIST DE REQUISITOS                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Sistema Operativo:                                      │
│  ✅ macOS 12 o superior                                  │
│  ✅ Linux (Ubuntu 20.04+, Debian 11+, etc.)              │
│  ✅ Windows 11 (vía WSL2)                                │
│                                                          │
│  Software:                                               │
│  [ ] Node.js v18 o superior  →  node --version          │
│  [ ] npm v8 o superior       →  npm --version            │
│  [ ] Git (recomendado)       →  git --version            │
│                                                          │
│  Cuenta:                                                 │
│  [ ] Cuenta en console.anthropic.com                    │
│  [ ] API Key de Anthropic                               │
│  [ ] Créditos o suscripción activa                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### ¿Cómo verificar Node.js?

Abre tu terminal y escribe:
```bash
node --version
# Debería mostrar algo como: v20.11.0
```

Si no tienes Node.js, descárgalo desde [nodejs.org](https://nodejs.org) (elige la versión LTS).

---

## 1.2 Obtener tu API Key

```
Paso 1: Ve a console.anthropic.com
        │
        ▼
Paso 2: Crea una cuenta o inicia sesión
        │
        ▼
Paso 3: En el menú izquierdo, busca "API Keys"
        │
        ▼
Paso 4: Haz clic en "Create Key"
        │
        ▼
Paso 5: Copia y guarda la clave (empieza con sk-ant-)
        │
        ▼
Paso 6: NUNCA la pongas en archivos de código
         que subirás a GitHub u otros repositorios
```

> ⚠️ **Importante:** Tu API Key es como tu contraseña de banco. Guárdala en un lugar seguro y nunca la compartas.

---

## 1.3 Instalación de Claude Code

### Paso 1: Instalar vía npm

```bash
npm install -g @anthropic-ai/claude-code
```

Este comando descarga e instala Claude Code globalmente en tu sistema. Verás muchas líneas de texto mientras se instala — es normal.

### Paso 2: Verificar la instalación

```bash
claude --version
```

Deberías ver algo como `1.x.x`. Si ves un error, consulta la sección de resolución de problemas al final.

### Paso 3: Configurar la API Key

```bash
# Añade esto a tu archivo ~/.bashrc o ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-tu-clave-aqui"
```

Luego recarga tu terminal:
```bash
source ~/.bashrc   # si usas bash
# o
source ~/.zshrc    # si usas zsh
```

> 💡 **Tip:** Para saber qué shell usas, escribe `echo $SHELL`. Si ves `/bin/zsh`, usa `.zshrc`. Si ves `/bin/bash`, usa `.bashrc`.

---

## 1.4 Tu Primera Sesión con Claude Code

¡Ahora viene lo divertido! Vamos a tener nuestra primera conversación.

### Iniciar Claude Code

```bash
claude
```

Verás algo parecido a esto:
```
╔═══════════════════════════════════════╗
║         Claude Code v1.x.x           ║
║   Tips for getting started:           ║
║   1. Ask Claude to create a file     ║
║   2. Ask Claude to explain code      ║
║   3. Type /help for commands         ║
╚═══════════════════════════════════════╝

>
```

El cursor `>` está esperando tu primer mensaje.

### Primeras Conversaciones

Prueba estas conversaciones de menos a más:

**Conversación 1 — Saludo simple:**
```
> Hola, ¿puedes decirme cuánto es 2 + 2?
```

**Conversación 2 — Crear un archivo:**
```
> Crea un archivo llamado hola.txt con el mensaje "¡Hola mundo!"
```

**Conversación 3 — Generar código:**
```
> Crea un archivo hola.py con un programa Python que imprima
  "¡Hola, Claude Code!" y la fecha actual
```

**Conversación 4 — Ejecutar código:**
```
> Ejecuta el archivo hola.py que acabas de crear
```

---

## 1.5 El Flujo de Trabajo Básico

```
┌─────────────────────────────────────────────────────────┐
│               CICLO DE TRABAJO CON CLAUDE CODE          │
│                                                         │
│   1. Tú escribes   →   Claude entiende tu intención     │
│                                                         │
│   2. Claude planifica  →  Decide qué herramientas usar  │
│                                                         │
│   3. Claude ejecuta    →  Usa herramientas (Read, Edit, │
│                           Bash, etc.)                   │
│                                                         │
│   4. Claude informa    →  Te dice qué hizo              │
│                                                         │
│   5. Tú revisas        →  Apruebas o corriges           │
│                                                         │
│   6. Repite            →  Siguiente tarea               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> ⚠️ **Importante:** Claude te pedirá confirmación antes de hacer cambios importantes (como borrar archivos o ejecutar comandos peligrosos). Siempre revisa antes de aprobar.

---

## 1.6 Navegación Básica

Claude Code recuerda en qué directorio estás. Puedes:

```bash
# Abrir Claude Code en tu proyecto actual
cd /ruta/a/tu/proyecto
claude

# O indicar el directorio directamente
claude --dir /ruta/a/tu/proyecto
```

Una vez dentro de Claude Code, puedes decirle:

```
> Muéstrame los archivos que hay en este directorio
> Lee el archivo README.md
> ¿Qué hace el archivo main.py?
> Muéstrame la estructura de carpetas del proyecto
```

---

## 1.7 El Archivo CLAUDE.md

Claude Code busca automáticamente un archivo llamado `CLAUDE.md` en la raíz de tu proyecto. Este archivo es como las "instrucciones permanentes" para Claude.

```bash
# Crear CLAUDE.md automáticamente
> /init
```

O créalo manualmente:

```markdown
# Mi Proyecto

## Descripción
Esta es una API REST en Python con Flask.

## Comandos útiles
- `python app.py` — iniciar el servidor
- `pytest` — ejecutar tests
- `pip install -r requirements.txt` — instalar dependencias

## Convenciones de código
- Usa snake_case para variables y funciones
- Todos los endpoints deben tener docstring
- Los tests van en la carpeta /tests
```

> 💡 **Tip:** Cuanto más detallado sea tu `CLAUDE.md`, más contexto tiene Claude y mejores respuestas da.

---

## 1.8 Controlar el Comportamiento de Claude

### Permisos

Por defecto, Claude te pide confirmación para acciones importantes. Puedes configurar qué acciones son automáticas.

```bash
# Durante la sesión, Claude puede pedir permisos así:
┌─────────────────────────────────────────────┐
│  Claude quiere ejecutar:                    │
│  > npm install express                      │
│                                             │
│  [Aprobar una vez] [Aprobar siempre] [No]  │
└─────────────────────────────────────────────┘
```

### Modos de Permiso

| Modo | Descripción |
|------|-------------|
| **Default** | Claude pide confirmación para acciones potencialmente destructivas |
| **Auto-approve** | Claude ejecuta sin preguntar (más rápido, menos seguro) |

---

## 1.9 Comandos Slash Esenciales

Dentro de Claude Code, estos son los comandos más usados:

| Comando | Cuándo usarlo |
|---------|--------------|
| `/help` | Cuando no recuerdas algo |
| `/clear` | Para limpiar la pantalla |
| `/compact` | Cuando la sesión se vuelve lenta (contexto lleno) |
| `/status` | Para ver el modelo activo y estado |

Para salir de Claude Code:
```
> Ctrl+C   (interrumpe la respuesta actual)
> Ctrl+D   (sale de Claude Code)
```

---

## 1.10 Resolución de Problemas Comunes

```
PROBLEMA: "command not found: claude"
SOLUCIÓN: El PATH no está configurado
  → Prueba: npx @anthropic-ai/claude-code
  → O reinstala con: npm install -g @anthropic-ai/claude-code

PROBLEMA: "API key not found" o "401 Unauthorized"
SOLUCIÓN: La API Key no está configurada correctamente
  → Verifica: echo $ANTHROPIC_API_KEY
  → Debe mostrar tu clave (sk-ant-...)

PROBLEMA: "Insufficient credits"
SOLUCIÓN: Tu cuenta no tiene créditos
  → Ve a console.anthropic.com y añade créditos

PROBLEMA: Claude se pone lento o no responde
SOLUCIÓN: Contexto lleno
  → Usa /compact para comprimir el historial
  → O sal y vuelve a entrar con: claude
```

---

## 1.11 Resumen Visual

```
╔══════════════════════════════════════════════════════╗
║           INSTALACIÓN Y PRIMER USO — RESUMEN         ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  1. node --version  →  Verificar Node.js v18+        ║
║                                                      ║
║  2. npm install -g @anthropic-ai/claude-code         ║
║                     →  Instalar Claude Code          ║
║                                                      ║
║  3. export ANTHROPIC_API_KEY="sk-ant-..."            ║
║                     →  Configurar API Key            ║
║                                                      ║
║  4. claude          →  Abrir Claude Code             ║
║                                                      ║
║  5. /init           →  Crear CLAUDE.md               ║
║                                                      ║
║  6. Habla con Claude en lenguaje natural             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

## Siguiente Paso

**→ [Autoevaluación del Módulo 1](autoevaluacion.md)**

**→ [Módulo 2: Funcionalidades Core](../02-funcionalidades-core/leccion.md)** — aprende a editar código, generar proyectos y debuggear
