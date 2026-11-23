# Instrucciones del proyecto para Codex

## Contexto que debes leer
- Antes de cambiar producto o requisitos, lee `docs/vision.md` y `docs/backlog.md`.
- Consulta `data/README.md` para el esquema de importación y `data/*_SOURCE.md` para procedencia y límites de las muestras.
- Usa `docs/learning_journal.md` como historial del proceso y de las decisiones. Si contradice la visión o el backlog actuales, prevalecen la visión y el backlog.

## Alcance aprobado
- El MVP es una herramienta local y personal para preparar torneos de Magic: The Gathering Standard.
- El MVP analiza listas publicadas importadas manualmente desde CSV o JSON, admite varios torneos y debe ofrecer filtros por fecha y tipo, métricas por arquetipo y cobertura explícita.
- La carga y visualización iniciales están verificadas; eso no significa que todos los criterios del MVP estén implementados.
- La consulta remota, la automatización, el acceso público y el rediseño visual están fuera del MVP. No amplíes el alcance sin una decisión del propietario.

## Datos y análisis
- Cada fila importada representa un mazo publicado de un torneo; no necesariamente representa a todos sus participantes.
- La ausencia de la lista completa de cartas (`decklist`) no significa que el arquetipo sea desconocido. Si `archetype` está vacío, la categoría analítica es `Sin etiquetar`.
- Incluye `Sin etiquetar` en el denominador y muéstralo como categoría independiente.
- Combina torneos sumando recuentos y denominadores; no promedies porcentajes de eventos.
- Conserva la etiqueta original de la fuente. Agrupa o divide arquetipos solo de forma manual y según criterios confirmados por el propietario; no infieras subarquetipos automáticamente.
- Distingue la proporción de arquetipos entre listas publicadas de la cobertura del torneo completo cuando se conozca el total de participantes.

## Forma de trabajar
- Mantén la documentación del producto en `docs/`; conserva en la raíz los puntos de entrada y configuración necesarios para ejecutar el proyecto.
- No inventes ni completes datos de torneos sin una fuente verificable.
- Antes de editar, revisa el estado del repositorio y conserva cambios existentes del propietario.
- Resume los cambios y las comprobaciones realizadas.
- No hagas commit ni push sin autorización explícita del propietario.
