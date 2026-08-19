# Fly-in

### Los drones son interesantes.

**Resumen:** Diseña un sistema eficiente de enrutamiento de drones que navegue a través de varias zonas conectadas, minimizando los turnos de simulación y gestionando las restricciones de movimiento.

**Versión:** 1.6

---

## Índice

- I   Prólogo
- II  Instrucciones sobre el uso de IA
- III Instrucciones comunes
  - III.1 Reglas generales
  - III.2 Makefile
  - III.3 Directrices adicionales
- IV  Introducción
- V   Restricciones
- VI  Deja volar al dron
- VII Parte obligatoria
  - VII.1 Requisitos de pathfinding y algoritmo
  - VII.2 Reglas de ocupación de zonas
  - VII.3 Mecánica de movimiento y turnos
  - VII.4 Restricciones del parser
  - VII.5 Formato de salida de la simulación
  - VII.6 Sistema de puntuación
  - VII.7 Puntos de referencia de rendimiento
- VIII Requisitos del README
- IX  Parte bonus
- X   Entrega y peer-review

---

## Capítulo I — Prólogo

Los drones se han usado para pastorear ovejas en Nueva Zelanda, sustituyendo a los perros pastores por zumbones pastores aéreos. En Japón, algunos edificios de oficinas despliegan drones que reproducen música a todo volumen y encienden luces para, literalmente, echar a los empleados a casa. Un dron fue entrenado para pintar grafitis en paredes en pleno vuelo, una mezcla rebelde de tecnología y arte urbano. En Suecia, científicos usaron drones para olfatear excrementos de ballena flotando en el océano y así estudiar especies en peligro. Algunos drones experimentales tienen forma de pájaro o de insecto para espiar sin ser detectados, aleteando incluido. Incluso existe un dron que vuela haciendo pompas de jabón, sin hélices de por medio. En la investigación de volcanes, un dron voló directo hacia una nube de erupción, se derritió en pleno vuelo, pero logró enviar datos segundos antes de desintegrarse. Y en Corea del Sur, los espectáculos sincronizados de drones han sustituido a los fuegos artificiales: más seguros, silenciosos y, de algún modo, aún más mágicos.

La expresión viene de la idea de que la rueda es un invento brillante que lleva existiendo desde siempre y que funciona muy bien. Como no tiene nada de malo, intentar reinventarla de nuevo no serviría de mucho y podría ser una pérdida de tiempo, sobre todo cuando ese tiempo podría dedicarse a resolver problemas nuevos.

En programación, esto ocurre cuando alguien construye desde cero algo que ya existe, como escribir tu propio algoritmo de ordenación o tu propio framework cuando ya hay versiones sólidas de código abierto disponibles. Pero no es del todo malo: hacerlo tú mismo puede ser una gran forma de aprender cómo funcionan las cosas por dentro. La clave está en encontrar el equilibrio: no reconstruyas todo, pero tómate el tiempo de explorar cómo funcionan realmente las herramientas que usas. Así crecerás como desarrollador sin quedarte atascado reinventando siempre las mismas ruedas.

---

## Capítulo II — Instrucciones sobre el uso de IA

### Contexto

Durante tu proceso de aprendizaje, la IA puede ayudarte con muchas tareas distintas. Tómate el tiempo de explorar las diferentes capacidades de las herramientas de IA y cómo pueden apoyar tu trabajo. Sin embargo, acércate siempre a ellas con precaución y evalúa críticamente los resultados. Ya sea código, documentación, ideas o explicaciones técnicas, nunca puedes estar completamente seguro de que tu pregunta estaba bien formulada o de que el contenido generado es correcto. Tus compañeros son un recurso valioso para ayudarte a evitar errores y puntos ciegos.

### Mensaje principal

- Usa la IA para reducir tareas repetitivas o tediosas.
- Desarrolla habilidades de prompting, tanto de código como de otro tipo, que beneficiarán tu futura carrera.
- Aprende cómo funcionan los sistemas de IA para anticipar y evitar mejor riesgos, sesgos y problemas éticos comunes.
- Sigue desarrollando tus habilidades técnicas y humanas trabajando con tus compañeros.
- Usa únicamente contenido generado por IA que entiendas completamente y del que puedas responsabilizarte.

### Reglas para el alumno

- Debes tomarte el tiempo de explorar las herramientas de IA y entender cómo funcionan, para poder usarlas de forma ética y reducir posibles sesgos.
- Debes reflexionar sobre tu problema antes de escribir el prompt: esto te ayuda a redactar prompts más claros, detallados y relevantes, usando un vocabulario preciso.
- Debes desarrollar el hábito de comprobar, revisar, cuestionar y probar sistemáticamente todo lo que genere la IA.
- Debes buscar siempre la revisión de tus compañeros; no te bases únicamente en tu propia validación.

### Resultados esperados de la fase

- Desarrollar habilidades de prompting tanto generales como específicas del dominio.
- Aumentar tu productividad mediante un uso eficaz de las herramientas de IA.
- Seguir reforzando el pensamiento computacional, la resolución de problemas, la adaptabilidad y la colaboración.

### Comentarios y ejemplos

- Te encontrarás regularmente con situaciones (exámenes, evaluaciones, etc.) en las que deberás demostrar una comprensión real. Prepárate y sigue desarrollando tanto tus habilidades técnicas como interpersonales.
- Explicar tu razonamiento y debatir con tus compañeros a menudo revela lagunas en tu comprensión. Haz del aprendizaje entre pares una prioridad.
- Las herramientas de IA a menudo carecen de tu contexto específico y tienden a dar respuestas genéricas. Tus compañeros, que comparten tu entorno, pueden ofrecerte perspectivas más relevantes y precisas.
- Cuando la IA tiende a generar la respuesta más probable, tus compañeros pueden aportar puntos de vista alternativos y matices valiosos. Apóyate en ellos como punto de control de calidad.

**✓ Buena práctica:**
> Le pregunto a la IA: «¿Cómo pruebo una función de ordenación?». Me da algunas ideas. Las pruebo y reviso los resultados con un compañero. Afinamos el enfoque juntos.

**✗ Mala práctica:**
> Le pido a la IA que escriba una función completa y la copio-pego en mi proyecto. Durante la evaluación entre pares, no puedo explicar qué hace ni por qué. Pierdo credibilidad y suspendo el proyecto.

**✓ Buena práctica:**
> Uso la IA para ayudarme a diseñar un parser. Luego repaso la lógica con un compañero. Encontramos dos bugs y lo reescribimos juntos: mejor, más limpio y totalmente comprendido.

**✗ Mala práctica:**
> Dejo que Copilot genere el código de una parte clave de mi proyecto. Compila, pero no puedo explicar cómo gestiona las pipes. Durante la evaluación no consigo justificarlo y suspendo el proyecto.

---

## Capítulo III — Instrucciones comunes

### III.1 Reglas generales

- Tu proyecto debe estar escrito en **Python 3.10 o superior**.
- Tu proyecto debe cumplir el estándar de codificación **flake8**.
- Tus funciones deben gestionar las excepciones con elegancia para evitar caídas. Usa bloques `try-except` para manejar posibles errores. Prefiere los context managers para recursos como ficheros o conexiones, para asegurar una limpieza automática. Si tu programa se cae por excepciones no gestionadas durante la revisión, se considerará no funcional.
- Todos los recursos (por ejemplo, descriptores de fichero, conexiones de red) deben gestionarse correctamente para evitar fugas. Usa context managers siempre que sea posible para un manejo automático.
- Tu código debe incluir type hints para los parámetros de las funciones, los tipos de retorno y las variables cuando corresponda (usando el módulo `typing`). Usa `mypy` para el chequeo estático de tipos. Todas las funciones deben pasar `mypy` sin errores.
- Incluye docstrings en funciones y clases siguiendo PEP 257 (por ejemplo, estilo Google o NumPy) para documentar el propósito, los parámetros y los valores de retorno.

### III.2 Makefile

Incluye un `Makefile` en tu proyecto para automatizar las tareas habituales. Debe contener las siguientes reglas (el lint obligatorio implica los flags especificados; se recomienda encarecidamente probar `-strict` para una comprobación reforzada):

- **install**: instala las dependencias del proyecto usando `pip`, `uv`, `pipx`, o cualquier otro gestor de paquetes de tu elección.
- **run**: ejecuta el script principal del proyecto (por ejemplo, a través del intérprete de Python).
- **debug**: ejecuta el script principal en modo debug usando el depurador integrado de Python (por ejemplo, `pdb`).
- **clean**: elimina ficheros temporales o cachés (por ejemplo, `__pycache__`, `.mypy_cache`) para mantener el entorno del proyecto limpio.
- **lint**: ejecuta los comandos `flake8 .` y `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
- **lint-strict** (opcional): ejecuta los comandos `flake8 .` y `mypy . --strict`

### III.3 Directrices adicionales

- Crea programas de prueba para verificar la funcionalidad del proyecto (no se entregan ni se evalúan). Usa frameworks como `pytest` o `unittest` para pruebas unitarias, cubriendo los casos límite.
- Incluye un fichero `.gitignore` para excluir los artefactos de Python.
- Se recomienda usar entornos virtuales (por ejemplo, `venv` o `conda`) para aislar las dependencias durante el desarrollo.

*Si aplica algún requisito adicional específico del proyecto, se indicará justo debajo de esta sección.*

---

## Capítulo IV — Introducción

Los drones autónomos son el futuro del transporte. Ya se usan en muchos sectores, como la agricultura, la construcción y la logística. También se usan en operaciones militares, como la vigilancia y el reconocimiento.

Tu tarea consiste en diseñar un sistema que **enrute eficientemente una flota de drones** desde una **base central (start)** hasta una **ubicación objetivo (end)**, navegando por esta red dinámica bajo un conjunto de restricciones estrictas y objetivos de optimización.

Se te proporcionará un **grafo** que representa la red de zonas, y un **conjunto de restricciones** que deberás respetar.

El grafo se representa como una red de zonas conectadas, donde las conexiones definen las posibles rutas de movimiento entre zonas.

---

## Capítulo V — Restricciones

- Está prohibida cualquier librería que ayude con la lógica de grafos (como `networkx`, `graphlib`, etc.).
- El proyecto debe ser completamente typesafe. El uso de `flake8` y `mypy` es obligatorio.
- El proyecto debe ser completamente **orientado a objetos**.

Esto deberá demostrarse durante el peer-review.

---

## Capítulo VI — Deja volar al dron

Junto a este enunciado encontrarás varios ficheros que representan la red de zonas con el siguiente formato:

Ejemplo:

```
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

Interesante, ¿verdad? Para ser más precisos:

- La primera línea define el número de drones con `nb_drones: <número>`.
- La definición de cada zona se hace en una línea usando prefijos de tipo:
  - `start_hub: <name> <x> <y> [metadata]` marca la zona de inicio.
  - `end_hub: <name> <x> <y> [metadata]` marca la zona final.
  - `hub: <name> <x> <y> [metadata]` define una zona normal.
  - La sintaxis de las conexiones prohíbe los guiones en los nombres de zona (ver más abajo).
- Todos los metadatos son opcionales y van entre corchetes `[...]` con valores por defecto:
  - `zone=<type>` (por defecto: `normal`)
  - `color=<value>` (por defecto: ninguno)
  - `max_drones=<number>` (por defecto: 1) - número máximo de drones que pueden ocupar esa zona simultáneamente
  - Las etiquetas dentro de los corchetes pueden aparecer en cualquier orden.
- Tipos de zona:
  - `normal` – zona estándar con un coste de movimiento de 1 turno (por defecto)
  - `blocked` – zona inaccesible. Los drones no deben entrar ni pasar por esta zona. Cualquier ruta que la use es inválida.
  - `restricted` – zona sensible o peligrosa. Moverse a esta zona cuesta 2 turnos.
  - `priority` – zona preferente. Moverse a esta zona cuesta 1 turno, pero debe priorizarse en el pathfinding.
- Colores:
  - Los colores son opcionales y pueden usarse para la representación visual (salida en terminal o gráfica).
  - Los valores aceptados para `color` son cualquier cadena válida de una sola palabra (por ejemplo, `red`, `blue`, `gray`). No hay una lista fija de colores permitidos.
  - Cuando se especifican colores, la implementación debe ofrecer retroalimentación visual mediante salida en terminal en color o representación gráfica.
- Las conexiones se definen usando `connection: <name1>-<name2> [metadata]`:
  - Definen una conexión bidireccional (arista) entre dos zonas.
  - La sintaxis de las conexiones prohíbe los guiones en los nombres de zona.
  - Los metadatos opcionales se pueden especificar entre corchetes `[...]`:
    - `max_link_capacity=<number>` (por defecto: 1) - número máximo de drones que pueden atravesar esta conexión simultáneamente
- Los comentarios empiezan con `#` y se ignoran.

> ℹ️ Las coordenadas de las zonas siempre serán números enteros, y siempre habrá una única zona de inicio y una única zona final.

---

## Capítulo VII — Parte obligatoria

Como ya habrás imaginado, el objetivo principal es mover todos los drones desde la zona de inicio hasta la zona final en el menor número posible de turnos de simulación.

### VII.1 Requisitos de pathfinding y algoritmo

- Los drones pueden moverse simultáneamente. El algoritmo debe planificar las rutas para maximizar el rendimiento y evitar retrasos innecesarios.
- Tu implementación debe gestionar:
  - La distribución de drones entre múltiples rutas.
  - La espera estratégica cuando el movimiento no es posible.
  - La evitación de conflictos de ruta y de bloqueos mutuos (deadlocks).
- El algoritmo debe tener en cuenta:
  - La longitud de las rutas, incluyendo los costes de movimiento asociados a los tipos de zona (por ejemplo, `restricted` o `priority`).
  - La planificación de turnos, para evitar que los drones colisionen o se bloqueen entre sí.
  - La estructura del grafo, para determinar las rutas disjuntas o superpuestas disponibles.
  - Las restricciones de capacidad de zona (`max_drones`) y de conexión (`max_link_capacity`).
- Tu algoritmo debe ser adaptable: distintos mapas pueden requerir distintas estrategias de enrutamiento, según la topología y los tipos de zona.
- **Representación visual**: tu implementación debe ofrecer retroalimentación visual de la simulación, ya sea mediante:
  - Salida en terminal en color mostrando los movimientos de los drones y el estado de las zonas
  - Una interfaz gráfica que muestre la red y las posiciones de los drones
  - Ambas opciones para una mejor experiencia de usuario

> 💡
> - ¿Qué tan eficiente es tu algoritmo?
> - ¿Puede funcionar con un gran número de drones?
> - ¿Cuál es su complejidad (por ejemplo, O(n), O(log n), etc.)?
> - ¿Estás recalculando o cacheando las rutas?
> - ¿Cómo afecta al uso de memoria?
> - ¿Cómo mejora tu representación visual la comprensión de la simulación?

### VII.2 Reglas de ocupación de zonas

- Por defecto, una zona puede contener como máximo un dron en un turno de simulación dado.
- Las zonas con el metadato `max_drones=N` pueden contener hasta N drones simultáneamente.
- Las únicas excepciones especiales a las reglas de ocupación son:
  - La zona `start`: todos los drones empiezan aquí y pueden compartir el espacio inicialmente.
  - La zona `end`: pueden llegar varios drones aquí y se consideran entregados.
- Dos drones no pueden entrar en la misma zona en el mismo turno a menos que la capacidad de la zona lo permita.
- Un dron no puede moverse a una zona que superaría su capacidad máxima.
- La capacidad de conexión (`max_link_capacity`) definida en las conexiones limita cuántos drones pueden atravesar la misma conexión simultáneamente.
- Los drones pueden moverse simultáneamente, siempre que se respeten todas las restricciones de capacidad.

### VII.3 Mecánica de movimiento y turnos

La simulación avanza en turnos discretos. En cada turno, cada dron puede:

- Moverse a una zona adyacente conectada (si la capacidad lo permite).
- Moverse hacia una conexión en dirección a una zona `restricted` (que requiere 2 turnos para alcanzarse). En este caso, el dron DEBE llegar a su destino durante el siguiente turno. No puede esperar turnos extra en la conexión.
- Quedarse en el sitio (por ejemplo, para esperar, o si el movimiento está bloqueado).

La simulación debe evitar conflictos y garantizar una planificación de movimientos válida basada en la evaluación del estado turno a turno:

- Los drones que salen de una zona liberan capacidad de esa zona en ese mismo turno.
- Una zona debe tener capacidad disponible para que un dron se mueva a ella (después de que todos los drones que salen hayan liberado espacio).
- Para los movimientos de varios turnos (zonas `restricted`), el dron ocupa la conexión durante el tránsito y DEBE llegar al destino tras el número de turnos especificado. No puede esperar en la conexión a que haya un hueco libre en la zona de destino.

Cada movimiento entre zonas tiene un coste en turnos, según el `zone=type` del destino:

- `normal`: 1 turno (por defecto)
- `restricted`: 2 turnos
- `priority`: 1 turno (pero debe priorizarse en los algoritmos de pathfinding)
- `blocked`: inaccesible — no se puede entrar

### VII.4 Restricciones del parser

El fichero de entrada debe respetar la estructura y la sintaxis esperadas:

- La primera línea debe definir el número de drones con `nb_drones: <positive_integer>`.
- El programa debe poder manejar cualquier número de drones.
- Debe haber exactamente una zona `start_hub:` y una zona `end_hub:`.
- Cada zona debe tener un nombre único y coordenadas enteras válidas.
- Los nombres de zona pueden usar cualquier carácter válido excepto guiones y espacios.
- Las conexiones solo pueden enlazar zonas previamente definidas usando `connection: <zone1>-<zone2> [metadata]`.
- La misma conexión no debe aparecer más de una vez (por ejemplo, `a-b` y `b-a` se consideran duplicados).
- Cualquier bloque de metadatos (por ejemplo, `[zone=... color=...]` para zonas, `[max_link_capacity=...]` para conexiones) debe ser sintácticamente válido.
- Los tipos de zona deben ser uno de: `normal`, `blocked`, `restricted`, `priority`. Cualquier tipo inválido debe generar un error de parsing.
- Los valores de capacidad (`max_drones` para zonas, `max_link_capacity` para conexiones) deben ser enteros positivos.
- La capacidad `max_drones` se ignora en las zonas `start_hub` y `end_hub`: estas no tienen límite de capacidad (todos los drones pueden empezar en la zona de inicio, y cualquier número de drones puede llegar a la zona final). Si ese metadato está presente en esas dos zonas, se ignora y no supone un error de validación.
- Cualquier otro error de parsing debe detener el programa y devolver un mensaje de error claro que indique la línea y la causa.

> ℹ️ Se recomienda encarecidamente crear tus propios ficheros de mapa además de los proporcionados en el enunciado, para gestionar casos límite y manejo de errores.

### VII.5 Formato de salida de la simulación

- La simulación debe mostrar el movimiento paso a paso de los drones desde la zona de inicio hasta la zona final.
- Cada turno de simulación se representa en una línea.
- Una línea debe listar todos los movimientos de drones que ocurren en ese turno, separados por espacios. Cada movimiento debe seguir el formato: `D<ID>-<zone>`, o `D<ID>-<connection>` en el caso de drones que aún están en vuelo hacia zonas `restricted`.
  - `D<ID>` se refiere al identificador único del dron (por ejemplo, `D1`, `D2`).
  - `<zone>` es el nombre de la zona de destino.
  - `<connection>` es el nombre de la conexión hacia una zona `restricted`.
- Los drones que no se mueven en un turno dado se omiten de esa línea.
- Los drones que llegan a la zona final se consideran entregados y dejan de rastrearse.
- La simulación termina cuando todos los drones han llegado a la zona final.
- Ejemplo:

```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
```

### VII.6 Sistema de puntuación

- El rendimiento de una solución se evalúa según el **número total de turnos de simulación** necesarios para enrutar todos los drones desde la zona de inicio hasta la zona final.
- Cuantos menos turnos, mejor la puntuación.
- Una simulación válida debe:
  - Cumplir todas las reglas de movimiento y ocupación.
  - Gestionar correctamente los costes de movimiento asociados a los tipos de zona.
  - Respetar todas las restricciones de capacidad (límites de zona y de conexión).
  - Evitar todos los conflictos (por ejemplo, superar la capacidad de una zona o conexión).

Las métricas de evaluación secundarias (opcionales) pueden incluir:

- El número de drones movidos por turno (eficiencia de la asignación de rutas).
- El número medio de turnos por dron.
- El coste total de la ruta (suma de los costes de movimiento ponderados de todos los drones).
- La calidad y utilidad de la representación visual.

En caso de igualdad en el número de turnos, las soluciones pueden compararse según las métricas secundarias o la calidad del código.

> ℹ️ Estas métricas secundarias no son obligatorias de calcular automáticamente, pero se anima a los alumnos a mostrarlas en la salida de su simulación o en la documentación, para ayudar a sus compañeros a evaluar el rendimiento.

### VII.7 Puntos de referencia de rendimiento

Los siguientes objetivos de rendimiento definen el nivel de optimización esperado que tu implementación debe alcanzar.

- **Rendimiento esperado:**
  - Los mapas fáciles deben resolverse en menos de 10 turnos
  - Los mapas medios deben resolverse en 10–30 turnos
  - Los mapas difíciles deben resolverse en menos de 60 turnos
  - El mapa Challenger (opcional) debería aspirar a batir el récord de referencia de 45 turnos. Este nivel es totalmente opcional y no afecta a tu nota.

Para ayudarte a evaluar la eficiencia de tu algoritmo, aquí tienes los objetivos de rendimiento de referencia basados en los mapas de prueba proporcionados:

- **Mapas fáciles**:
  - Ruta lineal con 2 drones: objetivo ≤ 6 turnos
  - Bifurcación simple con 4 drones: objetivo ≤ 8 turnos
  - Capacidad básica con 4 drones: objetivo ≤ 6 turnos
- **Mapas medios**:
  - Trampa sin salida con 5 drones: objetivo ≤ 12 turnos
  - Bucle circular con 6 drones: objetivo ≤ 15 turnos
  - Puzle de prioridad con 5 drones: objetivo ≤ 12 turnos
- **Mapas difíciles**:
  - Pesadilla de laberinto con 8 drones: objetivo ≤ 30 turnos
  - Infierno de capacidad con 12 drones: objetivo ≤ 35 turnos
  - Desafío definitivo con 15 drones: objetivo ≤ 45 turnos
- **Mapa Challenger** (opcional — para implementaciones excepcionales):
  - The Impossible Dream con 25 drones: récord de referencia: 45 turnos
  - Este desafío casi irresoluble está pensado para la investigación algorítmica y la optimización
  - Resolver este mapa demuestra habilidades excepcionales de pathfinding y optimización
  - **Nota**: este nivel es totalmente opcional y no afecta a tu nota

> ℹ️ Estos puntos de referencia se proporcionan como objetivos de optimización para ayudarte a evaluar el rendimiento de tu algoritmo. Alcanzar estos objetivos demuestra una implementación bien optimizada y se valorará durante la evaluación entre pares.

> 💡
> - ¿Puede tu algoritmo alcanzar estos puntos de referencia?
> - ¿Cómo se compara tu solución con los objetivos de referencia?
> - ¿Qué optimizaciones implementaste para lograr un mejor rendimiento?
> - ¿Puedes resolver el mapa Challenger y batir el récord de 45 turnos?

---

## Capítulo VIII — Requisitos del README

Debe incluirse un fichero `README.md` en la raíz de tu repositorio Git. Su propósito es permitir que cualquiera que no esté familiarizado con el proyecto (compañeros, staff, reclutadores, etc.) entienda rápidamente de qué trata el proyecto, cómo ejecutarlo y dónde encontrar más información sobre el tema.

El `README.md` debe incluir al menos:

- La primera línea debe ir en cursiva y decir: *This project has been created as part of the 42 curriculum by \<login1\>[, \<login2\>[, \<login3\>[...]]].*
- Una sección de "**Description**" que presente claramente el proyecto, incluyendo su objetivo y una breve descripción general.
- Una sección de "**Instructions**" con cualquier información relevante sobre compilación, instalación y/o ejecución.
- Una sección de "**Resources**" que liste referencias clásicas relacionadas con el tema (documentación, artículos, tutoriales, etc.), así como una descripción de cómo se usó la IA, especificando para qué tareas y en qué partes del proyecto.
- ➡ **Pueden requerirse secciones adicionales según el proyecto** (por ejemplo, ejemplos de uso, lista de funcionalidades, decisiones técnicas, etc.).

*Cualquier adición obligatoria se indicará explícitamente más abajo.*

- También debe incluirse una descripción detallada de las decisiones de tu algoritmo y de tu estrategia de implementación.
- Documentación de las funcionalidades de representación visual y de cómo mejoran la experiencia de usuario.
- Un ejemplo de entrada y la salida esperada, demostrando el funcionamiento del programa.

> ⚠️ Tu README debe estar escrito en inglés.

---

## Capítulo IX — Parte bonus

Esta parte bonus solo se revisará si se cumplen todos los requisitos obligatorios.

Estas son funcionalidades que puedes implementar para mejorar tu proyecto:

- **Rendimiento excepcional:**
  - Cumples 'perfectamente' los objetivos de rendimiento de referencia para todos los mapas proporcionados.
  - 'Perfectamente' significa igualar o superar el número de turnos objetivo.
- **Mapa Challenger:**
  - El mapa The Impossible Dream está resuelto y bate el récord de referencia de 45 turnos.

---

## Capítulo X — Entrega y peer-review

Entrega tu proyecto en tu repositorio `Git` como de costumbre. Solo se evaluará el trabajo dentro de tu repositorio durante la evaluación entre pares. No dudes en verificar dos veces los nombres de tus ficheros para asegurarte de que son correctos.

> ⚠️ Coloca todos tus ficheros en la raíz de tu repositorio.

Una simulación completamente funcional escrita en Python, que incluya:

- Un parser para el formato del fichero de entrada.
- Un motor de simulación que respete las reglas de movimiento y de zona.
- Un algoritmo de pathfinding (o varios) capaz de minimizar el número total de turnos.
- Un sistema de representación visual (colores en terminal y/o interfaz gráfica).
- Una salida en terminal o log que siga el formato especificado.

> ℹ️ Ten en cuenta que podemos pedirte que expliques tu código o incluso que escribas algo de código. Asegúrate de estar preparado para ello.

> ℹ️ Los mapas de evaluación pueden ser distintos de los proporcionados en el enunciado.

Durante la evaluación, se te puede pedir ocasionalmente una breve **modificación del proyecto**. Esto podría implicar un pequeño cambio de comportamiento, unas pocas líneas de código a escribir o reescribir, o una funcionalidad fácil de añadir.

Aunque este paso puede **no ser aplicable a todos los proyectos**, debes estar preparado para él si se menciona en las directrices de evaluación.

Este paso tiene como objetivo verificar tu comprensión real de una parte concreta del proyecto. La modificación puede realizarse en cualquier entorno de desarrollo que elijas (por ejemplo, tu configuración habitual), y debería poder completarse en pocos minutos, salvo que se defina un plazo específico como parte de la evaluación.

Por ejemplo, se te puede pedir que hagas una pequeña actualización a una función o script, que modifiques una visualización, o que ajustes una estructura de datos para almacenar nueva información, etc.

Los detalles (alcance, objetivo, etc.) se especificarán en las **directrices de evaluación** y pueden variar de una evaluación a otra para el mismo proyecto.
