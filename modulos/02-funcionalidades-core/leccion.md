# Módulo 2 — Funcionalidades Core de Claude Code

> **Nivel:** Principiante-Intermedio | **Duración estimada:** 40 minutos
> **Objetivo:** Dominar las operaciones fundamentales: leer, escribir, editar código, generar proyectos y debuggear.

---

## 2.1 Las Herramientas de Claude Code

Claude Code no "escribe texto mágicamente". Usa **herramientas concretas** para interactuar con tu sistema. Entender esto es fundamental.

```
┌────────────────────────────────────────────────────────────┐
│                  HERRAMIENTAS DE CLAUDE CODE               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  LEER INFORMACIÓN:                                         │
│  ├── Read     → Lee el contenido de un archivo             │
│  ├── Bash     → Ejecuta comandos (ls, grep, cat, etc.)     │
│  └── WebSearch → Busca en internet                         │
│                                                            │
│  MODIFICAR ARCHIVOS:                                       │
│  ├── Write    → Crea o sobreescribe un archivo completo    │
│  └── Edit     → Cambia partes específicas de un archivo    │
│                                                            │
│  GESTIONAR TAREAS:                                         │
│  ├── TodoWrite → Crea y gestiona lista de tareas           │
│  └── Agent    → Lanza un sub-agente (COWORK)               │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

Claude elige automáticamente qué herramienta usar según tu petición. Tú solo hablas en lenguaje natural.

---

## 2.2 Leer y Analizar Archivos

### Leer un archivo

```
Tú:    "Lee el archivo app.py y explícame qué hace"

Claude: [Usa la herramienta Read en app.py]
        
        "app.py es una aplicación Flask que:
         1. Define una API REST con 3 endpoints:
            - GET /users → devuelve lista de usuarios
            - POST /users → crea un nuevo usuario  
            - DELETE /users/:id → borra un usuario
         2. Usa SQLite como base de datos
         3. Tiene validación básica de datos de entrada"
```

### Analizar múltiples archivos

```
Tú:    "Analiza la carpeta src/ y dime qué hace cada archivo"

Claude: [Lee todos los archivos de src/ uno a uno]
        
        "La carpeta src/ contiene:
         - main.py: punto de entrada de la aplicación
         - models.py: definición de modelos de datos
         - routes.py: definición de rutas de la API
         - utils.py: funciones auxiliares compartidas"
```

### Buscar patrones en el código

```
Tú:    "Busca todos los archivos Python que usen la función 'connect_db'"

Claude: [Ejecuta comandos grep para buscar el patrón]
        
        "Encontré 'connect_db' en 3 archivos:
         - src/main.py (línea 45)
         - src/models.py (línea 12)
         - tests/test_db.py (línea 8)"
```

---

## 2.3 Generar Código Nuevo

Una de las superpotencias de Claude Code es generar código funcional desde cero.

### Generar un archivo simple

```
Tú:    "Crea un archivo calculadora.py con funciones para
        sumar, restar, multiplicar y dividir"

Claude: [Crea calculadora.py con el siguiente contenido:]

        def sumar(a, b):
            return a + b

        def restar(a, b):
            return a - b

        def multiplicar(a, b):
            return a * b

        def dividir(a, b):
            if b == 0:
                raise ValueError("No se puede dividir por cero")
            return a / b
```

### Generar un proyecto completo

```
Tú:    "Crea la estructura de un proyecto Flask básico con:
        - Un endpoint GET /saludo que devuelva 'Hola mundo'
        - Tests unitarios
        - Un requirements.txt"

Claude: [Crea varios archivos y carpetas:]
        
        mi-proyecto/
        ├── app.py
        ├── requirements.txt
        └── tests/
            └── test_app.py
```

> 💡 **Tip:** Cuanto más específico seas, mejor será el código generado. Indica el lenguaje, el framework, el estilo de código y los casos especiales.

---

## 2.4 Editar Código Existente

Claude Code puede modificar partes específicas de tu código sin tocar el resto.

### Refactorizar una función

```
Tú:    "La función procesar_datos en utils.py es muy larga.
        Divídela en funciones más pequeñas y añade type hints"

Claude: [Lee utils.py, identifica la función, la divide y edita]
        
        "He dividido procesar_datos en 3 funciones:
         1. validar_datos() - valida el formato de entrada
         2. transformar_datos() - aplica las transformaciones
         3. guardar_resultados() - persiste el resultado
         
         También añadí type hints a todas las funciones."
```

### Añadir funcionalidad

```
Tú:    "Añade logging a la función autenticar_usuario en auth.py.
        Registra cuando alguien inicia sesión correctamente o falla"

Claude: [Lee auth.py, encuentra autenticar_usuario, añade logging]
```

### Ver los cambios antes de aplicarlos

Claude Code siempre te muestra un **diff** (las diferencias) antes de aplicar cambios importantes:

```
Tú:    "Renombra la variable 'usr' a 'usuario' en models.py"

Claude: Voy a hacer estos cambios:
        
        - usr = User.query.get(id)   ← línea original
        + usuario = User.query.get(id)  ← línea nueva
        
        ¿Quieres aplicar este cambio? [Sí / No]
```

---

## 2.5 Debugging Asistido

El debugging (encontrar y corregir errores) es donde Claude Code brilla especialmente.

### Flujo de debugging

```
ERROR APARECE
     │
     ▼
Copias el error a Claude
     │
     ▼
Claude lee los archivos relevantes
     │
     ▼
Claude identifica la causa raíz
     │
     ▼
Claude propone una solución
     │
     ▼
Tú apruebas y Claude aplica el fix
     │
     ▼
Ejecutas el código → Funciona
```

### Ejemplo real de debugging

```
Tú:    "Obtengo este error al ejecutar app.py:
        
        Traceback (most recent call last):
          File 'app.py', line 23, in get_user
            return db.execute(f'SELECT * FROM users WHERE id={user_id}')
        sqlite3.OperationalError: no such table: users"

Claude: [Lee app.py y busca la inicialización de la DB]
        
        "El problema es que la tabla 'users' no existe porque
        nunca se llama a init_db() al arrancar la aplicación.
        
        Además, veo un problema de seguridad: estás usando
        f-strings en SQL, lo que permite inyección SQL.
        
        Propongo estos 2 fixes:
        
        1. Añadir init_db() al inicio de app.py
        2. Cambiar a consultas parametrizadas:
           db.execute('SELECT * FROM users WHERE id=?', [user_id])
        
        ¿Aplico ambos cambios?"
```

> 💡 **Tip:** Siempre comparte el error completo (traceback o stack trace) con Claude. Cuanta más información tenga, mejor diagnóstico hará.

---

## 2.6 Ejecutar Comandos

Claude Code puede ejecutar comandos de terminal por ti:

```
Tú:    "Instala las dependencias del proyecto y ejecuta los tests"

Claude: [Ejecuta: pip install -r requirements.txt]
        Instalando dependencias...
        
        [Ejecuta: pytest]
        ================================= test session starts ==================================
        collected 12 items
        
        tests/test_app.py ........   [8 passed]
        tests/test_models.py ....    [4 passed]
        
        ================================= 12 passed in 2.34s ==================================
        
        "Todos los tests pasan. El proyecto está listo."
```

> ⚠️ **Importante:** Claude siempre te pide confirmación antes de ejecutar comandos que pueden tener efectos permanentes (borrar archivos, modificar configuración del sistema, etc.).

---

## 2.7 Comparativa: Claude Code vs Forma Tradicional

| Tarea | Forma Tradicional | Con Claude Code |
|-------|------------------|-----------------|
| Entender un archivo desconocido | Leer línea a línea (20 min) | "¿Qué hace este archivo?" (30 seg) |
| Crear tests unitarios | Escribir manualmente (1h) | "Crea tests para esta clase" (1 min) |
| Debuggear un error | Stack Overflow + prueba y error (30 min) | Describe el error (2 min) |
| Refactorizar código | Editar manualmente con cuidado (45 min) | "Refactoriza esto" (1 min) |
| Añadir validación | Escribir if/else manualmente (15 min) | "Añade validación a esta función" (30 seg) |
| Convertir a otro lenguaje | Reescribir desde cero (horas) | "Convierte esto de JS a Python" (2 min) |

---

## 2.8 Buenas Prácticas

```
✅ SE ESPECÍFICO:
   Malo:  "Arregla el código"
   Bueno: "La función calcular_descuento en pricing.py
           devuelve un valor negativo cuando price < 10.
           Arregla ese caso especial"

✅ DA CONTEXTO:
   Malo:  "Hay un bug"
   Bueno: "Hay un bug cuando el usuario hace login con
           Google OAuth. El error ocurre en auth.py línea 45.
           Aquí está el traceback: [pega el error]"

✅ CONFIRMA LOS CAMBIOS:
   Siempre revisa el diff antes de aprobar cambios
   en código crítico de producción

✅ USA CLAUDE.md:
   Documenta allí cómo ejecutar tests, el estilo
   de código preferido y el stack tecnológico

⚠️  NO DEPENDAS CIEGAMENTE:
   Claude puede cometer errores. Siempre revisa
   el código generado antes de llevarlo a producción
```

---

## 2.9 Resumen Visual

```
╔════════════════════════════════════════════════════════╗
║         FUNCIONALIDADES CORE — RESUMEN                 ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  LEER:                                                 ║
║  "Lee / analiza / explica / busca"                    ║
║   → Claude usa Read + Bash para inspeccionar          ║
║                                                        ║
║  CREAR:                                                ║
║  "Crea / genera / escribe / implementa"               ║
║   → Claude usa Write para crear nuevos archivos       ║
║                                                        ║
║  EDITAR:                                               ║
║  "Edita / refactoriza / mejora / añade / cambia"      ║
║   → Claude usa Edit para modificar partes             ║
║                                                        ║
║  DEBUGGEAR:                                            ║
║  "Hay un error / no funciona / ¿por qué falla?"       ║
║   → Claude lee, diagnostica y propone fix             ║
║                                                        ║
║  EJECUTAR:                                             ║
║  "Ejecuta / corre / instala / testea"                 ║
║   → Claude usa Bash para correr comandos              ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

---

## Siguiente Paso

**→ [Autoevaluación del Módulo 2](autoevaluacion.md)**

**→ [Módulo 3: Características Avanzadas](../03-caracteristicas-avanzadas/leccion.md)** — Hooks, MCP Servers, Settings e integración con IDE
