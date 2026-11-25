# Esquema de la base de datos

**Base local:** `data/mtg_standard_analyst.sqlite3`  
**Implementación:** `src/database.py`  
**Estado:** esquema implementado para el MVP.

Esta guía describe las tablas SQLite que usa la aplicación. La base se crea y actualiza automáticamente al iniciar Streamlit. Los CSV/JSON locales son la fuente de importación; esta base es el almacenamiento que consulta el dashboard. Los archivos de datos y la base permanecen localmente y están excluidos de Git.

## Cómo se relacionan las tablas

```text
tournaments 1 ─── N decks 1 ─── N deck_cards
     │
     ├────────── N tournament_sources
     └────────── 0..1 card_sources
```

Un torneo tiene varias listas. Cada lista es una instancia concreta de un jugador en ese torneo, identificada por `(tournament_id, deck_id)`. Las cartas pertenecen a esa instancia; compartir arquetipo no combina listas.

## `tournaments` — eventos

Una fila por torneo. El total de participantes se almacena aquí una sola vez.

| Columna | Tipo | Significado |
|---|---|---|
| `tournament_id` | TEXT, clave primaria | Identificador estable del evento y clave usada para relacionar sus datos. |
| `tournament_date` | TEXT | Fecha del torneo, guardada como texto con formato ISO (`AAAA-MM-DD`). |
| `tournament_type` | TEXT | Nombre original del tipo de evento publicado por la fuente, por ejemplo, con sufijo numérico. |
| `tournament_category` | TEXT | Categoría normalizada para agrupar variantes, como `Standard Challenge` o `Standard Showcase Challenge`. Puede quedar vacía si el tipo no está reconocido. |
| `participants_total` | INTEGER, opcional | Total real de participantes informado por la fuente. Debe ser mayor que cero si se conoce; `NULL` significa desconocido. |
| `source_url` | TEXT | URL del evento, si está disponible. |
| `snapshot_hash` | TEXT | Huella interna del contenido importado, usada para detectar si el archivo cambió. |
| `imported_at` | TEXT | Momento de la última importación aceptada, en formato ISO y UTC. |

## `decks` — listas publicadas

Una fila por lista publicada en un torneo. La clave primaria compuesta es `(tournament_id, deck_id)`.

| Columna | Tipo | Significado |
|---|---|---|
| `tournament_id` | TEXT, clave foránea | Torneo al que pertenece; referencia a `tournaments.tournament_id`. |
| `deck_id` | TEXT, parte de clave primaria | Identificador de esta lista dentro del torneo. |
| `player` | TEXT | Nombre del jugador, si está publicado. No hay una tabla separada de jugadores. |
| `placement` | TEXT | Puesto o resultado publicado; es texto para conservar formatos de posición. |
| `archetype` | TEXT | Etiqueta de arquetipo publicada. Clasifica la lista, pero no determina su identidad. Vacío significa que no está etiquetada. |
| `decklist` | TEXT | Campo de lista de entrada cuando existe. Las cartas normalizadas se guardan en `deck_cards`. |
| `source_url` | TEXT | URL de la lista individual, si está disponible. |

Si la fuente no publica la lista completa, la fila del mazo puede existir igualmente; eso no significa que el arquetipo esté sin etiquetar.

## `deck_cards` — cartas de cada lista

Una fila por carta y zona de una lista. La clave primaria compuesta es `(tournament_id, deck_id, zone, card_name)`.

| Columna | Tipo | Significado |
|---|---|---|
| `tournament_id` | TEXT, parte de clave y foránea | Torneo de la lista. |
| `deck_id` | TEXT, parte de clave y foránea | Lista concreta a la que pertenece la carta. La pareja con `tournament_id` referencia `decks`. |
| `zone` | TEXT | Zona: `mainboard` (mazo principal) o `sideboard` (banquillo). |
| `card_name` | TEXT | Nombre de la carta. |
| `quantity` | INTEGER | Copias de esa carta en esa zona; debe ser mayor que cero. |
| `source_url` | TEXT | URL de la lista o fuente de cartas, si está disponible. |

La combinación de clave impide duplicar la misma carta en la misma zona de la misma lista; si aparece en el archivo más de una vez, el importador lo valida antes de guardar.

## Tablas de procedencia de importación

Estas tablas son de control interno y permiten reconocer archivos repetidos o actualizados. No representan eventos o listas adicionales.

### `tournament_sources`

| Columna | Significado |
|---|---|
| `tournament_id` | Evento al que corresponde la fuente; referencia a `tournaments`. |
| `source_path` | Ruta relativa del archivo local importado. |
| `snapshot_hash` | Huella del contenido de ese archivo. |

La clave primaria es `(tournament_id, source_path)`. Puede haber más de un archivo idéntico registrado para el mismo torneo.

### `card_sources`

| Columna | Significado |
|---|---|
| `tournament_id` | Evento cuyas cartas se importaron; referencia a `tournaments`. Es clave primaria, por lo que se registra un snapshot actual de cartas por torneo. |
| `source_path` | Ruta relativa del CSV de cartas. |
| `snapshot_hash` | Huella del contenido de cartas importado. |
| `imported_at` | Momento de la última importación aceptada, en formato ISO y UTC. |

## Reglas de integridad y actualización

- Las claves foráneas conectan las listas con sus torneos y las cartas con su lista. Al reemplazar un snapshot válido, sus filas relacionadas se actualizan en cascada dentro de una transacción.
- Los snapshots idénticos se reconocen y no crean duplicados. Una versión completa modificada se valida y reemplaza de forma transaccional.
- Los archivos de metadatos se validan completos y se aplican en una sola transacción por archivo. Un archivo inválido o un fallo de escritura conserva los snapshots anteriores. Si varios archivos válidos discrepan sobre un torneo, se informa del conflicto y se rechazan los archivos implicados completos. Los archivos válidos independientes se procesan por separado.
- Las etiquetas manuales se guardan fuera de SQLite, en `data/archetype_labels.json`; no son una columna de la tabla `decks`.
- Los índices de `decks.player`, `decks.archetype` y `deck_cards.card_name` ayudan a consultas por esos campos.

Consulta la [guía de datos](../data/README.md) para ver el formato de entrada y la [guía de entrega](local_delivery.md) para arrancar o trasladar una instalación con su base local.
