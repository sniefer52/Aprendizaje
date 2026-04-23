# 🎯 Autoevaluación — Módulo 1: Primeros Pasos

> Responde las preguntas sin mirar la lección. Luego comprueba tus respuestas abajo.
> Tiempo estimado: 5-10 minutos

---

## Preguntas

### Pregunta 1
¿Cuál es el comando correcto para instalar Claude Code?

- A) `pip install claude-code`
- B) `npm install -g @anthropic-ai/claude-code`
- C) `brew install claude`
- D) `apt-get install claude-code`

---

### Pregunta 2
¿Dónde debes guardar tu API Key de Anthropic para que Claude Code la encuentre automáticamente?

- A) En un archivo llamado `api_key.txt` en tu directorio de proyecto
- B) Como variable de entorno: `export ANTHROPIC_API_KEY="sk-ant-..."`
- C) En el archivo `settings.json` del proyecto
- D) No es necesario configurarla, Claude Code la solicita cada vez

---

### Pregunta 3
¿Para qué sirve el archivo `CLAUDE.md`?

- A) Para guardar las conversaciones con Claude
- B) Para almacenar la API Key de forma segura
- C) Para dar instrucciones permanentes y contexto del proyecto a Claude
- D) Es el archivo de configuración de instalación

---

### Pregunta 4
¿Qué comando slash usas cuando Claude Code se vuelve lento porque el contexto está lleno?

- A) `/clear`
- B) `/reset`
- C) `/compact`
- D) `/status`

---

### Pregunta 5
¿Cuál de estos mensajes es un ejemplo correcto de cómo interactuar con Claude Code?

- A) `--create-file --name=hola.py --content="print('hola')"`
- B) `Crea un archivo hola.py que imprima "Hola mundo"`
- C) `python -m claude create hola.py`
- D) `claude.create("hola.py", "print('hola')")`

---

## Reto Práctico

Antes de ver las respuestas, intenta hacer esto en tu terminal:

```
1. Abre Claude Code: claude
2. Pide a Claude que cree una carpeta llamada "mi-primer-proyecto"
3. Pide a Claude que dentro de esa carpeta cree un archivo
   "saludo.py" que imprima tu nombre
4. Pide a Claude que ejecute ese archivo
5. Cierra Claude Code con Ctrl+D
```

Si lo lograste: ¡excelente! Ya tienes el flujo básico dominado.

---

## Respuestas y Explicaciones

<details>
<summary>👉 Haz clic aquí para ver las respuestas</summary>

### Respuesta 1: ✅ B
**`npm install -g @anthropic-ai/claude-code`**

Claude Code es un paquete npm. El flag `-g` lo instala globalmente, lo que significa que puedes usar el comando `claude` desde cualquier directorio.

- `pip` es para Python (no aplica)
- `brew` instala apps de macOS pero Claude Code no está ahí
- `apt-get` es el gestor de Debian/Ubuntu (no aplica para Claude Code)

---

### Respuesta 2: ✅ B
**Como variable de entorno: `export ANTHROPIC_API_KEY="sk-ant-..."`**

Las variables de entorno son la forma estándar y segura de pasar credenciales a aplicaciones. Claude Code busca automáticamente `ANTHROPIC_API_KEY` en el entorno.

Nunca pongas la API Key en archivos de texto plano dentro de tu proyecto (pueden acabar en git por accidente).

---

### Respuesta 3: ✅ C
**Para dar instrucciones permanentes y contexto del proyecto a Claude.**

`CLAUDE.md` es leído automáticamente por Claude Code al iniciar. Contiene información sobre el proyecto: cómo funciona, qué comandos usar, convenciones de código, etc. Así no tienes que explicar lo mismo en cada sesión.

---

### Respuesta 4: ✅ C
**`/compact`**

`/compact` comprime el historial de la conversación para liberar espacio en el contexto. Esto permite continuar la sesión sin perder demasiado hilo.

- `/clear` limpia la pantalla visualmente pero no el contexto
- `/reset` no existe
- `/status` muestra información pero no libera contexto

---

### Respuesta 5: ✅ B
**`Crea un archivo hola.py que imprima "Hola mundo"`**

Claude Code acepta lenguaje natural. No necesitas aprender comandos especiales de sintaxis — simplemente describes lo que quieres en español (o inglés).

---

### Tu puntuación:
```
  5/5  Excelente! Avanza al Módulo 2.
  4/5  Muy bien. Revisa lo que fallaste.
  3/5  Repasa las secciones 1.2 a 1.7 antes de continuar.
  2/5  Vuelve a leer toda la lección.
  1/5  Reinicia desde el módulo 0.
```

</details>

---

**→ Cuando tengas 4 o más respuestas correctas: [Módulo 2 — Funcionalidades Core](../02-funcionalidades-core/leccion.md)**
