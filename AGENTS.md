# Instrucciones del proyecto para Codex

## Contexto que debes leer
- Antes de cambiar producto o requisitos, lee `docs/vision.md` y `docs/backlog.md`.
- Consulta `data/README.md` para el esquema de importación y `data/*_SOURCE.md` para procedencia y límites de las muestras.
- Usa `docs/learning_journal.md` como historial del proceso y de las decisiones. Si contradice la visión o el backlog actuales, prevalecen la visión y el backlog.

## Alcance aprobado
- El MVP es una herramienta local y personal para preparar torneos de Magic: The Gathering Standard.
- El MVP analiza listas publicadas desde archivos CSV o JSON guardados localmente en `data/`; al iniciar, debe detectar y cargar automáticamente los torneos disponibles, admitir varios eventos y ofrecer filtros por fecha y categoría normalizada (Standard Challenge o Standard Showcase Challenge), métricas por arquetipo y cobertura explícita.
- La carga automática desde `data/` está implementada: el arranque carga archivos CSV/JSON de torneo y reporta archivos inválidos sin bloquear los válidos. Una importación desde el panel lateral solo dura la sesión; para conservarla, guarda el archivo en `data/`.
- La carga y visualización iniciales están verificadas; eso no significa que todos los criterios del MVP estén implementados.
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
- Conserva la etiqueta original de la fuente. Agrupa o divide arquetipos solo de forma manual y según criterios confirmados por el propietario; no infieras subarquetipos automáticamente.

## Forma de trabajar
- Mantén la documentación del producto en `docs/`; conserva en la raíz los puntos de entrada y configuración necesarios para ejecutar el proyecto.
- No inventes ni completes datos de torneos sin una fuente verificable.
- Antes de editar, revisa el estado del repositorio y conserva cambios existentes del propietario.
- Resume los cambios y las comprobaciones realizadas.
- No hagas commit ni push sin autorización explícita del propietario.
