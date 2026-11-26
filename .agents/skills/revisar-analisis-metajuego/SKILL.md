---
name: revisar-analisis-metajuego
description: Revisa cálculos o interpretaciones del metajuego Standard sobre listas publicadas, arquetipos, filtros temporales, evolución y cobertura real de participantes.
---

# Revisar análisis del metajuego

## Cuándo usarla

Actívala al calcular, validar o explicar presencia por arquetipo, comparación entre torneos, evolución temporal, filtros o cobertura de participantes en los datos del proyecto.

## Procedimiento

1. Consulta `docs/vision.md`, `docs/backlog.md`, `data/README.md` y las notas de procedencia de los eventos analizados. La visión y el backlog vigentes prevalecen sobre decisiones históricas del `docs/learning_journal.md`. El MVP está cerrado; no propongas ampliar el producto como si ya estuviera aprobado.
2. Define la selección exacta: torneos incluidos, filtro de categoría y periodo. Filtra por fecha del torneo. Los periodos acordados incluyen hoy: 7, 15 o 30 días, o 2 o 3 meses naturales. Agrupa eventos que coincidan en una fecha.
3. Expresa siempre el universo y denominador de presencia: cada fila es un mazo publicado, no necesariamente un participante. Cuenta las listas importadas incluidas en el filtro; conserva `archetype` original y clasifica los vacíos como «Sin etiquetar», categoría visible que también forma parte del denominador. La ausencia de `decklist` no vuelve desconocido el arquetipo.
4. Al combinar eventos, suma recuentos y denominadores y calcula el porcentaje sobre esos totales; nunca promedies porcentajes de torneos. En la evolución, agrega primero por fecha y arquetipo y después calcula porcentajes con el denominador de listas de esa fecha.
5. Separa presencia entre listas publicadas de cobertura frente a participantes reales. Usa únicamente `participants_total` informado por la fuente, normalizado por torneo; no lo deduzcas del sufijo del título. La cobertura combinada solo es completa cuando se conoce el total de todos los eventos incluidos. Si falta en uno o más, indícala como incompleta y especifica qué información falta.
6. Conserva el título original. Puedes referirte a la categoría normalizada (Standard Challenge o Standard Showcase Challenge), pero no interpretes sufijos como 16, 32 o 64 como número de participantes. No agrupes ni dividas arquetipos de forma automática: cualquier recategorización debe ser manual y confirmada por el propietario.
7. Contrasta numeradores, denominadores, porcentajes y filtros con los datos o evidencia disponible. Si no puedes recalcular o inspeccionar una fuente, marca la cifra como no verificada y describe el límite; no inventes datos.

## Criterio de finalización y reporte

Entrega una conclusión reproducible con eventos y periodo seleccionados, recuentos, denominadores, porcentajes y fórmula de cobertura, diferenciando claramente listas publicadas de participantes reales. Señala «Sin etiquetar», valores faltantes, fuentes y límites que afectan la interpretación. Respeta la política del repositorio: no añadas ni ejecutes pruebas salvo petición expresa, y no cambies la aplicación ni el alcance aprobado al hacer una revisión analítica.
