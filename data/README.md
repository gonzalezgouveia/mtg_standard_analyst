# Formato de importación

Los datos se obtienen manualmente y se guardan como CSV UTF-8 o JSON que contenga una lista de objetos; cada fila/objeto representa una lista publicada de un torneo. El MVP incorporará automáticamente archivos de torneos compatibles desde esta carpeta a SQLite, incluidos varios eventos en archivos separados. SQLite será el almacenamiento operativo; los archivos son el formato de entrada. La consulta remota y la importación directa de HTML no forman parte del alcance actual.

Campos obligatorios: `tournament_id`, `tournament_date` (formato `YYYY-MM-DD`), `tournament_type` y `deck_id`. `deck_id` debe ser único dentro de cada torneo.

Campos opcionales: `player`, `placement`, `archetype`, `decklist`, `source_url` y `participants_total`. Déjalos vacíos si el dato no está disponible. Cada registro representa un mazo publicado; el número importado no debe interpretarse como el total de participantes.

`participants_total` es el total real de participantes del torneo según la fuente. En el formato por filas, repite el mismo entero positivo en todas las filas con ese `tournament_id`. Si la fuente no da el total, déjalo vacío en todas las filas del torneo. El importador rechaza valores no enteros, menores o iguales a cero, o inconsistentes dentro del mismo torneo; en SQLite el valor se almacena una sola vez en la tabla de torneos. El sufijo numérico del título (por ejemplo, 16, 32 o 64) no se usa como total de participantes.

Las etiquetas editadas en el dashboard se guardan actualmente en `archetype_labels.json`, identificadas por torneo y mazo. Al iniciar, la aplicación carga automáticamente los archivos CSV/JSON de torneos guardados en esta carpeta; el objetivo aprobado es incorporarlos a SQLite para persistencia, evitando duplicados. Para incorporar un torneo nuevo, añade aquí su archivo. Los archivos auxiliares como `archetype_labels.json` se ignoran. No rellenes el formato con datos inventados: usa únicamente información publicada que hayas importado manualmente.

Cada archivo debe representar un snapshot completo de los torneos que contiene. Reimportar el mismo snapshot no duplica registros. Una versión completa modificada reemplaza la versión anterior solo después de validarse correctamente. Si hay dos archivos con versiones contradictorias del mismo torneo, la aplicación debe señalar el conflicto y no decidir cuál prevalece. Si una lista desaparece del snapshot nuevo, sus etiquetas manuales se conservan para revisión.

Cada fila representa una lista concreta de un jugador en un torneo. La clave de identidad en SQLite será `tournament_id` + `deck_id`; el arquetipo solo clasifica la lista. No se deben combinar listas de jugadores distintos por compartir arquetipo, ni listas del mismo jugador en torneos distintos. La composición de cartas, cuando esté disponible, se relaciona con esa instancia de lista.

El número de registros representa las listas publicadas incluidas en los archivos, no necesariamente todos los participantes del evento. Las métricas deben indicar claramente cuántas listas se usan como base. La tabla de cartas por lista se usará cuando la fuente proporcione listas completas en formato estructurado; la muestra actual no contiene esa información.

## Encabezado CSV

```csv
tournament_id,tournament_date,tournament_type,deck_id,player,placement,archetype,decklist,source_url,participants_total
standard-challenge-32-2026-11-2012858925,2026-11-20,Standard Challenge 32,1,duanceyao,1,Jund Sacrifice,,https://mtgpile.com/tournament/standard-challenge-32-2026-11-2012858925,52
```

En el archivo completo del ejemplo, el valor `52` se repite en las 32 filas publicadas. Si se desconoce el total real, la última columna queda vacía en todas las filas de ese torneo.

## Ejemplo JSON

```json
[
  {
    "tournament_id": "standard-challenge-32-2026-11-2012858925",
    "tournament_date": "2026-11-20",
    "tournament_type": "Standard Challenge 32",
    "deck_id": "1",
    "player": "duanceyao",
    "placement": "1",
    "archetype": "Jund Sacrifice",
    "decklist": "",
    "source_url": "https://mtgpile.com/tournament/standard-challenge-32-2026-11-2012858925",
    "participants_total": 52
  }
]
```
