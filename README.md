# MTG Standard Metagame Analytics — MVP local

Herramienta local para ayudarte a preparar torneos de Magic: The Gathering Standard mediante el análisis de listas publicadas. El MVP usa SQLite como almacenamiento relacional persistente e importa CSV/JSON desde `data/`. El dashboard incluye filtros por fecha y tipo, presencia de arquetipos, cobertura de participantes y evolución por fecha.

El piloto local reúne 190 listas publicadas de seis torneos de MTGO celebrados del 20 al 24 de noviembre de 2026. Incluye cartas estructuradas para las 32 listas del torneo original. El backlog recoge las comprobaciones del dashboard completadas con el piloto y una base de prueba separada. La aplicación muestra la última importación aceptada para los torneos seleccionados. Los archivos de datos se mantienen localmente y no se versionan con Git. La consulta remota, la publicación web y el rediseño visual se dejan para etapas posteriores.

## Requisitos y ejecución

Se recomienda Python 3.11 o posterior. Desde la raíz del proyecto, en Git Bash o PowerShell:

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -m streamlit run app.py
```

Al iniciar, la aplicación valida los archivos CSV/JSON de torneos en `data/` y los sincroniza con la base SQLite local. Los archivos de cartas con sufijo `_cards.csv` se leen desde `data/examples/` o `data/cards/`. La importación del panel lateral guarda el archivo validado en `data/` y lo sincroniza con la base.

Las etiquetas manuales se persisten en `data/archetype_labels.json`. SQLite normaliza torneos, listas y cartas; el total de participantes se almacena una sola vez por torneo. Los CSV, JSON, bases de datos y demás datos dentro de `data/` se excluyen de Git; solo se versiona `data/README.md`. Por tanto, al clonar el repositorio hay que añadir los propios archivos locales de torneo si se quieren ver datos.

## Documentación del proyecto

- [Entrega y arranque local](docs/local_delivery.md): instalación, traslado de datos y demostración.
- [Revisión de aceptación](docs/mvp_acceptance.md): evidencia de las comprobaciones del MVP.
- [Visión del producto](docs/vision.md): usuario, propósito y límites aprobados del MVP.
- [Backlog](docs/backlog.md): criterios de aceptación y siguientes tareas.
- [Esquema de la base de datos](docs/database_schema.md): tablas, columnas, relaciones y reglas de integridad de SQLite.
- [Diario de aprendizaje](docs/learning_journal.md): decisiones, aprendizajes y colaboración entre el desarrollador y la IA.
- [Instrucciones para Codex](AGENTS.md): contexto y reglas de trabajo para agentes de IA.
- [Guía de datos](data/README.md): esquema de entrada, tratamiento local y límites de las muestras.

## Pruebas

```powershell
python -m pytest
```
