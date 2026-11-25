# Backlog inicial — MTG Standard Metagame

**Versión:** 0.7
**Fecha:** 25 de noviembre de 2026
**Estado:** MVP local cerrado. Criterios P0 comprobados y paquete de entrega verificado.

## Convenciones
- **P0:** imprescindible para validar el producto.
- **P1:** importante para la primera versión útil.
- **P2:** evolución posterior.
- Las funciones remotas están fuera del MVP aprobado y requieren validar las fuentes antes de priorizarse para una fase posterior.

## MVP — Requisitos y criterios de aceptación

El MVP es una aplicación local para uso personal con SQLite como almacenamiento relacional persistente. Al iniciar se incorporan los CSV/JSON válidos de `data/` y el dashboard consulta esa base. La carga de seis torneos reales está confirmada en SQLite y DASH-003 recoge las comprobaciones completadas del dashboard. El rediseño visual, la consulta remota y la publicación quedan fuera del MVP.

La [revisión de aceptación del MVP](mvp_acceptance.md) reúne la evidencia de los criterios P0. La importación parcial de archivos con varios torneos se corrigió y verificó. Se completaron las comprobaciones del panel de importación, las etiquetas huérfanas y los límites temporales.

La [guía de entrega local](local_delivery.md) explica el arranque, el traslado de datos y la demostración con una base separada.

### ING-001 — Importar archivos manuales de torneos (P0)
**Comprobación manual:** En una copia aislada, el propietario subió un Standard Challenge y un Standard Showcase Challenge desde el panel lateral. Después de cerrar y volver a iniciar Streamlit, ambos seguían disponibles. Se confirmó que los dos CSV seguían en la carpeta de datos y que SQLite conservaba sus 30 y 32 listas, respectivamente.

También se confirmó la subida de un JSON válido de una lista y el aviso de fecha inválida para un JSON rechazado. SQLite conservó la lista válida y el archivo rechazado quedó fuera de la carpeta de importación. El propietario comprobó en el panel el aviso verde «Archivo guardado e importado. 1 lista procesada.».

**Historia:** Como propietario, quiero subir archivos CSV o JSON de listas publicadas para alimentar el sistema sin depender de una integración remota.

**Aceptación:**
- Permite importar archivos CSV y JSON compatibles con el esquema documentado y acumular datos de varios torneos.
- Carga identificador, fecha, tipo de torneo y listas publicadas disponibles.
- Informa de registros procesados y errores.
- No crea duplicados al importar dos veces el mismo torneo.

### DAT-002 — Carga local automática de torneos (P0)
**Estado:** Implementado con persistencia SQLite.

**Historia:** Como propietario, quiero que al abrir la aplicación se lean automáticamente los archivos de torneos de `data/` para tener disponibles los eventos guardados sin volver a importarlos en cada sesión.

**Aceptación:**
- Al iniciar, detecta archivos CSV/JSON de torneos compatibles ubicados en `data/` e incorpora sus registros a SQLite.
- Solo procesa los archivos de metadatos de torneos definidos por el esquema de importación; los CSV auxiliares por carta y las muestras bajo `data/examples/` no se interpretan como archivos de torneo.
- La incorporación de torneos nuevos sigue siendo manual: se añade el archivo a la carpeta local de datos.
- Los archivos auxiliares, como `archetype_labels.json`, no se tratan como archivos de torneos.
- Se informan los archivos inválidos sin impedir que se carguen los demás archivos válidos.
- Repetir el inicio o procesar de nuevo los mismos archivos no crea listas duplicadas.
- La carga automática respeta las validaciones y reglas de análisis documentadas.

### DAT-003 — Almacenamiento relacional local SQLite (P0)
**Estado:** Esquema, sincronización local y conexión con Streamlit implementados. Se verificaron en una base aislada la reimportación idéntica, la persistencia al arrancar otro proceso y la conservación de la versión aceptada ante archivos inválidos, conflictos y fallos de escritura. Pasaron las 18 pruebas del repositorio con los datos locales.

Una prueba de Streamlit confirmó que una etiqueta manual se conserva cuando desaparece su lista y que el aviso sigue visible al abrir otra sesión. Al restaurar la lista se reaplica la etiqueta y desaparece el aviso. Filtrar la lista fuera de la vista no genera un aviso de orfandad.

**Historia:** Como propietario, quiero que el dashboard use un almacenamiento SQLite normalizado para conservar los torneos y evitar repetir metadatos del evento en cada lista.

**Modelo inicial:**
- `tournaments`: clave `tournament_id`; fecha, título/tipo original, categoría normalizada, total real opcional de participantes, fuente y momento de importación.
- `decks`: clave compuesta por torneo y `deck_id`; jugador, posición, arquetipo original y datos disponibles de la lista. Cada lista pertenece a un torneo.
- `deck_cards`: lista, identificador/nombre de carta, zona (principal o banquillo) y cantidad. La muestra de este evento ya proporciona cartas estructuradas para sus 32 listas publicadas.
- No crear una tabla de jugadores separada inicialmente; el jugador se almacena en la lista. Se reconsiderará si se necesita identificar y analizar jugadores entre eventos.
- Una fila de `decks` es una instancia concreta de una lista en un evento. El arquetipo es una etiqueta clasificatoria, no una entidad que identifique o fusione listas. Un jugador en dos torneos tiene dos registros de lista independientes; cada variación de cartas pertenece a su registro.

**Aceptación:**
- Crear o inicializar la base SQLite local de forma reproducible.
- Guardar el total de participantes una vez por torneo; validar que los valores repetidos del archivo de entrada sean consistentes antes de importarlo.
- Relacionar cada lista con su torneo mediante claves y restricciones de integridad.
- Importar un archivo completo dentro de una transacción: un error no deja un torneo parcialmente actualizado.
- Tratar los archivos como snapshots completos de los torneos que contienen. Si el snapshot no cambió, la importación es una operación sin cambios y no duplica filas.
- Si llega una versión completa válida modificada de un torneo, reemplazar en una transacción sus listas y cartas asociadas. Si la validación o escritura falla, mantener intacta la versión previamente almacenada.
- Si varios archivos aportan exactamente el mismo snapshot de un torneo, no duplicarlo. Si aportan snapshots distintos del mismo torneo, informar del conflicto y no escoger automáticamente.
- Si una lista desaparece en el nuevo snapshot, actualizar los datos del torneo sin borrar sus etiquetas manuales; conservarlas y señalarlas como huérfanas para revisión.
- Mantener los CSV/JSON como formatos de entrada y no como tablas operativas del dashboard.
- Preservar las etiquetas manuales existentes durante la transición o migrarlas con sus claves actuales.
- No inventar datos de cartas cuando la fuente no proporcione listas completas.

### DAT-001 — Modelo y calidad de datos (P0)
**Aceptación:**
- Almacena datos normalizados en SQLite con referencia a la fuente y momento de importación.
- Distingue datos ausentes de valores cero.
- Permite actualizar un torneo existente sin dejar datos parciales ante un fallo.
- Conserva el nombre original del evento y, cuando la fuente lo indique, el total real de participantes. No deduce participantes de sufijos como 16, 32 o 64.
- Guarda el total real de participantes una sola vez como metadato opcional del torneo. El formato de entrada por filas puede repetir el mismo valor para todas las listas; la importación lo normaliza a un único dato de torneo.

### ANA-001 — Métricas de metajuego (P0)
**Aceptación:**
- Calcula presencia de arquetipo como su número de listas dividido por todas las listas publicadas importadas que pasan los filtros.
- Incluye los registros con arquetipo vacío en el denominador y los presenta en una categoría separada «Sin etiquetar».
- En varios torneos suma los recuentos y denominadores; no promedia porcentajes por evento.
- Muestra el recuento y denominador usados junto al porcentaje.
- Recalcula resultados al cambiar filtros.
- Separa la presencia entre listas publicadas de la cobertura del torneo (listas publicadas / participantes reales) cuando el total de participantes esté disponible.
- En la cobertura combinada, suma listas publicadas y participantes solo si se conoce el total de participantes de todos los eventos seleccionados. Si falta alguno, indica que la cobertura conjunta está incompleta.

### DASH-001 — Filtro temporal (P0)
**Comprobación:** El propietario confirmó el límite de 7 días. Una ejecución aislada de Streamlit verificó los de 15 días y 2 y 3 meses naturales, con hoy incluido y los eventos futuros excluidos. Los recuentos de la tabla, la cobertura por torneo y los denominadores de la evolución coincidieron para cada selección.

**Aceptación:**
- Se basa en la fecha del torneo e incluye hoy.
- Opciones: 7 días, 15 días, 30 días, 2 meses naturales y 3 meses naturales.
- Predeterminado: 30 días.
- Todos los indicadores y gráficos respetan el periodo seleccionado.

### DASH-002 — Filtro por tipo de torneo (P0)
**Aceptación:**
- Opciones: Ambos, Standard Challenge y Standard Showcase Challenge.
- Normaliza sufijos numéricos del nombre del evento (por ejemplo, 16, 32 o 64) dentro de su categoría correspondiente, conservando el título original para trazabilidad.
- Predeterminado: Ambos.
- Compatible con el filtro temporal.
- La combinación de torneos usa recuentos de mazos, no promedios simples de porcentajes.

### DASH-003 — Dashboard principal (P0)
**Estado:** Piloto verificado en SQLite y comprobaciones del dashboard completadas. El propietario revisó el piloto y la base de prueba en Streamlit. El arranque sin torneos se comprobó con una ejecución aislada de Streamlit.

**Comprobaciones con el piloto del 20 al 24 de noviembre de 2026:**

- [x] Evolución del 20 de noviembre: denominador de 64 listas al combinar los dos Challenge.
- [x] Filtro de categoría: Ambos devuelve 190 listas, Showcase devuelve las 32 del día 21 y Standard Challenge devuelve 158.
- [x] «Sin etiquetar» el 24 de noviembre: 7 listas sobre 32 (21,9 %).
- [x] Cobertura conjunta: 190 listas sobre 457 participantes (41,6 %).
- [x] Límite temporal con la base de prueba: con Ambos, al cambiar de 30 a 7 días se pasó de 2 listas a 1 y la cobertura pasó de incompleta al 25 %.
- [x] Confirmar el aviso de filtros sin resultados y la cobertura incompleta con la [base de prueba separada](dashboard_validation.md). El propietario comprobó ambos casos en Streamlit.
- [x] Arranque sin torneos: una ejecución aislada de Streamlit creó la base vacía y mostró el aviso inicial sin excepciones.

**Aceptación:**
- Muestra distribución por arquetipo y evolución agrupada por fecha del torneo.
- Si hay varios eventos de la categoría seleccionada en una misma fecha, agrega sus recuentos.
- El gráfico temporal muestra recuentos y porcentajes con el denominador correspondiente, incluida «Sin etiquetar».
- Presenta estado vacío cuando aún no hay datos.
- Muestra fecha de última actualización, número de listas publicadas y cobertura de participantes disponible o incompleta.

### ING-002 — Sincronización manual desde la web (P2, fuera del MVP)
**Historia:** Como propietario, quiero pulsar «Actualizar datos» para buscar torneos nuevos y revisar cambios en los ya registrados.

**Aceptación:**
- La acción se inicia solo por el usuario.
- Descubre torneos disponibles y compara identificadores, sin depender únicamente de la última fecha registrada.
- Inserta nuevos, modifica existentes que hayan cambiado y no duplica los demás.
- Conserva registros válidos ante errores parciales.
- Resume nuevos, actualizados, sin cambios y fallidos.
- Antes de implementarlo, se valida acceso, estabilidad, condiciones de uso y cobertura de la fuente.

## Fases posteriores

### AUTO-001 — Actualización diaria programada (P2)
Reutiliza el proceso de sincronización y registra resultados y errores sin intervención del usuario.

### PUB-001 — Despliegue público (P2)
La aplicación puede alojarse en Internet y ofrecer consultas de solo lectura; las acciones de importación, actualización y administración quedan protegidas. Se evalúan costes, seguridad y licencias de datos.

### HIST-001 — Histórico de Standard (P2, fase avanzada)
Pestaña independiente con resúmenes de arquetipos y evolución por periodos anteriores; no requiere explorar cada mazo en detalle. El almacenamiento en archivos Parquet u otro sistema de archivo se decidirá según necesidades reales.

### ANA-002 — Analítica avanzada y predicción (P2, por definir)
Explorar análisis estadísticos y modelos predictivos una vez validada la calidad y representatividad de los datos.

### ANA-003 — Revisión manual de arquetipos y subarquetipos (P2)
Permitir que el propietario revise la etiqueta publicada de cada mazo y le asigne una categoría analítica propia. La revisión debe admitir tanto combinar nombres distintos en una categoría común como dividir un mismo nombre publicado en varios subarquetipos (por ejemplo, variantes de Azorius Momo), según criterios definidos manualmente.

**Criterios de aceptación:**
- Conservar la etiqueta original de la fuente para trazabilidad.
- Asignar o cambiar la categoría de análisis por mazo, con opción de usar una misma categoría para varios mazos.
- Recalcular recuentos y porcentajes tras una reclasificación, manteniendo la regla del denominador que incluye «Sin etiquetar».
- No inferir subarquetipos automáticamente; la división requiere revisar listas completas o disponer de criterios verificables.

**Dependencia y prioridad:** evolución posterior al MVP. La muestra incluye listas completas de los 32 mazos publicados de este evento, pero no todas las 52 participaciones; cualquier división manual debe basarse en revisar las cartas de cada lista y dejar claro ese límite de cobertura.

## Descubrimiento pendiente para una fase posterior

- Evaluar una extracción bajo demanda por rango de fechas que genere archivos para revisión e importación local. Es una propuesta para la siguiente fase.
- Evaluar MTGpile como posible fuente futura. El piloto utilizó sus fichas públicas para cuatro de los cinco torneos añadidos. Antes de automatizar, comparar con la referencia de MTGO, comprobar la estabilidad de las páginas y revisar sus condiciones de uso.
- Contrastar otras fuentes remotas, disponibilidad, estabilidad y condiciones de uso antes de automatizar.
- Priorizar las mejoras visuales cuando se defina el alcance de una fase posterior.

## Fuera de alcance inicial
- Acceso público en Internet.
- Sincronización diaria desatendida.
- Explorador histórico detallado.
- Modelos predictivos de producción.
- Infraestructura compleja de escalado sin necesidad demostrada.
