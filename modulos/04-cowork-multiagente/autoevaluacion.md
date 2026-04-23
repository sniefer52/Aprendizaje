# 🎯 Autoevaluación — Módulo 4: COWORK Multi-Agente

> Responde las preguntas sin mirar la lección. Luego comprueba tus respuestas abajo.
> Tiempo estimado: 10 minutos

---

## Preguntas

### Pregunta 1
¿Qué es un "orquestador" en el contexto de COWORK?

- A) Un servidor que ejecuta los agentes en la nube
- B) El agente principal que divide y coordina el trabajo de los sub-agentes
- C) Un tipo especial de sub-agente para tareas de música
- D) El nombre del protocolo de comunicación entre agentes

---

### Pregunta 2
Tienes que analizar 3 módulos independientes de tu aplicación (auth, api, db). ¿Qué patrón es más eficiente?

- A) Secuencial: analizar auth, luego api, luego db
- B) Paralelo: lanzar los 3 análisis simultáneamente
- C) Híbrido: analizar auth primero, luego api y db juntos
- D) No importa, ambos tardan lo mismo

---

### Pregunta 3
Un sub-agente que lanzas con `run_in_background: True`, ¿tiene acceso a toda tu conversación anterior?

- A) Sí, hereda todo el contexto de la conversación del orquestador
- B) No, solo ve lo que le describes en su prompt
- C) Solo si usas el mismo modelo (Sonnet, Opus, etc.)
- D) Depende de si está en modo aislado o no

---

### Pregunta 4
¿Cuál de estas situaciones justifica usar COWORK en lugar de un solo agente?

- A) Corregir un typo en un comentario de código
- B) Refactorizar una función de 20 líneas
- C) Auditar 500 archivos de código para encontrar vulnerabilidades de seguridad
- D) Crear un archivo README sencillo

---

### Pregunta 5
¿Cómo se comunican los sub-agentes entre sí en COWORK?

- A) Directamente mediante un canal de mensajes compartido
- B) A través del orquestador, que actúa de intermediario
- C) Usando un archivo compartido en disco
- D) Los sub-agentes no pueden comunicarse; cada uno trabaja completamente aislado

---

## 🏆 Reto de Diseño

Diseña (en papel o mentalmente) cómo orquestarías este problema con COWORK:

**Tarea:** "Migra nuestro proyecto de JavaScript puro a TypeScript. El proyecto tiene 3 carpetas: `src/`, `tests/` y `utils/`."

Responde:
1. ¿Cuántos sub-agentes usarías?
2. ¿Qué haría cada uno?
3. ¿Serían secuenciales o paralelos? ¿Por qué?
4. ¿Qué tipo de agente (`Explore`, `Plan`, `general-purpose`) asignarías a cada uno?

<details>
<summary>Ver un posible diseño de solución</summary>

```
DISEÑO POSIBLE:

FASE 1 — Exploración (paralela):
  Sub-Agente A (Explore): Analiza src/ — qué archivos hay, qué patrones usa
  Sub-Agente B (Explore): Analiza tests/ — estructura de tests
  Sub-Agente C (Explore): Analiza utils/ — funciones utilitarias
  → Paralelo porque son independientes

FASE 2 — Planificación (secuencial, espera fase 1):
  Sub-Agente D (Plan): Con los resultados de A+B+C, diseña el
  plan de migración: orden, tipos a crear, configuración TS
  → Secuencial porque necesita los resultados de la fase 1

FASE 3 — Implementación (paralela):
  Sub-Agente E (general-purpose): Migra src/ según el plan
  Sub-Agente F (general-purpose): Migra tests/ según el plan
  Sub-Agente G (general-purpose): Migra utils/ según el plan
  → Paralelo porque cada carpeta es independiente

FASE 4 — Verificación (secuencial, espera fase 3):
  Orquestador ejecuta `tsc` y los tests para verificar
  que la migración fue exitosa
```

Este es un diseño válido, pero hay otras soluciones igualmente correctas.
</details>

---

## Respuestas y Explicaciones

<details>
<summary>👉 Haz clic aquí para ver las respuestas del quiz</summary>

### Respuesta 1: ✅ B
**El agente principal que divide y coordina el trabajo de los sub-agentes.**

El orquestador es quien recibe la tarea del usuario, la descompone en partes manejables, asigna cada parte a un sub-agente especializado, recoge los resultados y produce la respuesta final integrada.

---

### Respuesta 2: ✅ B
**Paralelo: lanzar los 3 análisis simultáneamente.**

Si los 3 módulos son independientes entre sí (el resultado de analizar `auth` no afecta al análisis de `api`), lo más eficiente es lanzarlos en paralelo. Tiempo total = el tiempo del más lento, no la suma de los tres.

---

### Respuesta 3: ✅ B
**No, solo ve lo que le describes en su prompt.**

Los sub-agentes son instancias nuevas e independientes. No heredan el contexto de la conversación del orquestador. Por eso, el prompt que escribes para el sub-agente debe ser auto-contenido e incluir toda la información necesaria.

---

### Respuesta 4: ✅ C
**Auditar 500 archivos de código.**

Con 500 archivos, un solo agente no puede mantener todo ese contexto en memoria simultáneamente. Con COWORK, puedes dividir los archivos entre múltiples sub-agentes que trabajan en paralelo, reduciendo el tiempo dramáticamente y evitando el límite de contexto.

Las otras opciones (typo, refactorizar 20 líneas, README) son tareas pequeñas perfectamente manejables por un solo agente.

---

### Respuesta 5: ✅ B
**A través del orquestador, que actúa de intermediario.**

Los sub-agentes no tienen canales directos entre sí. Cada sub-agente reporta sus resultados al orquestador, y si un sub-agente B necesita información del sub-agente A, el orquestador se la pasa al hacer el prompt de B.

---

### Tu puntuación:
```
  5/5  Excelente! Dominas COWORK. Listo para el proyecto final.
  4/5  Muy bien. Revisa lo que fallaste.
  3/5  Repasa las secciones 4.4 a 4.6 antes de continuar.
  2/5  Vuelve a leer la lección completa.
  1/5  Repasa desde el módulo 3.
```

</details>

---

**→ Cuando tengas 4 o más respuestas correctas: [Módulo 5 — Proyecto Final](../05-proyecto-final/leccion.md)**
