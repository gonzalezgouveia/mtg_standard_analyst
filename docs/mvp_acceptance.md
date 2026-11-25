# Revisión de aceptación del MVP

**Fecha:** 25 de noviembre de 2026. **Resultado:** criterios P0 comprobados y cierre del MVP local confirmado por el propietario.

La revisión cruza los criterios P0 del [backlog](backlog.md) con la prueba manual en Streamlit, la consulta de SQLite, las pruebas automatizadas y la inspección del código. La batería pasó con 18 pruebas tras la corrección. El piloto real contiene seis torneos y 190 listas. Las comprobaciones con datos ficticios se hicieron en bases separadas.

| Criterio | Evidencia | Pendiente para cerrar |
|---|---|---|
| **ING-001** · Importación manual | El propietario subió dos CSV que seguían visibles al reiniciar y un JSON válido de una lista. Otro JSON mostró el aviso de fecha inválida y no se incorporó. Tras corregir el aviso de éxito, el propietario confirmó que el panel muestra «1 lista procesada» al volver a subir el JSON válido. La prueba aislada de Streamlit también verificó el aviso tras la recarga automática y que el JSON rechazado deja intacta la lista válida. Reimportar contenido idéntico no duplicó filas. | Comprobado. El panel admite un torneo por archivo. La carpeta local admite archivos con varios torneos. |
| **DAT-002** · Carga local al iniciar | El piloto se sincronizó desde la carpeta de datos. Una ejecución con base vacía inicializó SQLite. El importador informó del JSON inválido y mantuvo la versión anterior. Una prueba confirmó que un archivo válido independiente se importa durante la misma sincronización que rechaza un archivo inválido con varios torneos. El código excluye las etiquetas auxiliares y descubre los CSV de cartas por separado. | Los casos acordados de carga local están comprobados. |
| **DAT-003** · Persistencia y actualización | Las consultas y el esquema confirman las claves de listas y cartas y el total de participantes por torneo. Se verificaron la persistencia, la reimportación idéntica, el reemplazo de un torneo, el rechazo íntegro de archivos con datos inconsistentes o conflictos y la reversión tras un fallo de escritura en el segundo torneo. Las cartas del piloto original proceden del archivo complementario. Una prueba de Streamlit confirmó que una etiqueta manual se conserva y genera un aviso cuando se retira su lista, incluso en una sesión nueva. Al restaurarla, se reaplica la etiqueta y desaparece el aviso. | Comprobado. |
| **DAT-001** · Calidad y procedencia | El esquema guarda procedencia y hora de importación, tiene una fila por torneo y permite un total desconocido. El código valida los totales repetidos y conserva el título original al normalizar la categoría. El Challenge 32 original tiene 52 participantes y el Showcase tiene 183. El fallo de escritura inducido confirmó la conservación de los datos previos. | Los casos revisados de calidad y conservación de datos están comprobados. |
| **ANA-001** · Presencia y cobertura | Streamlit mostró recuentos, denominadores y porcentajes en la selección vigente. El día 24 mostró 7 de 32 listas «Sin etiquetar» (21,9 %). La cobertura de los seis eventos fue 190 de 457 (41,6 %). La base de prueba mostró cobertura incompleta al faltar un total y 25 % al excluir ese evento. El código agrupa las listas antes de calcular los porcentajes. | Los casos acordados de presencia y cobertura están comprobados. |
| **DASH-001** · Periodo | El selector ofrece 7, 15 y 30 días y 2 o 3 meses naturales, con 30 días por defecto. El propietario verificó el límite de 7 días. Una ejecución aislada de Streamlit verificó los límites de 15 días y 2 y 3 meses naturales, la inclusión de hoy y la exclusión de mañana. El contador, la cobertura por torneo y los denominadores de la evolución coincidieron con la tabla filtrada. | Comprobado. |
| **DASH-002** · Tipo de torneo | El piloto mostró 190 listas con Ambos, 158 con Standard Challenge y 32 con Showcase. La normalización del sufijo conserva el título original. El código aplica juntos los filtros de fecha y categoría. | Los casos acordados de categoría están comprobados. |
| **DASH-003** · Dashboard principal | El propietario vio la distribución y la evolución, confirmó el denominador de 64 para los dos torneos del día 20 y el aviso al filtrar sin resultados. Una ejecución aislada confirmó el aviso inicial con SQLite vacío. El indicador de última importación se mostró tras reiniciar Streamlit y la reimportación idéntica conservó la marca en SQLite. | Las comprobaciones acordadas de la vista principal están completadas. |

## Brecha reproducida en DAT-003

En una base aislada se cargaron dos torneos ficticios, A y B, desde un único JSON. Después se cambió un arquetipo de A y se añadió una segunda lista de B con una fecha distinta de la primera. El importador notificó el error de fecha en B, pero guardó el arquetipo nuevo de A. El resultado esperado es conservar las dos versiones previas cuando el archivo se rechaza, y permitir que otros archivos válidos e independientes se importen.

El importador anterior publicaba candidatos antes de terminar de validar el archivo y guardaba cada torneo en su propia transacción. El importador corregido valida primero todos los torneos de cada archivo de metadatos, detecta conflictos entre archivos válidos y guarda cada archivo admitido en una sola transacción. Las pruebas reproducen el defecto original y provocan un fallo de SQLite al guardar el segundo torneo para confirmar que se revierten también los cambios del primero.

## Comprobación de los límites temporales

El 25 de noviembre de 2026 se ejecutó Streamlit con los datos de la copia de prueba y un archivo temporal de eventos ficticios en los límites de cada periodo. Todas las ventanas incluyeron los eventos del 25 y excluyeron los del 26 de noviembre.

| Periodo | Primer día incluido | Día anterior excluido |
|---|---|---|
| 15 días | 11 de noviembre | 10 de noviembre |
| 2 meses naturales | 1 de octubre | 30 de septiembre |
| 3 meses naturales | 1 de septiembre | 31 de agosto |
