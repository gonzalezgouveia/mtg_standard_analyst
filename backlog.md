# Backlog inicial — MTG Standard Metagame

**Versión:** 0.2  
**Fecha:** 23 de noviembre de 2026  
**Estado:** Alcance del MVP aprobado

## Convenciones
- **P0:** imprescindible para validar el producto.
- **P1:** importante para la primera versión útil.
- **P2:** evolución posterior.
- Las funciones remotas están fuera del MVP aprobado y requieren validar las fuentes antes de priorizarse para una fase posterior.

## MVP — Requisitos y criterios de aceptación

El MVP es una aplicación local para uso personal, con importación manual de CSV/JSON, análisis de varios torneos, filtros por fecha y tipo, y métricas por arquetipo con cobertura explícita. La carga y visualización de una primera muestra ya se verificaron; el rediseño visual, la consulta remota y la publicación quedan fuera de este alcance.

### ING-001 — Importar archivos manuales de torneos (P0)
**Historia:** Como propietario, quiero subir archivos CSV o JSON de listas publicadas para alimentar el sistema sin depender de una integración remota.

**Aceptación:**
- Permite importar archivos CSV y JSON compatibles con el esquema documentado y acumular datos de varios torneos.
- Carga identificador, fecha, tipo de torneo y listas publicadas disponibles.
- Informa de registros procesados y errores.
- No crea duplicados al importar dos veces el mismo torneo.

### DAT-001 — Modelo y calidad de datos (P0)
**Aceptación:**
- Almacena datos normalizados con referencia a la fuente y momento de importación.
- Distingue datos ausentes de valores cero.
- Permite actualizar un torneo existente sin dejar datos parciales ante un fallo.

### ANA-001 — Métricas de metajuego (P0)
**Aceptación:**
- Calcula recuentos y porcentajes de arquetipos a partir de los mazos publicados y disponibles.
- Identifica el número de mazos usado como denominador.
- Recalcula resultados al cambiar filtros.
- Advierte de cobertura incompleta cuando corresponda.

### DASH-001 — Filtro temporal (P0)
**Aceptación:**
- Opciones: 7 días, 15 días, 30 días, 2 meses y 3 meses.
- Predeterminado: 30 días.
- Todos los indicadores y gráficos respetan el periodo seleccionado.

### DASH-002 — Filtro por tipo de torneo (P0)
**Aceptación:**
- Opciones: Ambos, Standard Challenge, Showcase Challenge.
- Predeterminado: Ambos.
- Compatible con el filtro temporal.
- La combinación de torneos usa recuentos de mazos, no promedios simples de porcentajes.

### DASH-003 — Dashboard principal (P0)
**Aceptación:**
- Muestra al menos distribución por arquetipo y evolución temporal con los datos disponibles.
- Presenta estado vacío cuando aún no hay datos.
- Muestra fecha de última actualización y cobertura.

### ING-002 — Sincronización manual desde la web (P2, fuera del MVP)
**Historia:** Como propietario, quiero pulsar «Actualizar datos» para buscar torneos nuevos y revisar cambios en los ya registrados.

**Aceptación:**
- La acción se inicia solo por el usuario.
- Descubre torneos disponibles y compara identificadores, sin depender únicamente de la última fecha registrada.
- Inserta nuevos, modifica existentes que hayan cambiado y no duplica los demás.
- Conserva registros válidos ante errores parciales.
- Resume nuevos, actualizados, sin cambios y fallidos.
- Antes de implementarlo, se valida acceso, estabilidad, condiciones de uso y cobertura de la fuente.

## Fases posteriores

### AUTO-001 — Actualización diaria programada (P2)
Reutiliza el proceso de sincronización y registra resultados y errores sin intervención del usuario.

### PUB-001 — Despliegue público (P2)
La aplicación puede alojarse en Internet y ofrecer consultas de solo lectura; las acciones de importación, actualización y administración quedan protegidas. Se evalúan costes, seguridad y licencias de datos.

### HIST-001 — Histórico de Standard (P2, fase avanzada)
Pestaña independiente con resúmenes de arquetipos y evolución por periodos anteriores; no requiere explorar cada mazo en detalle. El almacenamiento en archivos Parquet u otro sistema de archivo se decidirá según necesidades reales.

### ANA-002 — Analítica avanzada y predicción (P2, por definir)
Explorar análisis estadísticos y modelos predictivos una vez validada la calidad y representatividad de los datos.

## Siguientes tareas para completar el MVP
1. Probar importación de varios torneos y comprobar que no se duplican registros.
2. Implementar filtros temporales y por tipo de torneo con el comportamiento acordado.
3. Calcular recuentos y porcentajes por arquetipo usando el total de listas publicadas disponibles como denominador.
4. Mostrar cobertura y limitaciones de representatividad junto a los resultados.
5. Validar los datos y resultados con varias fuentes/torneos publicados.
6. Revisar los criterios de aceptación y documentar el resultado antes de ampliar el alcance.

## Descubrimiento pendiente para una fase posterior
- Identificar y validar fuentes remotas, disponibilidad, estabilidad y condiciones de uso antes de automatizar.
- Decidir si se necesita persistencia entre sesiones; actualmente los torneos cargados viven en la sesión de Streamlit.
- Priorizar mejoras visuales después de completar la validación funcional del MVP.

## Fuera de alcance inicial
- Acceso público en Internet.
- Sincronización diaria desatendida.
- Explorador histórico detallado.
- Modelos predictivos de producción.
- Infraestructura compleja de escalado sin necesidad demostrada.
