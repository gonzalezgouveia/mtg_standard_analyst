# Formato de importación

El contenido de esta carpeta es local y Git lo ignora, excepto este README. CSV, JSON, archivos SQLite, etiquetas manuales y otros datos no se suben al repositorio. Cada persona debe conservar aquí sus datos locales; las muestras de prueba documentadas no forman parte de una clonación nueva.

Los datos se obtienen manualmente y se guardan como CSV UTF-8 o JSON que contenga una lista de objetos; cada fila/objeto representa una lista publicada de un torneo. Al iniciar, la aplicación incorpora archivos compatibles de la raíz de esta carpeta a SQLite; esa base es el almacenamiento operativo persistente. CSV de cartas separados se leen desde `examples/` o `cards/` si sus nombres terminan en `_cards.csv`. La consulta remota y la importación directa de HTML no forman parte del alcance actual.

Campos obligatorios: `tournament_id`, `tournament_date` (formato `YYYY-MM-DD`), `tournament_type` y `deck_id`. `deck_id` debe ser único dentro de cada torneo.

Campos opcionales: `player`, `placement`, `archetype`, `decklist`, `source_url` y `participants_total`. Déjalos vacíos si el dato no está disponible. Cada registro representa un mazo publicado; el número importado no debe interpretarse como el total de participantes.

`participants_total` es el total real de participantes del torneo según la fuente. En el formato por filas, repite el mismo entero positivo en todas las filas con ese `tournament_id`. Si la fuente no da el total, déjalo vacío en todas las filas del torneo. El importador rechaza valores no enteros, menores o iguales a cero, o inconsistentes dentro del mismo torneo; en SQLite el valor se almacena una sola vez en la tabla de torneos. El sufijo numérico del título (por ejemplo, 16, 32 o 64) no se usa como total de participantes.

Las etiquetas editadas en el dashboard se guardan en `archetype_labels.json`, identificadas por torneo y mazo. Al iniciar, los archivos de torneo se sincronizan con SQLite evitando duplicados. Para incorporar un torneo nuevo, añade aquí su archivo; también puedes usar el importador del panel lateral, que guarda el archivo en esta carpeta. Los archivos auxiliares como `archetype_labels.json` se ignoran. No rellenes el formato con datos inventados: usa únicamente información publicada que hayas importado manualmente.

Cada archivo debe contener un snapshot completo de cada torneo que incluya. La aplicación valida el archivo de metadatos entero y lo guarda en una sola transacción. Si falla la validación o la escritura, conserva las versiones anteriores. Reimportar el mismo snapshot no duplica registros. Si hay versiones contradictorias de un torneo, la aplicación avisa y rechaza los archivos implicados completos. Los archivos válidos independientes se siguen cargando. Si una lista desaparece de la versión nueva, sus etiquetas manuales se conservan para revisión.

Cada fila representa una lista concreta de un jugador en un torneo. La clave de identidad en SQLite será `tournament_id` + `deck_id`; el arquetipo solo clasifica la lista. No se deben combinar listas de jugadores distintos por compartir arquetipo, ni listas del mismo jugador en torneos distintos. La composición de cartas, cuando esté disponible, se relaciona con esa instancia de lista.

El número de registros representa las listas publicadas incluidas en los archivos, no necesariamente todos los participantes del evento. Las métricas deben indicar claramente cuántas listas se usan como base.

## Muestra complementaria de cartas

`examples/standard_challenge_32_2026-11-20_cards.csv` es un archivo provisional con una fila por carta y zona de cada lista publicada. Incluye torneo, lista, jugador, posición, arquetipo, zona (`mainboard` o `sideboard`), nombre de carta, cantidad y URL de la página de procedencia. Contiene 988 filas de cartas (684 filas de principal y 304 de banquillo), que suman 60 cartas principales y 15 de banquillo por cada una de las 32 listas. Las 32 listas se cotejaron con el CSV de metadatos por jugador, posición y arquetipo.

Se extrajo de las páginas públicas individuales de [MTGpile para el torneo](https://mtgpile.com/tournament/standard-challenge-32-2026-11-2012858925), que señalan MTGO como fuente. El archivo complementa las 32 listas publicadas, no las 52 participaciones del evento. La página oficial de MTGO fue consultada, pero requiere JavaScript en el lector usado; no se usó una conexión autenticada con MTGO. Al iniciar, la aplicación importa este archivo a `deck_cards` tras comprobar que sus listas coinciden con los metadatos.

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
