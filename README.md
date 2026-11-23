# MTG Standard Metagame Analytics — prototipo P01

Herramienta local para ayudarte a preparar torneos de Magic: The Gathering Standard mediante el análisis de listas publicadas. El MVP acordado usará SQLite como almacenamiento relacional persistente, importará CSV/JSON de varios torneos desde `data/`, y permitirá filtrarlos por fecha y tipo para consultar métricas por arquetipo y cobertura. La adaptación de la carga actual en memoria a SQLite y los filtros siguen en desarrollo.

La primera prueba técnica ya confirmó que una muestra local se importa y se muestra en el dashboard. La muestra de prueba incluye metadatos y cartas de 32 listas publicadas de un evento con 52 participantes, por lo que no representa a todo el torneo. Los archivos de datos se mantienen localmente y no se versionan con Git. La consulta remota, la publicación web y los cambios visuales se dejan para etapas posteriores.

## Requisitos y ejecución

Se recomienda Python 3.11 o posterior. Desde la raíz del repositorio:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

La implementación actual carga automáticamente los archivos CSV/JSON de torneos guardados en `data/` en la sesión actual; para añadir eventos nuevos, guarda allí el archivo siguiendo [data/README.md](data/README.md). La siguiente etapa es incorporar esos registros a SQLite para conservarlos y normalizarlos. La importación desde el panel lateral es temporal hasta que se implemente el almacenamiento SQLite.

Las etiquetas manuales se persisten actualmente en `data/archetype_labels.json`. SQLite será el almacenamiento normalizado previsto para torneos, listas y sus cartas; el total real de participantes se guardará una sola vez por torneo. El formato CSV/JSON puede repetirlo por fila para facilitar la importación. Los CSV, JSON, bases de datos y demás datos que se guarden dentro de `data/` se excluyen de Git; solo se versiona `data/README.md`.

## Documentación del proyecto

- [Visión del producto](docs/vision.md): usuario, propósito y límites aprobados del MVP.
- [Backlog](docs/backlog.md): criterios de aceptación y siguientes tareas.
- [Diario de aprendizaje](docs/learning_journal.md): decisiones, aprendizajes y colaboración entre el desarrollador y la IA.
- [Instrucciones para Codex](AGENTS.md): contexto y reglas de trabajo para agentes de IA.
- [Guía de datos](data/README.md): esquema de entrada, tratamiento local y límites de las muestras.

## Pruebas

```powershell
python -m pytest
```
