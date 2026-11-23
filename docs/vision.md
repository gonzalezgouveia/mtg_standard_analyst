# Visión de producto — MTG Standard Metagame

**Versión:** 0.4
**Fecha:** 23 de noviembre de 2026
**Estado:** Aprobada para orientar el MVP

## 1. Propósito
Crear una aplicación web de análisis del metajuego competitivo de Magic: The Gathering en formato Standard, centrada inicialmente en torneos Standard Challenge y Standard Showcase Challenge. Su objetivo principal es ayudar al propietario a preparar torneos mediante información reciente y comprensible sobre arquetipos, presencia en el metajuego y evolución temporal.

Como objetivo secundario, el producto podrá publicarse en Internet para otros jugadores y funcionar como portfolio técnico de ingeniería y análisis de datos, incluyendo el desarrollo asistido por IA.

## 2. Usuario y contexto
- **MVP:** un único usuario, ejecución local y acceso personal.
- **Futuro:** visitantes públicos con acceso de solo lectura; administración restringida.
- **Contexto de uso:** consultar el metajuego reciente antes de competir en Standard.

## 3. Propuesta de valor
Unificar datos de torneos publicados, limpiarlos, clasificarlos y transformarlos en indicadores y gráficos filtrables. Mostrar claramente la cobertura y limitaciones de los datos para evitar conclusiones engañosas.

## 4. Alcance funcional previsto
### MVP
- Aplicación local para uso personal, enfocada en preparar torneos de Standard.
- Mantener los archivos CSV o JSON de torneos en la carpeta local `data/` y cargar automáticamente todos los torneos válidos al abrir la aplicación. Los archivos nuevos se incorporan manualmente a esa carpeta; no se requiere volver a importarlos en cada sesión. La importación HTML y cualquier consulta remota quedan sujetas a validación posterior.
- Mostrar distribución por arquetipo mediante recuentos y porcentajes sobre las listas publicadas importadas que pasan los filtros. Los mazos sin arquetipo se incluyen en el denominador como categoría «Sin etiquetar».
- Filtro temporal basado en la fecha del torneo: 7, 15 o 30 días, o 2 o 3 meses naturales; el periodo predeterminado es 30 días e incluye hoy.
- Filtro por categoría normalizada: Ambos (predeterminado), Standard Challenge o Standard Showcase Challenge. Se conserva el nombre original del evento; sufijos numéricos como 16, 32 o 64 no se interpretan como total de participantes.
- Evolución temporal agrupada por fecha del torneo. Si hay varios eventos seleccionados en la misma fecha, se suman sus listas; el gráfico presenta porcentajes y recuentos con su denominador.
- Evitar duplicados y mostrar errores de importación.
- Conservar los torneos entre sesiones mediante sus archivos locales y volver a leerlos al iniciar; excluir de la lectura automática archivos auxiliares que no sean datos de torneos.
- Mostrar por separado la proporción de arquetipos entre listas publicadas y la cobertura del torneo (listas publicadas frente a participantes reales), solo cuando el total de participantes esté disponible.
- Al combinar torneos, sumar listas y participantes; mostrar la cobertura conjunta como incompleta si falta el total de participantes de algún evento.
- La carga y visualización iniciales se probaron satisfactoriamente con el torneo de muestra del 20 de noviembre de 2026. Esta prueba técnica no valida todavía todos los criterios del MVP.

### Fuera del MVP acordado
- Rediseño visual y cambios de presentación; se posponen hasta después de completar la validación funcional.
- Actualización automática o consulta remota de torneos.
- Publicación web o acceso público.

### Evolución posterior
- Actualización diaria programada reutilizando la lógica de sincronización manual.
- Publicación web con consultas públicas y operaciones administrativas protegidas.
- Pestaña «Histórico de Standard» con visualizaciones resumidas por periodos, sin detalle exhaustivo de mazos.
- Archivado o almacenamiento histórico optimizado solo si el volumen o el rendimiento lo justifican.
- Mejoras analíticas y modelos predictivos, pendientes de definición y priorización.

## 5. Principios de diseño
- Separar ingesta, transformación, almacenamiento, análisis y presentación.
- Mantener trazabilidad de las fuentes y fechas de actualización.
- No asumir que los datos publicados representan la totalidad de los participantes.
- Evitar duplicados y permitir actualizar registros existentes sin perder datos válidos ante fallos.
- Priorizar simplicidad en el MVP y extensibilidad razonable.
- Validar condiciones de acceso y reutilización de las fuentes antes de automatizar o publicar.

## 6. Flujo de trabajo del desarrollo
- Planificar y aprobar requisitos antes de implementar.
- Trabajar en VS Code con Codex y GitHub.
- El agente puede proponer cambios y ejecutar pruebas, pero **no debe hacer commit ni push sin confirmación explícita del propietario**.
- Documentar y validar cada hito antes de avanzar.

## 7. Decisiones pendientes
- Fuente exacta y viabilidad de la extracción remota de torneos.
- Criterios detallados para agrupar o dividir arquetipos manualmente, como evolución posterior al MVP.
- Arquitectura futura y estrategia de despliegue, si se decide publicar el producto.
- Qué funcionalidades analíticas avanzadas entran en versiones posteriores.
