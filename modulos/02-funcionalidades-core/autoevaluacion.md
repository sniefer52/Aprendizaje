# 🎯 Autoevaluación — Módulo 2: Funcionalidades Core

> Responde las preguntas sin mirar la lección. Luego comprueba tus respuestas abajo.
> Tiempo estimado: 10 minutos

---

## Preguntas

### Pregunta 1
¿Cuál es la diferencia entre las herramientas `Write` y `Edit` que usa Claude Code?

- A) `Write` es para Python y `Edit` es para otros lenguajes
- B) `Write` crea o sobreescribe un archivo completo; `Edit` modifica partes específicas
- C) `Write` es más rápido que `Edit`
- D) No hay diferencia, son lo mismo

---

### Pregunta 2
¿Qué debes incluir siempre cuando le pides a Claude que debuggee un error?

- A) El nombre del archivo solamente
- B) Tu sistema operativo y versión de Python
- C) El error completo (traceback/stack trace) y descripción del contexto
- D) El historial completo de git

---

### Pregunta 3
Quieres que Claude explique qué hace la función `calcular_iva()` en el archivo `facturacion.py`. ¿Cuál es la mejor manera de pedírselo?

- A) `read facturacion.py function calcular_iva`
- B) `Explícame qué hace la función calcular_iva en facturacion.py`
- C) `claude --explain calcular_iva facturacion.py`
- D) `/explain facturacion.py:calcular_iva`

---

### Pregunta 4
¿Qué muestra Claude antes de aplicar cambios a un archivo de código?

- A) Un resumen en texto de los cambios
- B) El archivo completo nuevo para que lo revises
- C) Un diff (diferencias entre versión original y nueva)
- D) Aplica los cambios directamente sin preguntar

---

### Pregunta 5
¿Cuál de estas peticiones a Claude Code es la MÁS efectiva?

- A) "Arregla el bug"
- B) "El código tiene un error"
- C) "Hay un problema en procesar_pago() en payments.py línea 78. Cuando `amount` es 0, lanza una excepción no controlada. El traceback es: [...]"
- D) "Revisa todos los archivos y encuentra bugs"

---

## 🏆 Reto Práctico

Intenta este ejercicio en Claude Code:

```
1. Crea un archivo suma_lista.py que tenga una función
   que reciba una lista de números y devuelva su suma

2. Pide a Claude que añada manejo de errores para cuando
   la lista esté vacía o contenga valores no numéricos

3. Pide a Claude que genere tests unitarios para esa función

4. Ejecuta los tests
```

Si completaste los 4 pasos, tienes las funcionalidades core dominadas.

---

## Respuestas y Explicaciones

<details>
<summary>👉 Haz clic aquí para ver las respuestas</summary>

### Respuesta 1: ✅ B
**`Write` crea/sobreescribe un archivo completo; `Edit` modifica partes específicas.**

`Write` reemplaza todo el contenido de un archivo (o lo crea si no existe). `Edit` hace reemplazos quirúrgicos: cambia solo las partes que especificas sin tocar el resto. Para archivos existentes grandes, `Edit` es más seguro porque minimiza el riesgo de perder contenido.

---

### Respuesta 2: ✅ C
**El error completo y el contexto.**

El traceback completo le dice a Claude exactamente dónde ocurrió el error (archivo, línea, función). El contexto (qué estabas haciendo cuando ocurrió) ayuda a entender las condiciones del fallo. Sin esto, Claude tiene que adivinar.

---

### Respuesta 3: ✅ B
**`Explícame qué hace la función calcular_iva en facturacion.py`**

Claude Code acepta lenguaje natural. No hay sintaxis especial que aprender. Simplemente describes lo que necesitas como si le hablaras a una persona.

---

### Respuesta 4: ✅ C
**Un diff (diferencias entre versión original y nueva).**

Un diff muestra en formato estándar qué líneas se eliminan (marcadas con `-`) y qué líneas se añaden (marcadas con `+`). Esto te permite revisar exactamente qué cambiará antes de aprobarlo, sin sorpresas.

---

### Respuesta 5: ✅ C
**La descripción específica con función, archivo, línea y traceback.**

La especificidad es clave para obtener una solución precisa. Cuando indicas la función exacta, el archivo, la línea y el error completo, Claude puede diagnosticar el problema sin necesidad de buscar ciegamente por todo el código.

---

### Tu puntuación:
```
  5/5  Excelente! Tienes las funcionalidades core dominadas.
  4/5  Muy bien. Revisa lo que fallaste.
  3/5  Repasa las secciones 2.2 a 2.5 antes de continuar.
  2/5  Vuelve a leer toda la lección.
  1/5  Repasa desde el módulo 1.
```

</details>

---

**→ Cuando tengas 4 o más respuestas correctas: [Módulo 3 — Características Avanzadas](../03-caracteristicas-avanzadas/leccion.md)**
