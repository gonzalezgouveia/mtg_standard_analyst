# Diario de aprendizaje — MTG Standard Metagame

**Versión:** 0.5 · **Inicio:** 21/11/2026 · **Actualizado:** 23/11/2026

Este documento registra brevemente qué hacemos, qué aprendemos y cómo colaboramos con la IA. Se actualizará al cerrar cada fase o hito importante. Los estados son orientativos y podrán cambiar.

## Hoja de ruta del proyecto

- [x] **1. Descubrimiento inicial:** identificar el problema, los usuarios y el objetivo del producto.
- [x] **2. Primeros borradores:** preparar la visión y el backlog iniciales.
- [x] **3. Revisar y validar la visión:** prioridad confirmada: ayudar al propietario a preparar torneos de Standard con datos recientes.
- [x] **4. Refinar y priorizar el backlog:** MVP local, importación manual CSV/JSON de varios torneos, filtros por fecha y tipo, recuentos y porcentajes por arquetipo y cobertura visible. Rediseño visual, automatización y acceso público quedan fuera.
- [x] **5. Diseño funcional y de datos:** reglas de filtros, denominadores, cobertura y evolución temporal acordadas. La validación de más fuentes sigue pendiente.
- [x] **6. Prueba técnica inicial:** cargar la muestra en Streamlit y comprobar que se visualiza. La viabilidad de fuentes remotas queda pendiente y fuera del MVP.
- [ ] **7. Diseño de arquitectura:** Streamlit y Python ya están elegidos; el MVP usará SQLite para persistencia local y queda pendiente completar esa capa relacional.
- [x] **8. Preparación del desarrollo:** repositorio, entorno local, documentación, pruebas iniciales y flujo de trabajo con IA preparados.
- [ ] **9. Desarrollo iterativo del MVP:** en curso; completar filtros, métricas y cobertura.
- [ ] **10. Pruebas y validación:** verificar resultados, calidad de datos y requisitos.
- [ ] **11. Entrega del MVP:** documentación, ejecución local y demostración.
- [ ] **12. Evolución posterior:** publicación web, automatización e histórico, según prioridades.

**Estado actual:** visión y alcance del MVP aprobados el 23/11/2026. Se comprobó manualmente que la muestra se carga y se visualiza. El foco pasa a completar y validar los criterios funcionales acordados; no se ha validado una integración remota.

> **Terminología:** *Discovery* o descubrimiento es la fase de comprensión del problema. **Licitación** es un proceso para solicitar y evaluar ofertas de proveedores; no es una fase necesaria en este proyecto individual. Después del descubrimiento suelen venir definición, diseño, implementación, validación y entrega, con iteraciones entre ellas.

## Registro de aprendizaje

### Entrada 001 — Descubrimiento inicial (21/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Pasamos de la idea de analizar el metajuego de Magic: The Gathering Standard a los primeros borradores de visión y backlog. Delimitamos un MVP local y dejamos para más adelante la publicación web y otras mejoras.

**Qué aprendimos:** La visión explica el propósito y el valor del producto; el backlog organiza requisitos; el MVP acota la primera versión útil. El descubrimiento precede a las decisiones técnicas detalladas.

**Decisiones:** Revisar y aprobar los borradores antes de diseñar la arquitectura. Validar la viabilidad de las fuentes de datos antes de depender de ellas.

**Papel de la IA:** Apoyar el análisis y la redacción; las decisiones finales y su validación corresponden al desarrollador.

**Siguiente paso:** Revisar la visión y registrar los cambios acordados. Completado en la entrada 002.

### Entrada 002 — Aprobación de visión y alcance del MVP (23/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Confirmamos que la prioridad es preparar torneos propios de Standard con datos recientes. Se revisó la muestra disponible en Streamlit y el propietario verificó que la importación y las gráficas iniciales funcionan.

**Qué aprendimos:** La prueba inicial confirma que se pueden cargar y mostrar los datos de muestra; no demuestra todavía que el MVP completo cumpla filtros, métricas y cobertura.

**Decisiones y motivos:** El MVP será local y de uso personal, con importación manual CSV/JSON de varios torneos, filtros temporales y por tipo, y recuentos y porcentajes por arquetipo con cobertura explícita. Se posponen el rediseño visual, la actualización remota y el acceso público.

**Papel de la IA:** Ayudó a resumir los borradores, señalar la diferencia entre una muestra de listas publicadas y el total de participantes, y traducir las decisiones del propietario en alcance y criterios de aceptación. La IA no ejecutó la comprobación visual: el propietario abrió la aplicación, importó el archivo y confirmó el resultado.

**Resultado y siguiente paso:** Visión y alcance aprobados. Completar y validar los criterios funcionales del MVP con datos de varios torneos.

**Reflexión sobre programación con IA:** Este hito muestra un uso de la IA como apoyo para leer documentación, comparar el prototipo con los requisitos, proponer una estructura de MVP y mantener un registro claro de decisiones. La persona desarrolladora conserva el criterio y valida el comportamiento real ejecutando la aplicación; la IA ayuda a convertir esa evidencia en tareas concretas y documentación revisable.

### Entrada 003 — Pruebas de Git, conexión con GitHub y permisos (23/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Intentamos preparar y subir cambios del proyecto y, después, realizamos pruebas controladas con `push_test.txt`. La primera sesión no pudo escribir en el índice de Git porque `.git` estaba en modo de solo lectura, aunque sí podía editar archivos del proyecto. Más adelante, al elegir un permiso más amplio, apareció una ventana de GitHub para autorizar la conexión con la aplicación. Una vez completada esa conexión, se pudo crear y subir un commit de prueba; también se subió un commit que eliminó ese primer archivo. Finalmente, con el modo **Ask for approval / Solicitar aprobación**, se aprobó la petición concreta para preparar el segundo archivo, crear el commit y hacer push. GitHub recibió el commit y la rama local quedó sincronizada.

**Qué aprendimos:** La autorización de GitHub y los permisos de Codex son dos cosas distintas. La conexión con GitHub permite autenticar las operaciones contra el repositorio remoto; el modo de permisos controla si Codex puede modificar los metadatos locales de Git y acceder a la red. Tener una de estas dos cosas no sustituye a la otra. El modo de aprobación puede funcionar sin mantener acceso total, siempre que la cuenta de GitHub ya esté conectada y se apruebe la solicitud de permisos cuando aparezca.

**Decisiones y motivos:** Para trabajar con este repositorio, mantener la cuenta de GitHub conectada en la aplicación y usar **Ask for approval / Solicitar aprobación** como modo habitual. Aprobar la petición específica cuando una operación de Git necesite más acceso. Reservar **Full access / Acceso completo** para situaciones puntuales, no como requisito permanente.

**Papel de la IA:** La IA preparó y ejecutó las operaciones de Git solicitadas, explicó la diferencia entre conexión remota y permisos del entorno, y comprobó el estado final de la rama. El propietario completó la autorización de GitHub y aprobó las operaciones solicitadas.

**Resultado y siguiente paso:** Se comprobó que el flujo de commit y push funciona después de conectar GitHub y conceder la aprobación requerida. En futuras operaciones, verificar primero que GitHub sigue conectado y aceptar la solicitud de aprobación de Codex si aparece. Esta prueba valida el flujo de Git, no los criterios funcionales del MVP.

### Entrada 004 — Reglas de análisis del metajuego (23/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Acordamos cómo calcular la presencia de arquetipos, tratar listas sin etiqueta, combinar torneos, definir ventanas temporales, normalizar categorías de evento, expresar cobertura y construir la evolución temporal.

**Qué aprendimos:** El número del título de un evento no equivale necesariamente al total de participantes. En la muestra disponible, el Standard Challenge 32 tuvo 52 participantes y 32 listas publicadas. Por eso el porcentaje de arquetipos debe usar las listas realmente importadas; la cobertura de participantes es una medida distinta y requiere conocer el total real.

**Decisiones y motivos:** «Sin etiquetar» será una categoría independiente incluida en el denominador. Al combinar eventos se suman recuentos y denominadores, no se promedian porcentajes. Los filtros de fecha usan la fecha del torneo, incluyen hoy y ofrecen 7, 15 o 30 días, o 2 o 3 meses naturales. Los tipos se normalizan a Standard Challenge o Standard Showcase Challenge, conservando el título de origen y sin inferir participantes de sus sufijos numéricos. La cobertura de participantes se muestra por separado cuando el total está disponible; si falta en algún evento seleccionado, la cobertura conjunta se declara incompleta. La evolución agrupa por fecha del torneo y muestra porcentaje, recuento y denominador; los eventos del mismo día se agregan.

**Papel de la IA:** Propuso definiciones y ejemplos para hacer explícitos los denominadores y evitar confundir listas publicadas con participantes totales. El propietario revisó y confirmó cada regla antes de incorporarla a la documentación.

**Resultado y siguiente paso:** Las reglas funcionales del análisis quedan documentadas. Continuar con la validación de datos de varios torneos y después implementar filtros, métricas y cobertura en el dashboard.

### Entrada 005 — Importación del total de participantes (23/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Añadimos al esquema de importación el campo opcional `participants_total`, actualizamos la muestra del Standard Challenge 32 con el total de 52 participantes reportado por la fuente y documentamos el formato CSV/JSON.

**Qué aprendimos:** El total de participantes es un dato del evento, aunque el archivo tenga una fila por mazo. En el formato actual se repite el mismo total en cada fila de ese torneo; si no se conoce, se deja vacío en todas. El importador comprueba que los valores sean enteros positivos y consistentes dentro del torneo.

**Decisiones y motivos:** No deducir el total de participantes a partir del sufijo numérico del nombre del evento. Mantener el dato opcional y separado del número de listas publicadas.

**Papel de la IA:** La IA preparó un ejemplo con datos ya documentados, implementó la aceptación y validación del nuevo campo y actualizó la guía de importación; el propietario confirmó el formato antes de implementarlo.

**Resultado y siguiente paso:** El importador ya conserva el total real de participantes cuando se proporciona. Integrar esta información en el indicador de cobertura del dashboard después de validar varios torneos.

### Entrada 006 — Aclaración sobre carga persistente de torneos (23/11/2026)
**Estado:** Decisión terminada; implementación pendiente.

**Qué hicimos:** Al revisar si el MVP debía conservar datos entre sesiones, el propietario aclaró el flujo deseado: al abrir la aplicación, esta debe leer automáticamente la carpeta local de datos y cargar los torneos disponibles. No quiere volver a importar los mismos torneos cada vez que inicia Streamlit.

**Qué aprendimos:** En la decisión inicial se consideró que los archivos locales bastaban como almacenamiento duradero. Esa decisión se revisó después: el propietario aprobó SQLite como almacenamiento relacional local, mientras que los archivos de `data/` siguen siendo la entrada manual. La etiqueta guardada en `archetype_labels.json` es un archivo auxiliar y no debe confundirse con un torneo.

**Decisiones y motivos:** La carga automática desde `data/` forma parte del alcance aprobado del MVP. En esta entrada se planteó inicialmente usar los archivos como fuente duradera; esa parte fue sustituida por la decisión de usar SQLite. La recolección de nuevos datos continúa siendo manual; quedan fuera la consulta remota y la actualización automática.

**Papel de la IA:** La IA detectó que la pregunta de persistencia seguía marcada como pendiente y explicó el comportamiento actual. El propietario corrigió el supuesto y concretó el flujo esperado; la IA registró esa decisión en la documentación sin implementar todavía el cambio.

**Resultado y siguiente paso:** Se implementó la primera lectura automática de CSV/JSON desde `data/`, en memoria. Posteriormente el propietario aprobó SQLite para la persistencia normalizada; adaptar esta carga al almacenamiento relacional queda pendiente.

### Entrada 007 — Carga automática desde la carpeta local (23/11/2026)
**Estado:** Implementado; validación funcional pendiente.

**Qué hicimos:** La aplicación ahora busca en `data/` archivos CSV y JSON al inicializar la sesión de Streamlit, los valida con el esquema habitual y carga los registros válidos. Informa por separado de archivos que no se puedan leer o validar. La detección por extensión deja fuera los archivos auxiliares de etiquetas. La importación desde el panel lateral sigue disponible y es temporal; para que un archivo aparezca en futuras sesiones hay que guardarlo en `data/`.

**Qué aprendimos:** La primera solución carga los archivos de datos al inicio y valida duplicados, pero los datos combinados permanecen en la sesión. La decisión posterior de usar SQLite permitirá mantenerlos normalizados y persistentes entre sesiones.

**Decisiones y motivos:** Se mantiene la incorporación manual de nuevos torneos y se excluyen la consulta remota y la actualización automática. Un archivo inválido no debe bloquear la carga de otros válidos.

**Papel de la IA:** La IA implementó el lector de carpeta, lo conectó al inicio de Streamlit y alineó la documentación con el comportamiento. La validación visual de la aplicación y las pruebas con varios archivos quedan pendientes.

**Resultado y siguiente paso:** La carga automática desde carpeta está implementada en memoria y el propietario comprobó que la muestra aparece sin subirla manualmente. Siguiente paso: integrar la carga con SQLite y validar varios torneos.

### Entrada 008 — Modelo relacional con SQLite (23/11/2026)
**Estado:** Decisión aprobada; documentación actualizada; implementación pendiente.

**Qué hicimos:** Al revisar por qué el total de participantes se repetía en cada fila del archivo, el propietario propuso separar los metadatos del torneo de sus listas y, más adelante, las cartas de cada lista. Aprobó adaptar el alcance del MVP para usar SQLite y pidió actualizar la documentación del proyecto.

**Qué aprendimos:** Repetir `participants_total` en CSV/JSON es cómodo para un formato de importación por filas, pero en el modelo relacional el total debe almacenarse una vez por torneo. Las listas publicadas pertenecen a un torneo; las cartas pertenecen a una lista. Los archivos CSV/JSON pueden seguir facilitando la incorporación manual sin ser el almacenamiento operativo del dashboard.

**Decisiones y motivos:** SQLite será el almacenamiento local persistente del MVP. El esquema separará torneos y listas, y preverá una relación de cartas por lista. El jugador se mantiene como atributo de la lista por ahora; no se crea entidad de jugador hasta que haya una necesidad concreta de seguimiento entre eventos. La tabla de cartas se poblará solo cuando existan listas completas y estructuradas; la muestra actual no las contiene. La carga de archivos desde `data/` debe incorporarlos a SQLite de manera idempotente y segura.

**Política de identidad y actualización acordada:** Cada lista es una instancia del torneo y jugador, con clave `(tournament_id, deck_id)`; el arquetipo no es la identidad de la lista. El mismo arquetipo puede corresponder a listas con cartas distintas, y un jugador tendrá registros independientes en torneos distintos. Archivos idénticos no duplican datos. Una versión completa modificada y válida reemplaza la anterior en una transacción; si falla, se conservan los datos previos. Si hay snapshots contradictorios simultáneos del mismo torneo, la aplicación informa el conflicto y no escoge uno. Etiquetas manuales de listas que desaparezcan se conservan como huérfanas para revisión.

**Papel de la IA:** La IA explicó las ventajas de separar las entidades y recomendó mantener CSV/JSON como entrada, normalizar los metadatos en SQLite y posponer la tabla independiente de jugadores. Tras la aprobación del propietario, actualizó visión, backlog, README, guía de datos, instrucciones y este diario. No implementó el almacenamiento SQLite en este cambio documental.

**Resultado y siguiente paso:** El modelo de datos y el cambio de alcance quedan documentados. Diseñar e implementar el esquema SQLite y adaptar la carga automática de `data/` antes de desarrollar filtros y métricas sobre la nueva capa de datos.

### Entrada 009 — Primera muestra de cartas de torneo (23/11/2026)
**Estado:** Muestra creada; importación a SQLite pendiente.

**Qué hicimos:** A partir de las páginas públicas individuales de MTGpile para el Standard Challenge 32 del 20 de noviembre, preparamos un CSV complementario con una fila por carta, mazo y zona. Incluye las 32 listas publicadas del top 32; cada una suma 60 cartas principales y 15 cartas de banquillo. El archivo contiene 988 filas de carta y conserva la URL fuente en cada una.

**Qué aprendimos:** El sitio muestra MTGO como fuente del torneo y publica cartas en sus páginas individuales. El acceso directo a la página oficial de MTGO requería JavaScript en la herramienta de lectura utilizada; la recopilación se hizo desde páginas públicas de MTGpile, sin conectar una cuenta ni un cliente de MTGO. El torneo tuvo 52 participantes, pero solo están disponibles estas 32 listas; la muestra de cartas no representa todas las participaciones.

**Decisiones y motivos:** Mantener el archivo de cartas separado del CSV de metadatos, con identificadores de torneo y lista y zona de mazo. Guardarlo bajo `data/examples/` para que el cargador de archivos de torneo no lo confunda con otro evento. Registrar procedencia y carácter provisional; no incorporarlo todavía al importador actual.

**Papel de la IA:** La IA consultó la página del evento, extrajo los datos estructurados de las 32 páginas de listas, cotejó jugador, posición y arquetipo con el CSV existente y comprobó los totales de cartas por lista. También documentó la cobertura y los límites de la fuente.

**Resultado y siguiente paso:** El CSV provisional está listo para revisar y sirve como muestra para la futura tabla `deck_cards`. Después, implementar un importador específico y validar el almacenamiento SQLite; no usarlo para afirmar cobertura total del evento.

### Entrada 010 — MTGpile como posible fuente futura (23/11/2026)
**Estado:** Decisión registrada; evaluación futura pendiente.

**Qué hicimos:** Tras consultar las páginas públicas de MTGpile para crear la muestra de cartas, el propietario indicó que el sitio podría ser útil para traer datos de otros Challenges en el futuro. Para las pruebas actuales, considera suficiente el torneo ya incorporado y sus listas publicadas.

**Qué aprendimos:** Una página que permite leer resultados y listas no queda automáticamente validada como fuente estable para un proceso de ingesta. Antes de automatizarla habrá que comprobar varias fechas y eventos, la cobertura, los cambios de formato y las condiciones de uso, y comparar los resultados con la referencia de MTGO.

**Decisiones y motivos:** MTGpile queda documentada como candidata futura, no como integración aprobada ni parte del MVP. No se ampliará ahora la recolección: la muestra existente basta para continuar las pruebas del esquema y la importación.

**Papel de la IA:** La IA explicó que las páginas públicas estáticas parecen técnicamente accesibles, pero que la viabilidad de una extracción automatizada requiere validación adicional. El propietario decidió conservarla como opción futura y mantener acotada la muestra actual.

**Resultado y siguiente paso:** Se añadió una tarea futura al backlog. Evaluar la fuente después, con una prueba controlada en varios torneos, antes de considerar una sincronización automatizada.

## Plantilla de próximas entradas

### Entrada NNN — [Fase o hito] ([fecha])
**Estado:** Pendiente / En curso / Terminado.

**Qué hicimos:** …

**Qué aprendimos:** …

**Decisiones y motivos:** …

**Papel de la IA:** …

**Resultado y siguiente paso:** …
