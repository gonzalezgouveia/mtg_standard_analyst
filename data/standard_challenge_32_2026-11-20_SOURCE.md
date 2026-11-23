# Procedencia del archivo de prueba

`standard_challenge_32_2026-11-20.csv` contiene los 32 registros de listas que aparecen publicados para el Standard Challenge 32 del 20 de noviembre de 2026. La tabla incluye jugador, posición, arquetipo y el total de 52 participantes reportado por la fuente; `deck_id` usa la posición como clave local porque la tabla consultada no muestra un identificador individual de lista.

- Fuente solicitada: [MTGO — Standard Challenge 32](https://www.mtgo.com/decklist/standard-challenge-32-2026-11-2012858925).
- La página de MTGO requiere JavaScript para mostrar el contenido en el lector usado durante esta preparación.
- Los registros se transcribieron de la ficha del mismo evento en [MTGpile](https://mtgpile.com/tournament/standard-challenge-32-2026-11-2012858925), cuya página enlaza MTGO como fuente e indica que hubo 52 participantes y que se publicaron las 32 listas del top 32.
- La columna `decklist` se deja vacía: no se recopilaron ni verificaron aquí las listas completas. `participants_total` vale 52 en cada fila porque ese es el total del evento, no el número de listas publicadas.

Por tanto, el archivo permite probar la importación, los recuentos y el gráfico sobre las 32 listas listadas, pero **no representa a los 52 participantes** ni se debe interpretar como el resultado de una importación automatizada de MTGO. Revisa los datos contra la página original antes de usarlos para análisis competitivo.
