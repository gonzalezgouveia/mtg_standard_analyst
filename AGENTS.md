# Instrucciones del proyecto para Codex

## Contexto que debes leer
- Antes de cambiar producto o requisitos, lee `docs/vision.md` y `docs/backlog.md`.
- Consulta `data/README.md` para el esquema de importación y `data/*_SOURCE.md` para procedencia y límites de las muestras.
- Usa `docs/learning_journal.md` como historial del proceso y de las decisiones. Si contradice la visión o el backlog actuales, prevalecen la visión y el backlog.
- Consulta `docs/mvp_acceptance.md` para la evidencia del cierre del MVP y `docs/local_delivery.md` para el arranque y la entrega local.

## Alcance aprobado
- El MVP es una herramienta local y personal para preparar torneos de Magic: The Gathering Standard.
- El MVP usa SQLite como almacenamiento local relacional. Los archivos CSV o JSON guardados en `data/` son el formato de entrada y se incorporan automáticamente al almacenamiento al iniciar; el dashboard consulta los datos persistidos.
- El modelo separa torneos, listas publicadas y cartas por lista. El total real de participantes se guarda una vez por torneo en SQLite, aunque se repita por fila en el CSV/JSON de entrada.
- Cada lista publicada es una instancia independiente identificada por `(tournament_id, deck_id)`; jugador y arquetipo son atributos. No agrupes listas por arquetipo ni fusiones listas de un jugador entre torneos.
- Reimportar un snapshot idéntico no cambia ni duplica registros. Valida todos los torneos de cada archivo de metadatos antes de aplicar sus cambios en una única transacción. Si falla la validación o la escritura, conserva los datos anteriores. Si archivos válidos contienen snapshots contradictorios para el mismo torneo, informa el conflicto y rechaza los archivos implicados completos. Procesa por separado los archivos válidos independientes.
- Conserva las etiquetas manuales aunque una lista desaparezca en la nueva versión; marca la etiqueta como huérfana para revisión, no la elimines en silencio.
- La carga automática desde `data/` y el almacenamiento SQLite local están implementados. Los archivos inválidos o en conflicto deben reportarse sin sobrescribir registros válidos.
- Los CSV/JSON de metadatos se guardan en la raíz de `data/`; los CSV de cartas solo se cargan desde `data/examples/` y `data/cards/` cuando terminan en `_cards.csv`. No interpretes esos archivos como torneos.
- La base se crea en `data/mtg_standard_analyst.sqlite3`, que está excluida de Git. El importador manual del panel guarda el archivo validado en `data/` para conservarlo y cargarlo en futuros inicios.
- El MVP local está cerrado. El piloto, la base SQLite, las etiquetas y el ZIP de entrega se mantienen fuera de Git.
- La consulta remota, la automatización, el acceso público y el rediseño visual están fuera del MVP. No amplíes el alcance sin una decisión del propietario.

## Datos y análisis
- Cada fila importada representa un mazo publicado de un torneo; no necesariamente representa a todos sus participantes.
- La ausencia de la lista completa de cartas (`decklist`) no significa que el arquetipo sea desconocido. Si `archetype` está vacío, la categoría analítica es `Sin etiquetar`.
- Incluye `Sin etiquetar` en el denominador y muéstralo como categoría independiente.
- Combina torneos sumando recuentos y denominadores; no promedies porcentajes de eventos.
- Usa la fecha del torneo para los filtros y la evolución temporal. Los periodos incluyen hoy: 7, 15 o 30 días, o 2 o 3 meses naturales. Agrega los eventos que coincidan en una fecha.
- Separa la presencia del arquetipo entre listas importadas de la cobertura del evento frente a participantes reales. Calcula cobertura combinada solo si se conoce el total de participantes de todos los eventos incluidos; si no, indícala como incompleta.
- Conserva el título original del evento. Normaliza sus variantes numéricas en una categoría de torneo, pero nunca trates el sufijo como número de participantes.
- Trata `participants_total` como el total real informado por la fuente: es opcional y, cuando se conoce, debe repetirse de forma consistente en todas las filas del torneo; no lo deduzcas del título.
- Al trasladar los registros de importación a SQLite, normaliza `participants_total` en la entidad torneo; no mantengas copias contradictorias por lista.
- Conserva la etiqueta original de la fuente. Agrupa o divide arquetipos solo de forma manual y según criterios confirmados por el propietario; no infieras subarquetipos automáticamente.

## Forma de trabajar
- Mantén la documentación del producto en `docs/`; conserva en la raíz los puntos de entrada y configuración necesarios para ejecutar el proyecto.
- Considera las skills repo-locales de `.agents/skills/` cuando una tarea coincida con su flujo especializado. No son requisitos para toda tarea ni funciones de la aplicación; el propietario puede seleccionar una en Codex o pedirla por su nombre. La descripción orienta la selección automática, pero no la garantiza.
- No inventes ni completes datos de torneos sin una fuente verificable.
- Antes de editar, revisa el estado del repositorio y conserva cambios existentes del propietario.
- Resume los cambios y las comprobaciones realizadas.
- No hagas commit ni push sin autorización explícita del propietario.
