# Diario de aprendizaje — MTG Standard Metagame

**Versión:** 0.4 · **Inicio:** 21/11/2026 · **Actualizado:** 23/11/2026

Este documento registra brevemente qué hacemos, qué aprendemos y cómo colaboramos con la IA. Se actualizará al cerrar cada fase o hito importante. Los estados son orientativos y podrán cambiar.

## Hoja de ruta del proyecto

- [x] **1. Descubrimiento inicial:** identificar el problema, los usuarios y el objetivo del producto.
- [x] **2. Primeros borradores:** preparar la visión y el backlog iniciales.
- [x] **3. Revisar y validar la visión:** prioridad confirmada: ayudar al propietario a preparar torneos de Standard con datos recientes.
- [x] **4. Refinar y priorizar el backlog:** MVP local, importación manual CSV/JSON de varios torneos, filtros por fecha y tipo, recuentos y porcentajes por arquetipo y cobertura visible. Rediseño visual, automatización y acceso público quedan fuera.
- [ ] **5. Diseño funcional y de datos:** acordar métricas y denominadores, reglas de clasificación y cobertura.
- [x] **6. Prueba técnica inicial:** cargar la muestra en Streamlit y comprobar que se visualiza. La viabilidad de fuentes remotas queda pendiente y fuera del MVP.
- [ ] **7. Diseño de arquitectura:** Streamlit y Python ya están elegidos para el prototipo; falta cerrar persistencia y estructura a medida que se definan las necesidades.
- [x] **8. Preparación del desarrollo:** repositorio, entorno local, documentación, pruebas iniciales y flujo de trabajo con IA preparados.
- [ ] **9. Desarrollo iterativo del MVP:** en curso; completar filtros, métricas y cobertura.
- [ ] **10. Pruebas y validación:** verificar resultados, calidad de datos y requisitos.
- [ ] **11. Entrega del MVP:** documentación, ejecución local y demostración.
- [ ] **12. Evolución posterior:** publicación web, automatización e histórico, según prioridades.

**Estado actual:** visión y alcance del MVP aprobados el 23/11/2026. Se comprobó manualmente que la muestra se carga y se visualiza. El foco pasa a completar y validar los criterios funcionales acordados; no se ha validado una integración remota.

> **Terminología:** *Discovery* o descubrimiento es la fase de comprensión del problema. **Licitación** es un proceso para solicitar y evaluar ofertas de proveedores; no es una fase necesaria en este proyecto individual. Después del descubrimiento suelen venir definición, diseño, implementación, validación y entrega, con iteraciones entre ellas.

## Registro de aprendizaje

### Entrada 001 — Descubrimiento inicial (21/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Pasamos de la idea de analizar el metajuego de Magic: The Gathering Standard a los primeros borradores de visión y backlog. Delimitamos un MVP local y dejamos para más adelante la publicación web y otras mejoras.

**Qué aprendimos:** La visión explica el propósito y el valor del producto; el backlog organiza requisitos; el MVP acota la primera versión útil. El descubrimiento precede a las decisiones técnicas detalladas.

**Decisiones:** Revisar y aprobar los borradores antes de diseñar la arquitectura. Validar la viabilidad de las fuentes de datos antes de depender de ellas.

**Papel de la IA:** Apoyar el análisis y la redacción; las decisiones finales y su validación corresponden al desarrollador.

**Siguiente paso:** Revisar la visión y registrar los cambios acordados. Completado en la entrada 002.

### Entrada 002 — Aprobación de visión y alcance del MVP (23/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Confirmamos que la prioridad es preparar torneos propios de Standard con datos recientes. Se revisó la muestra disponible en Streamlit y el propietario verificó que la importación y las gráficas iniciales funcionan.

**Qué aprendimos:** La prueba inicial confirma que se pueden cargar y mostrar los datos de muestra; no demuestra todavía que el MVP completo cumpla filtros, métricas y cobertura.

**Decisiones y motivos:** El MVP será local y de uso personal, con importación manual CSV/JSON de varios torneos, filtros temporales y por tipo, y recuentos y porcentajes por arquetipo con cobertura explícita. Se posponen el rediseño visual, la actualización remota y el acceso público.

**Papel de la IA:** Ayudó a resumir los borradores, señalar la diferencia entre una muestra de listas publicadas y el total de participantes, y traducir las decisiones del propietario en alcance y criterios de aceptación. La IA no ejecutó la comprobación visual: el propietario abrió la aplicación, importó el archivo y confirmó el resultado.

**Resultado y siguiente paso:** Visión y alcance aprobados. Completar y validar los criterios funcionales del MVP con datos de varios torneos.

**Reflexión sobre programación con IA:** Este hito muestra un uso de la IA como apoyo para leer documentación, comparar el prototipo con los requisitos, proponer una estructura de MVP y mantener un registro claro de decisiones. La persona desarrolladora conserva el criterio y valida el comportamiento real ejecutando la aplicación; la IA ayuda a convertir esa evidencia en tareas concretas y documentación revisable.

### Entrada 003 — Pruebas de Git, conexión con GitHub y permisos (23/11/2026)
**Estado:** Terminado.

**Qué hicimos:** Intentamos preparar y subir cambios del proyecto y, después, realizamos pruebas controladas con `push_test.txt`. La primera sesión no pudo escribir en el índice de Git porque `.git` estaba en modo de solo lectura, aunque sí podía editar archivos del proyecto. Más adelante, al elegir un permiso más amplio, apareció una ventana de GitHub para autorizar la conexión con la aplicación. Una vez completada esa conexión, se pudo crear y subir un commit de prueba; también se subió un commit que eliminó ese primer archivo. Finalmente, con el modo **Ask for approval / Solicitar aprobación**, se aprobó la petición concreta para preparar el segundo archivo, crear el commit y hacer push. GitHub recibió el commit y la rama local quedó sincronizada.

**Qué aprendimos:** La autorización de GitHub y los permisos de Codex son dos cosas distintas. La conexión con GitHub permite autenticar las operaciones contra el repositorio remoto; el modo de permisos controla si Codex puede modificar los metadatos locales de Git y acceder a la red. Tener una de estas dos cosas no sustituye a la otra. El modo de aprobación puede funcionar sin mantener acceso total, siempre que la cuenta de GitHub ya esté conectada y se apruebe la solicitud de permisos cuando aparezca.

**Decisiones y motivos:** Para trabajar con este repositorio, mantener la cuenta de GitHub conectada en la aplicación y usar **Ask for approval / Solicitar aprobación** como modo habitual. Aprobar la petición específica cuando una operación de Git necesite más acceso. Reservar **Full access / Acceso completo** para situaciones puntuales, no como requisito permanente.

**Papel de la IA:** La IA preparó y ejecutó las operaciones de Git solicitadas, explicó la diferencia entre conexión remota y permisos del entorno, y comprobó el estado final de la rama. El propietario completó la autorización de GitHub y aprobó las operaciones solicitadas.

**Resultado y siguiente paso:** Se comprobó que el flujo de commit y push funciona después de conectar GitHub y conceder la aprobación requerida. En futuras operaciones, verificar primero que GitHub sigue conectado y aceptar la solicitud de aprobación de Codex si aparece. Esta prueba valida el flujo de Git, no los criterios funcionales del MVP.

## Plantilla de próximas entradas

### Entrada NNN — [Fase o hito] ([fecha])
**Estado:** Pendiente / En curso / Terminado.

**Qué hicimos:** …

**Qué aprendimos:** …

**Decisiones y motivos:** …

**Papel de la IA:** …

**Resultado y siguiente paso:** …
