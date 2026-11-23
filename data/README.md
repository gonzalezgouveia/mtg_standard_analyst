# Formato de importación

El MVP acordado usa importación manual de CSV UTF-8 o JSON que contenga una lista de objetos; cada fila/objeto representa una lista publicada de un torneo. Se podrán analizar varios torneos, incluso si se cargan desde archivos separados. La consulta remota y la importación directa de HTML no forman parte del alcance actual.

Campos obligatorios: `tournament_id`, `tournament_date` (formato `YYYY-MM-DD`), `tournament_type` y `deck_id`. `deck_id` debe ser único dentro de cada torneo.

Campos opcionales: `player`, `placement`, `archetype`, `decklist` y `source_url`. Déjalos vacíos si el dato no está disponible. Cada registro representa un mazo publicado; el número importado no debe interpretarse como el total de participantes.

Las etiquetas editadas en el dashboard se guardan en `archetype_labels.json`, identificadas por torneo y mazo. Los torneos importados se conservan solo durante la sesión actual de Streamlit; al abrir una sesión nueva hay que volver a importarlos. No rellenes el formato con datos inventados: usa únicamente información publicada que hayas importado manualmente.

El número de registros representa las listas publicadas incluidas en los archivos, no necesariamente todos los participantes del evento. Las métricas deben indicar claramente cuántas listas se usan como base.

## Encabezado CSV

```csv
tournament_id,tournament_date,tournament_type,deck_id,player,placement,archetype,decklist,source_url
```

## Ejemplo de estructura JSON vacía

```json
[]
```
