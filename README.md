# MTG Standard Metagame Analytics — prototipo P01

Herramienta local para ayudarte a preparar torneos de Magic: The Gathering Standard mediante el análisis de listas publicadas. El MVP acordado permitirá importar manualmente datos de varios torneos, filtrarlos por fecha y tipo, y consultar recuentos y porcentajes por arquetipo con cobertura explícita. La visión y el alcance están aprobados; el MVP aún está en desarrollo.

La primera prueba técnica ya confirmó que la muestra incluida se importa y se muestra en el dashboard. La muestra contiene 32 listas publicadas de un evento con 52 participantes, por lo que no representa a todo el torneo. La consulta remota, la publicación web y los cambios visuales se dejan para etapas posteriores.

## Requisitos y ejecución

Se recomienda Python 3.11 o posterior. Desde la raíz del repositorio:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Al iniciar, la aplicación carga automáticamente los archivos CSV/JSON de torneos guardados en `data/`; para añadir eventos nuevos, guarda allí el archivo siguiendo [data/README.md](data/README.md). También se pueden importar archivos desde el panel lateral, aunque esa carga solo dura la sesión actual. Los filtros acordados también forman parte del trabajo pendiente del MVP.

Las etiquetas manuales se persisten en `data/archetype_labels.json`. Los archivos CSV/JSON de torneos guardados en `data/` se cargan al iniciar; los archivos inválidos se notifican y no impiden cargar los demás. El archivo de etiquetas no se trata como torneo.

## Documentación del proyecto

- [Visión del producto](docs/vision.md): usuario, propósito y límites aprobados del MVP.
- [Backlog](docs/backlog.md): criterios de aceptación y siguientes tareas.
- [Diario de aprendizaje](docs/learning_journal.md): decisiones, aprendizajes y colaboración entre el desarrollador y la IA.
- [Instrucciones para Codex](AGENTS.md): contexto y reglas de trabajo para agentes de IA.
- [Datos de ejemplo y procedencia](data/standard_challenge_32_2026-11-20_SOURCE.md): cobertura y limitaciones de la muestra.

## Pruebas

```powershell
python -m pytest
```
