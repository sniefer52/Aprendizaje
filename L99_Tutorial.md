# L99 — Tutorial de Aprendizaje Autoguiado con Claude Code

> **¿Qué es este espacio?**
> Este repositorio es tu entorno personal de práctica. Aquí usas **Claude Code** como tutor interactivo para resolver los 99 problemas clásicos de programación (L-99), aprender a tu ritmo y construir criterio técnico real.

---

## Índice

1. [¿Qué son los L99?](#1-qué-son-los-l99)
2. [Cómo funciona este espacio](#2-cómo-funciona-este-espacio)
3. [Tu primer ciclo de aprendizaje](#3-tu-primer-ciclo-de-aprendizaje)
4. [Cómo hablar con Claude Code](#4-cómo-hablar-con-claude-code)
5. [Los 99 problemas (lista completa)](#5-los-99-problemas-lista-completa)
6. [Flujo de trabajo recomendado](#6-flujo-de-trabajo-recomendado)
7. [Señales de progreso real](#7-señales-de-progreso-real)
8. [Errores comunes y cómo evitarlos](#8-errores-comunes-y-cómo-evitarlos)

---

## 1. ¿Qué son los L99?

Los **L-99** son 99 problemas de programación progresivos, originalmente diseñados para aprender Lisp funcional pero aplicables a cualquier lenguaje. Cubren:

| Categoría | Problemas | Habilidades |
|-----------|-----------|-------------|
| Listas | 1–28 | Manipulación, recursión, transformación |
| Aritmética | 29–41 | Números primos, factorización, Euclides |
| Lógica | 42–48 | Tablas de verdad, circuitos lógicos |
| Binarios / Árboles | 49–69 | Árboles BST, Huffman, balanceo |
| Grafos | 70–80 | BFS, DFS, coloreo, spanning trees |
| Misceláneos | 81–99 | Puzzles de combinatoria y optimización |

**¿Por qué L99?** Porque cada problema es un peldaño: resolver el P03 hace que el P10 sea trivial. No son ejercicios aislados, son una escalera.

---

## 2. Cómo funciona este espacio

```
Aprendizaje/
├── README.md              ← Descripción general del repo
├── L99_Tutorial.md        ← Este archivo (léelo una sola vez, luego úsalo como referencia)
├── soluciones/            ← Tus soluciones van aquí (una por problema)
│   ├── p01.py             ← Ejemplo: solución al problema 1 en Python
│   └── ...
└── notas/                 ← Tus apuntes personales (opcional)
    └── conceptos.md
```

**Claude Code está siempre disponible** en la terminal del mismo directorio. Es tu par de programación: le puedes preguntar, pedirle que revise tu código, que te explique un error, o que te dé una pista sin revelar la solución.

### Regla de oro

> **Intenta primero. Pregunta después.**
> Si pides la respuesta directa, te privas del aprendizaje. Claude Code está configurado para darte pistas, no soluciones inmediatas — a menos que explícitamente lo pidas.

---

## 3. Tu primer ciclo de aprendizaje

Sigue este ciclo para cada problema:

```
┌─────────────────────────────────────────────┐
│                                             │
│   LEE el enunciado (2 min)                  │
│         │                                   │
│         ▼                                   │
│   ESCRIBE tu solución sin ayuda (10-30 min) │
│         │                                   │
│         ▼                                   │
│   ¿Funciona? ──NO──► Depura con Claude Code │
│         │                                   │
│        SÍ                                   │
│         ▼                                   │
│   PIDE REVISIÓN a Claude Code               │
│         │                                   │
│         ▼                                   │
│   REFACTORIZA si hay mejoras                │
│         │                                   │
│         ▼                                   │
│   HAZ COMMIT y pasa al siguiente            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 4. Cómo hablar con Claude Code

Abre la terminal en este directorio y escribe `claude`. Algunos ejemplos de prompts efectivos:

### Para obtener pistas (sin spoilers)
```
Estoy en el problema P14 (duplicar elementos de una lista).
Mi solución falla con listas vacías. Sin decirme la respuesta,
¿qué concepto debería revisar?
```

### Para revisar tu código
```
Aquí está mi solución al P07 (aplanar lista anidada).
¿Es idiomática? ¿Hay algo ineficiente?

[pega tu código aquí]
```

### Para entender un error
```
Tengo este error de Python:
RecursionError: maximum recursion depth exceeded
¿Qué lo causa en general y cómo lo identifico en mi código?
```

### Para pedir explicación de un concepto
```
No entiendo qué es un árbol binario de búsqueda.
Explícamelo con un ejemplo concreto antes de que ataque el P57.
```

### Para pedir la solución (cuando ya agotaste opciones)
```
Llevé 45 minutos en el P23 y sigo atascado.
Muéstrame la solución y luego explícame línea por línea.
```

---

## 5. Los 99 problemas (lista completa)

### Listas (P01–P28)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P01 | Encontrar el último elemento de una lista | ★☆☆ |
| P02 | Encontrar el penúltimo elemento | ★☆☆ |
| P03 | Encontrar el k-ésimo elemento (1-indexado) | ★☆☆ |
| P04 | Contar los elementos de una lista | ★☆☆ |
| P05 | Invertir una lista | ★☆☆ |
| P06 | Determinar si una lista es palíndromo | ★☆☆ |
| P07 | Aplanar una lista anidada | ★★☆ |
| P08 | Eliminar duplicados consecutivos | ★★☆ |
| P09 | Empaquetar duplicados consecutivos en sublistas | ★★☆ |
| P10 | Run-length encoding | ★★☆ |
| P11 | Run-length encoding modificado | ★★☆ |
| P12 | Decodificar run-length encoding | ★★☆ |
| P13 | Run-length encoding directo (sin P09) | ★★☆ |
| P14 | Duplicar los elementos de una lista | ★☆☆ |
| P15 | Replicar elementos N veces | ★★☆ |
| P16 | Eliminar cada N-ésimo elemento | ★★☆ |
| P17 | Partir una lista en dos partes | ★★☆ |
| P18 | Extraer una sublista | ★★☆ |
| P19 | Rotar lista N posiciones a la izquierda | ★★☆ |
| P20 | Eliminar el k-ésimo elemento | ★★☆ |
| P21 | Insertar elemento en posición dada | ★☆☆ |
| P22 | Crear lista de enteros en un rango | ★☆☆ |
| P23 | Extraer N elementos aleatorios | ★★☆ |
| P24 | Lotería: N números distintos de rango 1..M | ★★☆ |
| P25 | Permutación aleatoria de lista | ★★☆ |
| P26 | Generar combinaciones de K elementos | ★★★ |
| P27 | Agrupar elementos en subconjuntos disjuntos | ★★★ |
| P28 | Ordenar lista de listas por longitud | ★★☆ |

### Aritmética (P29–P41)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P29 | Determinar si un número es primo | ★★☆ |
| P30 | Calcular MCD con algoritmo de Euclides | ★★☆ |
| P31 | Determinar si dos números son coprimos | ★☆☆ |
| P32 | Calcular la función Totient de Euler | ★★☆ |
| P33 | Lista de factores primos | ★★☆ |
| P34 | Lista de factores primos con multiplicidad | ★★☆ |
| P35 | Totient mejorada con factores | ★★★ |
| P36 | Comparar los dos métodos de Totient | ★★☆ |
| P37 | Lista de números primos en un rango | ★★☆ |
| P38 | Conjetura de Goldbach | ★★☆ |
| P39 | Lista de parejas de Goldbach en un rango | ★★★ |
| P40 | Suma de Goldbach para un número par | ★★★ |
| P41 | Tabla de Goldbach con límite de primo | ★★★ |

### Lógica y Códigos (P42–P48)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P42 | Tabla de verdad para expresiones lógicas | ★★★ |
| P43 | Código Gray | ★★☆ |
| P44 | Codificación de Huffman | ★★★ |
| P45–P48 | Variantes de codificación y compresión | ★★★ |

### Árboles Binarios (P49–P69)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P49 | Conteo de árboles completamente balanceados | ★★★ |
| P50 | Generar todos los CBT | ★★★ |
| P51 | Árbol simétrico | ★★☆ |
| P52 | Árbol binario de búsqueda (BST) | ★★★ |
| P53 | Generar y probar: árboles simétricos y completos | ★★★ |
| P54 | Altura de un árbol | ★★☆ |
| P55 | Árboles perfectamente balanceados en altura | ★★★ |
| P56 | Contar hojas | ★★☆ |
| P57 | Recolectar hojas en una lista | ★★☆ |
| P58 | Recolectar nodos internos | ★★☆ |
| P59 | Nodos a nivel N | ★★☆ |
| P60 | Construir árbol completo con N nodos | ★★★ |
| P61–P69 | Recorridos, serialización y layout de árboles | ★★★ |

### Árboles Multicamino (P70–P75)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P70 | Contar nodos de árbol multicamino | ★★☆ |
| P71 | Determinación de la ruta interna | ★★★ |
| P72 | Recorrido postorder | ★★☆ |
| P73 | Representación Lisp-like | ★★★ |

### Grafos (P74–P86)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P80 | Conversión entre representaciones de grafo | ★★★ |
| P81 | Caminos entre dos nodos | ★★★ |
| P82 | Ciclos desde un nodo | ★★★ |
| P83 | Árbol de expansión mínima | ★★★ |
| P84 | Prim's algorithm | ★★★ |
| P85 | Isomorfismo de grafos | ★★★ |
| P86 | Coloreo de grafos | ★★★ |

### Misceláneos (P87–P99)

| # | Enunciado | Dificultad |
|---|-----------|------------|
| P87 | Ocho reinas | ★★★ |
| P88 | Problema del caballo | ★★★ |
| P89 | Cuadrado de Von Koch | ★★★ |
| P90–P99 | Puzzles combinatorios avanzados | ★★★ |

---

## 6. Flujo de trabajo recomendado

### Estructura de archivos

Crea una carpeta `soluciones/` y nombra cada archivo con el número del problema:

```bash
mkdir -p soluciones notas
```

Ejemplo de archivo de solución bien estructurado (`soluciones/p01.py`):

```python
# P01 - Último elemento de una lista
# Enunciado: Encontrar el último elemento de una lista.
# Ejemplo: last([1, 2, 3, 4]) → 4

def last(lst):
    if not lst:
        raise ValueError("lista vacía")
    if len(lst) == 1:
        return lst[0]
    return last(lst[1:])


# Tests
assert last([1, 2, 3, 4]) == 4
assert last(['a']) == 'a'
print("P01 ✓")
```

### Comandos git que usarás

```bash
# Ver qué archivos cambiaste
git status

# Guardar tu progreso
git add soluciones/p01.py
git commit -m "P01: solución recursiva al último elemento"

# Ver tu historial de progreso
git log --oneline
```

### Cómo ejecutar tu solución

```bash
python soluciones/p01.py
```

---

## 7. Señales de progreso real

Sabes que aprendiste algo cuando puedes:

- [ ] Explicar tu solución en voz alta sin mirar el código
- [ ] Resolver una variante del problema sin buscar ayuda
- [ ] Identificar si tu solución es O(n) o O(n²) (y por qué importa)
- [ ] Reescribir la solución de otra manera (iterativa si era recursiva, y viceversa)
- [ ] Encontrar el caso borde que rompe una solución naive

**Hito de bloque:**
- Completar P01–P10: dominas manipulación de listas
- Completar P01–P28: piensas de forma funcional
- Completar P01–P41: te sientes cómodo con recursión y matemáticas
- Completar todos: tienes base sólida para entrevistas técnicas y algoritmos

---

## 8. Errores comunes y cómo evitarlos

### ❌ Leer la solución antes de intentar

**Consecuencia:** Ilusión de comprensión. Ves la solución y dices "tiene sentido" pero no puedes reproducirla.

**Alternativa:** Dedica al menos 15 minutos de intento real antes de pedir pistas.

---

### ❌ Resolver sin tests

**Consecuencia:** Tu función "funciona" en el ejemplo trivial pero falla en bordes.

**Alternativa:** Escribe siempre al menos 3 casos: el ejemplo del enunciado, una lista vacía, y un caso de un solo elemento.

---

### ❌ Copiar y pegar código de Claude sin leerlo

**Consecuencia:** No aprendes nada. El código pasa los tests pero tú no podrías defenderlo.

**Alternativa:** Si pides una solución, léela línea por línea y pide que te explique lo que no entiendas. Luego ciérrala y reescríbela tú de memoria.

---

### ❌ Saltar problemas porque "parecen fáciles"

**Consecuencia:** Los problemas fáciles son los que construyen los patrones mentales que los difíciles requieren.

**Alternativa:** Hazlos todos. Los primeros 10 no toman más de 2 horas en total.

---

### ❌ No hacer commit al terminar cada problema

**Consecuencia:** Pierdes el rastro de tu progreso y no puedes volver atrás.

**Alternativa:** Un commit por problema. El mensaje del commit es tuyo: "P07: primera vez que uso recursión con acumulador".

---

## Empecemos

Tu primer problema está abajo. No lo busques en internet. No le pidas la solución a Claude todavía. **Intenta.**

---

### P01 — Último elemento de una lista

**Enunciado:**
Escribe una función `last(lst)` que devuelva el último elemento de una lista.

```
last([1, 1, 2, 3, 5, 8]) → 8
last(['a', 'b', 'c']) → 'c'
```

**Restricciones:**
- No uses `lst[-1]` (eso sería trampa para este ejercicio)
- Implementa una solución recursiva

**Pistas disponibles** (pídelas a Claude Code cuando las necesites):
1. Pista 1: ¿Cuál es el caso base?
2. Pista 2: ¿Qué pasa si la lista tiene un solo elemento?
3. Pista 3: ¿Qué pasa con el resto de la lista?

---

Cuando termines P01, vuelve a la tabla del paso 5 y pasa a P02.

**¡Buena suerte!** El progreso en L99 es acumulativo: cada problema que resuelves hace los siguientes más fáciles. La dificultad no es la programación — es la disciplina de intentar antes de pedir ayuda.

---

*Tutorial creado para el repositorio Aprendizaje — Aprendizaje autoguiado con Claude Code*
