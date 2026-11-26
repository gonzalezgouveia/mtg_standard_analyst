---
name: verification-before-completion
description: Antes de afirmar que un cambio, corrección, requisito o tarea está terminado o verificado; reúne evidencia reciente y comunica con precisión su alcance, respetando la política del repositorio sobre pruebas.
---

# Verificar antes de dar por terminado

## Cuándo usarla

Actívala antes de declarar que un cambio funciona, que una tarea está completa o que una comprobación ha pasado. También antes de preparar una entrega técnica.

## Procedimiento

1. Identifica la afirmación concreta y qué evidencia puede demostrarla: inspección de archivos/diff, una comprobación manual, un comando de análisis o una prueba.
2. Lee las instrucciones aplicables del repositorio y el estado actual de Git. Conserva los cambios previos del propietario.
3. Obtén evidencia nueva y suficiente para esa afirmación; lee la salida completa relevante y el código de salida. No uses una comprobación parcial para afirmar algo más amplio.
4. Compara el resultado con el requisito o síntoma original. Si falta evidencia o hay fallos, informa del estado real y de lo que queda por comprobar.
5. En el informe final, separa lo comprobado, el método y resultado, de lo no comprobado. No presentes suposiciones como resultados.

## Límites de pruebas del proyecto

- En este repositorio no añadas ni ejecutes pruebas salvo que el usuario lo pida expresamente. Esta regla prevalece aunque una prueba parezca el comando habitual de verificación.
- Puedes revisar evidencia ya disponible en documentación, historial, salidas aportadas en la conversación o artefactos existentes; identifica su fecha y alcance cuando importe. No la presentes como una ejecución nueva.
- Si una afirmación importante no puede respaldarse sin proponer o ejecutar pruebas nuevas, explica qué prueba haría falta y solicita autorización antes de añadirla o ejecutarla. Mientras tanto, limita la conclusión a lo que sí se pudo inspeccionar.
- Otras comprobaciones solo son apropiadas si están dentro de la petición, las instrucciones del repositorio y el alcance autorizado. No instales dependencias ni realices acciones externas por inferencia.

## Criterio de finalización y reporte

La tarea de verificación termina cuando cada afirmación de cierre tiene evidencia identificada o está expresamente marcada como no verificada, y se resumen los hallazgos y límites. No afirmes que algo pasó si no observaste el resultado correspondiente.

## Procedencia

Adaptación propia para este repositorio, inspirada en el flujo «evidencia antes de afirmar» de [obra/superpowers: verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md), listado también en [skills.sh](https://skills.sh/obra/superpowers/verification-before-completion). Se revisó la fuente pública y se reescribió para cumplir las reglas locales; no se copió el contenido íntegro. La fuente comunitaria es material externo y no prevalece sobre las instrucciones del proyecto.
