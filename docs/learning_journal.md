# Diario de aprendizaje — MTG Standard Metagame

**Versión:** 0.7 · **Inicio:** 21/11/2026 · **Actualizado:** 25/11/2026

Este documento registra brevemente qué hacemos, qué aprendemos y cómo colaboramos con la IA. Se actualizará al cerrar cada fase o hito importante. Los estados son orientativos y podrán cambiar.

## Hoja de ruta del proyecto

- [x] **1. Descubrimiento inicial:** identificar el problema, los usuarios y el objetivo del producto.
- [x] **2. Primeros borradores:** preparar la visión y el backlog iniciales.
- [x] **3. Revisar y validar la visión:** prioridad confirmada: ayudar al propietario a preparar torneos de Standard con datos recientes.
- [x] **4. Refinar y priorizar el backlog:** MVP local, importación manual CSV/JSON de varios torneos, filtros por fecha y tipo, recuentos y porcentajes por arquetipo y cobertura visible. Rediseño visual, automatización y acceso público quedan fuera.
- [x] **5. Diseño funcional y de datos:** reglas de filtros, denominadores, cobertura y evolución temporal acordadas. La validación de más fuentes sigue pendiente.
- [x] **6. Prueba técnica inicial:** cargar la muestra en Streamlit y comprobar que se visualiza. La viabilidad de fuentes remotas queda pendiente y fuera del MVP.
- [x] **7. Diseño de arquitectura:** Streamlit y Python para la aplicación y SQLite para la persistencia local.
- [x] **8. Preparación del desarrollo:** repositorio, entorno local, documentación, pruebas iniciales y flujo de trabajo con IA preparados.
- [x] **9. Desarrollo iterativo del MVP:** filtros, presencia, cobertura, evolución e indicador de importación implementados.
- [x] **10. Pruebas y validación:** revisión de los criterios P0 completada y documentada en la revisión de aceptación.
- [x] **11. Entrega del MVP:** paquete local verificado, guía de arranque y traslado disponible, y cierre confirmado por el propietario.
- [ ] **12. Evolución posterior:** publicación web, automatización e histórico, según prioridades.

**Estado actual:** el MVP local está cerrado. Se verificó la entrega recién extraída y el propietario confirmó el cierre. El piloto local contiene seis torneos de MTGO y 190 listas publicadas.

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

**Decisiones y motivos:** SQLite será el almacenamiento local persistente del MVP. El esquema separará torneos y listas, con una relación de cartas por lista. El jugador se mantiene como atributo de la lista por ahora; no se crea entidad de jugador hasta que haya una necesidad concreta de seguimiento entre eventos. La carga de archivos desde `data/` debe incorporarlos a SQLite de manera idempotente y segura.

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

### Entrada 011 — Persistencia SQLite del MVP (23/11/2026)
**Estado:** Implementado; validación inicial completada.

**Qué hicimos:** Creamos el almacenamiento local SQLite con las tablas `tournaments`, `decks`, `deck_cards` y registro de fuentes. Conectamos la sincronización al arranque de Streamlit: los CSV/JSON de metadatos de la raíz de `data/` se importan como snapshots de torneo y los archivos `_cards.csv` de `data/examples/` o `data/cards/` se importan por separado. El importador manual ahora guarda su archivo validado en `data/` para que permanezca disponible.

**Qué aprendimos:** Separar los metadatos de torneo, listas y cartas evita repetir el total de participantes y conserva cada lista como una instancia de torneo y `deck_id`. Los snapshots idénticos quedan sin cambios; los modificados se escriben en transacciones; archivos contradictorios se reportan; un fallo de validación conserva lo previamente guardado.

**Decisiones y motivos:** El archivo SQLite vive en `data/` y Git lo ignora junto con los CSV/JSON. Las etiquetas manuales siguen en `archetype_labels.json`, fuera de las tablas de torneo, y no se eliminan cuando una lista falta en una nueva versión. La muestra de cartas es un archivo complementario local y no se confunde con un CSV de torneo.

**Papel de la IA:** La IA implementó esquema, validación/importación, persistencia y conexión de Streamlit; añadió verificaciones automatizadas para idempotencia, actualización, conflictos y preservación ante errores. El propietario había validado previamente la carga visual y aprobó las reglas de importación.

**Resultado y siguiente paso:** Las 32 listas y 988 filas de cartas se cargaron en la base local; al sincronizar por segunda vez no hubo cambios ni duplicados. Las 15 pruebas automatizadas pasaron y la prueba de Streamlit terminó sin excepciones. Seguir con los filtros por fecha y tipo, métricas y cobertura.

### Entrada 012 — Evolución del metajuego por fecha (25/11/2026)
**Estado:** Implementado; validación funcional con varios eventos pendiente.

**Qué hicimos:** Añadimos al dashboard una evolución temporal de la presencia de arquetipos para los torneos que pasan los filtros activos. La vista agrupa las listas por fecha y arquetipo, muestra porcentajes y permite consultar recuentos y denominadores en el gráfico y la tabla.

**Qué aprendimos:** La base de comparación temporal es el total de listas publicadas de cada fecha, sumando los eventos del mismo día. «Sin etiquetar» permanece como categoría independiente y forma parte del denominador.

**Decisiones y motivos:** Se conserva la fecha del torneo como eje temporal y se agregan eventos coincidentes antes de calcular porcentajes. No se promedian porcentajes de eventos. La evolución respeta los filtros de periodo y tipo ya existentes.

**Papel de la IA:** Implementó la agrupación y visualización en Streamlit, y actualizó el estado del dashboard en el backlog.

**Resultado y siguiente paso:** El código compila y la revisión de formato no reporta errores. Falta comprobar la agregación con varios eventos, especialmente eventos distintos en una misma fecha, cuando haya datos disponibles. Después, completar la fecha de última actualización y revisar el MVP funcional.

### Entrada 013 — Fecha de última importación y documentación (25/11/2026)
**Estado:** Implementado; revisión visual pendiente.

**Qué hicimos:** Añadimos a la consulta del dashboard el momento de importación aceptada de cada torneo y mostramos la fecha más reciente entre los torneos que pasan los filtros. Actualizamos el README y el resumen del backlog para reflejar los filtros, métricas, cobertura y evolución ya implementados.

**Qué aprendimos:** La columna `imported_at` registra la última importación aceptada del snapshot de un torneo. Una sincronización idéntica sin cambios no actualiza ese momento, por lo que el indicador describe cuándo se incorporó por última vez una versión aceptada, no cuándo se abrió Streamlit.

**Decisiones y motivos:** El indicador sigue los filtros activos para que su alcance coincida con los datos mostrados. Se presenta en hora local. Se mantiene la validación con varios torneos como trabajo pendiente.

**Papel de la IA:** Amplió la consulta SQLite, conectó el valor con la presentación del dashboard y corrigió la documentación de estado.

**Resultado y siguiente paso:** Código compilado y revisión de formato correcta; no se ejecutaron pruebas automatizadas. Revisar visualmente la fecha en Streamlit y, cuando haya datos verificables de varios torneos, validar filtros y agregaciones.

### Entrada 014 — Piloto con seis torneos de MTGO (25/11/2026)

**Estado:** Carga confirmada en SQLite. Revisión inicial en Streamlit realizada.

**Qué hicimos:** Conservamos el Challenge original del día 20 e incorporamos otros cinco eventos celebrados del 20 al 24 de noviembre. El piloto suma cinco Standard Challenge y un Showcase, con 190 listas publicadas, 158 de ellas nuevas. Guardamos un CSV por evento y anotamos su procedencia en el archivo local `data/standard_pilot_2026-11-20_to_24_SOURCE.md`.

**Qué aprendimos:** Las dos fichas del día 20 corresponden a eventos distintos y suman 64 listas. El Showcase del 21 tiene 32 listas publicadas de 183 participantes. La fuente del día 24 deja siete arquetipos en blanco, que se conservaron así. Los seis eventos informan el total de participantes, por lo que la cobertura incompleta requiere otro caso de validación.

**Decisiones y motivos:** Mantuvimos la recopilación manual y usamos MTGO como referencia. Transcribimos cuatro eventos desde MTGpile y el del día 24 desde Magic: The Metagame. Los cinco eventos añadidos aportan metadatos de listas. El evento original conserva sus cartas estructuradas.

**Papel de la IA:** Contrastó las fichas, preparó los CSV, ejecutó el importador local y consultó SQLite para confirmar los recuentos. El importador informó cero errores y dejó el torneo original sin cambios.

**Resultado y siguiente paso:** El propietario confirmó en Streamlit los recuentos por categoría, el denominador de 64 del día 20, el 21,9 % de «Sin etiquetar» del día 24 y el 41,6 % de cobertura conjunta. Las ventanas de 7 y 30 días incluyeron los mismos eventos. Queda probar el cambio de resultados entre ventanas, el estado vacío y la cobertura incompleta con datos de prueba separados.

### Entrada 015 — Base mínima para validar el dashboard (25/11/2026)

**Estado:** Comprobaciones del dashboard completadas con la base de prueba.

**Qué hicimos:** Preparamos una copia local del dashboard con dos eventos ficticios, a seis y siete días de la fecha de preparación. Uno declara cuatro participantes y el otro deja ese dato vacío. La herramienta genera una base SQLite separada usando el importador habitual.

**Resultado y siguiente paso:** El propietario confirmó la cobertura incompleta, el aviso de filtros sin resultados y el cambio de 2 listas a 1 con una cobertura del 25 % al pasar de 30 a 7 días. Una ejecución aislada de Streamlit creó una base vacía y mostró el aviso inicial sin excepciones. La [guía de validación](dashboard_validation.md) explica cómo repetir estos casos. Sigue la revisión de los criterios de importación y persistencia del MVP.

### Entrada 016 — Comprobaciones de importación y persistencia (25/11/2026)

**Estado:** Cuatro comprobaciones superadas en una base aislada. Las 15 pruebas existentes pasaron.

**Qué hicimos:** Reimportamos el mismo contenido desde un segundo archivo y comprobamos que se conservaban la lista y la fecha de importación. Abrimos otro proceso con el archivo original retirado y recuperamos la lista desde SQLite. Después presentamos un JSON inválido y dos archivos válidos pero contradictorios. En ambos casos el importador informó del problema y conservó la versión y la fecha ya guardadas.

**Resultado y siguiente paso:** El propietario completó la comprobación desde el panel lateral en la copia aislada. Subió un Showcase después del Challenge que ya había importado, cerró Streamlit con Ctrl+C y confirmó que ambos seguían visibles al volver a abrirlo. Se verificaron los dos CSV guardados y sus 62 listas en SQLite. El piloto real quedó intacto. El siguiente paso es cotejar la evidencia con los criterios de aceptación del MVP.

### Entrada 017 — Revisión de aceptación del MVP (25/11/2026)

**Estado:** Revisión realizada. Cierre pendiente.

**Qué hicimos:** Cotejamos las comprobaciones del propietario en Streamlit, las consultas a SQLite, las pruebas existentes y el código con los criterios P0 del backlog.

**Qué aprendimos:** Un JSON inválido con varios torneos puede actualizar uno antes de que se detecte un error en otro. Lo reproducimos en una base aislada. Las comprobaciones previas de archivos inválidos y conflictos siguen siendo válidas para los casos que cubren.

**Resultado y siguiente paso:** El importador valida todos los torneos del archivo antes de registrar candidatos y guarda cada archivo de metadatos en una transacción. Pasaron 18 pruebas, incluidas tres nuevas que cubren el rechazo íntegro, la reversión si falla el segundo torneo y el tratamiento de archivos en conflicto e independientes. El propietario confirmó en Streamlit la subida de un JSON con una lista y el rechazo de otro con una fecha inválida. Se verificó la lista guardada en SQLite. La [revisión de aceptación](mvp_acceptance.md) recoge los casos que quedan por comprobar.

### Entrada 018 — Etiquetas manuales cuando desaparece una lista (25/11/2026)

**Estado:** Comprobado en una sesión aislada de Streamlit.

**Qué hicimos:** Guardamos una etiqueta desde el formulario de Streamlit y subimos una nueva versión del torneo sin esa lista. SQLite dejó de devolver la lista, el archivo de etiquetas conservó su clave y Streamlit mostró el aviso, también al abrir otra sesión. Al volver a subir la versión original, reapareció la lista con su etiqueta y el aviso desapareció. Comprobamos que excluir la lista mediante un filtro tampoco activa el aviso.

**Resultado y siguiente paso:** La [revisión de aceptación](mvp_acceptance.md) recoge la evidencia. Quedan los límites de 15 días, 2 meses naturales y 3 meses naturales.

### Entrada 019 — Límites temporales y cierre de la revisión P0 (25/11/2026)

**Estado:** Comprobaciones de aceptación completadas. Entrega pendiente.

**Qué hicimos:** Ejecutamos Streamlit con los torneos de la copia de prueba y eventos ficticios situados en los límites de 15 días, 2 meses y 3 meses naturales. Confirmamos que entra el primer día de cada ventana y queda fuera el anterior. Los tres periodos incluyeron hoy y excluyeron mañana. Los recuentos de la tabla, la cobertura por torneo y los denominadores de la evolución coincidieron para cada selección.

**Resultado y siguiente paso:** La [revisión de aceptación](mvp_acceptance.md) reúne la evidencia de los criterios P0. La hoja de ruta pasa a la entrega del MVP local.

### Entrada 020 — Entrega del MVP local (25/11/2026)

**Estado:** Entrega verificada y cierre confirmado por el propietario.

**Qué hicimos:** Reunimos el código, los requisitos, las pruebas y la documentación en un ZIP. La [guía de entrega](local_delivery.md) explica el arranque en Windows, cómo transportar una instalación con sus datos y cómo hacer una demostración con la base de prueba.

**Resultado y siguiente paso:** La copia extraída arrancó en Streamlit con SQLite vacío y generó la base de demostración. Pasaron 17 pruebas y se omitió la que requiere el CSV del piloto local. El propietario dio por finalizado el MVP. El backlog recoge las propuestas de una fase posterior, incluida la extracción bajo demanda por fechas.

## Plantilla de próximas entradas

### Entrada NNN — [Fase o hito] ([fecha])
**Estado:** Pendiente / En curso / Terminado.

**Qué hicimos:** …

**Qué aprendimos:** …

**Decisiones y motivos:** …

**Papel de la IA:** …

**Resultado y siguiente paso:** …
