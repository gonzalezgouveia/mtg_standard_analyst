---
name: revisar-importacion-torneos
description: Revisa archivos CSV o JSON de torneos Standard y su importación local a SQLite, incluidos validación, snapshots, conflictos, procedencia, participantes y etiquetas manuales.
---

# Revisar importaciones de torneos

## Cuándo usarla

Úsala al inspeccionar, preparar, diagnosticar o revisar una importación de torneos desde `data/`, una carga manual del panel o cambios en su flujo. No la uses para convertir archivos auxiliares de cartas en torneos.

## Procedimiento

1. Lee `AGENTS.md`, `data/README.md` y los archivos `data/*_SOURCE.md` pertinentes. Para cambios del producto, consulta también `docs/vision.md`, `docs/backlog.md` y la evidencia pertinente en `docs/mvp_acceptance.md` y `docs/learning_journal.md`. El MVP está cerrado: no amplíes el alcance sin decisión del propietario.
2. Revisa `git status` antes de editar. No alteres ni sobrescribas datos locales existentes; los archivos CSV/JSON del propietario, SQLite y etiquetas pueden quedar fuera de Git.
3. Confirma tipo y ubicación: CSV/JSON de metadatos en la raíz de `data/`; CSV de cartas solo en `data/examples/` o `data/cards/` y con sufijo `_cards.csv`. No interpretes `archetype_labels.json` ni otras muestras auxiliares como torneos.
4. Valida el archivo de metadatos completo antes de proponer escritura: campos obligatorios, fecha `YYYY-MM-DD`, `deck_id` único dentro del torneo y tipos/valores permitidos por el esquema. Cada fila es una lista publicada identificada por `(tournament_id, deck_id)`; no unas listas por jugador ni arquetipo.
5. Comprueba cada torneo dentro del archivo como snapshot completo. `participants_total` es opcional; si está informado, debe ser entero positivo y repetirse de forma consistente entre sus filas. No lo deduzcas del título ni del sufijo numérico. Conserva el título y la etiqueta de arquetipo originales y la procedencia; no rellenes datos ausentes.
6. Si se modifica el importador o se aplica una importación autorizada, exige estas propiedades: validar todos los torneos del archivo antes de escribir; aplicar cada archivo de metadatos válido en una sola transacción; un error de validación o escritura conserva íntegros los datos anteriores; snapshots idénticos son idempotentes; snapshots contradictorios del mismo torneo rechazan completos todos los archivos implicados; archivos válidos independientes se procesan por separado.
7. Al reemplazar un snapshot, comprueba que las etiquetas manuales se conservan si desaparece una lista y que se señalan como huérfanas para revisión. No borres etiquetas silenciosamente. Las cartas siguen vinculadas a la instancia concreta de lista.
8. Informa por archivo: aceptado, sin cambios, rechazado o en conflicto; torneos/listas afectados; evidencia disponible; origen y límites de la fuente; y cualquier dato que no pudo verificarse. No reportes solo un resultado agregado que oculte archivos rechazados.

## Alcance y finalización

Esta skill guía una revisión y no autoriza por sí sola a importar, modificar datos locales, editar la aplicación ni ampliar el MVP. Termina cuando los archivos y snapshots están clasificados con motivos, se han señalado los riesgos de integridad/procedencia y queda explícito qué requiere decisión del propietario. Respeta la instrucción del repositorio: no añadas ni ejecutes pruebas salvo petición expresa.
