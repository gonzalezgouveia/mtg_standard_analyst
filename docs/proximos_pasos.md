# Próximos pasos

El MVP local de MTG Standard Analyst está cerrado y validado. Puede servir como **versión 1.0.0** y punto de comparación para las próximas entregas. Las versiones de abajo son orientativas. El rediseño y la demo pueden avanzar por separado. La actualización programada depende de que la extracción por fechas funcione bien bajo demanda.

## Hitos propuestos

### 1. Rediseñar el dashboard · v1.1.0

Revisar cómo se usa el dashboard antes de un torneo. Empezar por una pantalla que haga fácil ver qué arquetipos tienen más presencia, cómo han cambiado y cuántas listas respaldan los porcentajes. Comparar dos bocetos con los mismos datos del piloto.

**Listo cuando** puedas responder esas preguntas con menos pasos y, para los mismos filtros, los resultados coincidan con los del MVP.

### 2. Traer torneos por fechas bajo demanda · v1.2.0

Probar dos rangos de fechas con Standard Challenge y Standard Showcase Challenge. Usar MTGO como referencia y contrastar la cobertura, la estabilidad y las condiciones de uso de la fuente candidata. La primera entrega puede ser un comando local que prepare archivos para revisar. Un botón en el dashboard puede ejecutar ese mismo proceso más adelante.

**Listo cuando** puedas elegir fechas, revisar qué torneos se encontraron y cuáles fallaron, e importar los válidos. Repetir un rango debe conservar los datos aceptados y evitar duplicados.

### 3. Publicar una demo gratuita de solo lectura · v1.3.0

La opción más directa es **Streamlit Community Cloud**, que permite publicar el dashboard de Python desde GitHub. La demo puede arrancar con un conjunto de datos revisado y mantener las importaciones y etiquetas en la instalación local. El almacenamiento del servidor no tiene persistencia garantizada. **GitHub Pages** es una alternativa si quieres practicar diseño web y construir una interfaz que lea datos preparados por Python. [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud) · [Persistencia de archivos](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data) · [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

**Listo cuando** otra persona pueda abrir el enlace, usar los filtros y entender de qué fecha son los datos y qué cobertura tienen.

### 4. Programar las actualizaciones · v1.4.0

Probar la extracción con una ejecución manual en GitHub Actions y, cuando sea fiable, programarla semanal o diariamente. Consultar varios días recientes permite recoger resultados publicados con retraso. En Streamlit se actualizaría el conjunto de datos publicado. En GitHub Pages, el mismo flujo generaría los datos y volvería a publicar el sitio. [Programación en GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

**Listo cuando** la demo se actualice sin que nadie tenga que abrirla, se vea el resultado de cada ejecución y se conserve la última versión válida si falla la fuente.

## Forma de trabajo y aprendizaje con IA

Crear un hito en GitHub por entrega, dividirlo en tareas pequeñas y trabajar cada cambio en una rama. Definir el problema y la comprobación antes de pedir a la IA que proponga opciones o implemente. Revisar los resultados con el piloto antes de integrar y etiquetar la entrega validada. Registrar en el diario una decisión, la aportación de la IA y cómo comprobaste el resultado.

## Ideas para más adelante

- Añadir un histórico por rotación de Standard para comparar periodos con contexto.
- Mostrar la procedencia y la cobertura de las listas con más detalle, para interpretar mejor las comparaciones entre torneos.
