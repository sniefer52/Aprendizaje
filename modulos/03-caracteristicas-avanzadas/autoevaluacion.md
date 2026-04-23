# 🎯 Autoevaluación — Módulo 3: Características Avanzadas

> Responde las preguntas sin mirar la lección. Luego comprueba tus respuestas abajo.
> Tiempo estimado: 10 minutos

---

## Preguntas

### Pregunta 1
¿Qué hace el hook `PostToolUse` configurado para la herramienta `Edit`?

- A) Se ejecuta antes de que Claude edite un archivo
- B) Se ejecuta después de que Claude edite un archivo
- C) Previene que Claude edite archivos
- D) Registra qué archivos están disponibles para editar

---

### Pregunta 2
¿Para qué sirven los MCP Servers?

- A) Para acelerar las respuestas de Claude
- B) Para conectar Claude con servicios externos como GitHub, Slack o bases de datos
- C) Para guardar el historial de conversaciones
- D) Para instalar plugins de Claude Code

---

### Pregunta 3
Tienes dos archivos `settings.json`: uno en `~/.claude/` y otro en `.claude/` de tu proyecto. ¿Cuál tiene prioridad?

- A) El global (`~/.claude/settings.json`) siempre tiene prioridad
- B) El local (`.claude/settings.json` del proyecto) tiene prioridad
- C) Se mezclan y ambos tienen la misma prioridad
- D) El que se editó más recientemente tiene prioridad

---

### Pregunta 4
¿Cómo crearías un slash command personalizado llamado `/deploy`?

- A) Escribiendo `/define deploy` dentro de Claude Code
- B) Añadiéndolo a la sección `"commands"` del `settings.json`
- C) Creando el archivo `.claude/commands/deploy.md`
- D) Ejecutando `claude --register-command deploy`

---

### Pregunta 5
¿Cuál de estos patrones de permiso permite a Claude ejecutar `npm install` y `npm run build`, pero NO `npm publish`?

- A) `"Bash(npm *)"`
- B) `"Bash(npm install)", "Bash(npm run *)"`
- C) `"Bash(npm install *)", "Bash(npm run build)"`
- D) `"Bash(npm)", "deny": ["Bash(npm publish)"]`

---

## 🏆 Reto Práctico

Crea un `settings.json` local para un proyecto imaginario con estas reglas:

```
1. Permitir: todos los comandos git
2. Permitir: ejecutar npm run test y npm run build
3. Denegar: cualquier comando rm
4. Hook PostToolUse en Edit: ejecuta "npm run lint"
5. Variable de entorno: NODE_ENV = "test"
```

Escribe el JSON antes de ver la solución.

<details>
<summary>Ver solución del reto</summary>

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm run test)",
      "Bash(npm run build)"
    ],
    "deny": [
      "Bash(rm *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint"
          }
        ]
      }
    ]
  },
  "env": {
    "NODE_ENV": "test"
  }
}
```

</details>

---

## Respuestas y Explicaciones

<details>
<summary>👉 Haz clic aquí para ver las respuestas del quiz</summary>

### Respuesta 1: ✅ B
**Se ejecuta DESPUÉS de que Claude edite un archivo.**

`PostToolUse` significa "después de usar la herramienta". Es el momento ideal para ejecutar validaciones, linters, o registrar qué se cambió. El hook recibe información sobre qué herramienta se usó y en qué archivo.

---

### Respuesta 2: ✅ B
**Para conectar Claude con servicios externos.**

MCP (Model Context Protocol) es el puente entre Claude y el mundo exterior. Sin MCP, Claude solo puede trabajar con archivos locales y comandos. Con MCP puede interactuar con cualquier API o servicio que tenga un servidor MCP implementado.

---

### Respuesta 3: ✅ B
**El local (`.claude/settings.json` del proyecto) tiene prioridad.**

La configuración local sobreescribe la global cuando hay conflicto. Esto permite tener configuración general para todos tus proyectos en `~/.claude/settings.json` y sobreescribir solo lo específico en cada proyecto.

---

### Respuesta 4: ✅ C
**Creando el archivo `.claude/commands/deploy.md`.**

Los slash commands personalizados son archivos Markdown en `.claude/commands/`. El nombre del archivo (sin `.md`) se convierte en el comando. El contenido del archivo es el prompt que Claude ejecutará cuando uses ese comando.

---

### Respuesta 5: ✅ B
**`"Bash(npm install)", "Bash(npm run *)"`**

- `Bash(npm *)` permitiría CUALQUIER comando npm, incluyendo `npm publish`
- `"Bash(npm install)", "Bash(npm run *)"` permite exactamente `npm install` y cualquier `npm run <algo>` (como `npm run build`, `npm run test`, etc.) pero no `npm publish`

---

### Tu puntuación:
```
  5/5  Excelente! Las características avanzadas están claras.
  4/5  Muy bien. Revisa lo que fallaste.
  3/5  Repasa las secciones 3.2 a 3.5 antes de continuar.
  2/5  Vuelve a leer la lección completa.
  1/5  Repasa desde el módulo 2.
```

</details>

---

**→ Cuando tengas 4 o más respuestas correctas: [Módulo 4 — COWORK Multi-Agente](../04-cowork-multiagente/leccion.md)**
