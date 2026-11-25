# Entrega del MVP local

**Fecha de entrega:** 25 de noviembre de 2026.

MTG Standard Metagame Analytics permite importar torneos de Standard y consultar presencia por arquetipo, evolución por fecha y cobertura de participantes. Está preparado para uso local y guarda los torneos en SQLite.

## Instalación y arranque en Windows

Abre Git Bash o PowerShell en la carpeta que contiene `app.py`. Con Python 3.11 o posterior, ejecuta estos comandos la primera vez:

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Para abrir la aplicación, ejecuta:

```bash
./.venv/Scripts/python.exe -m streamlit run app.py
```

Abre la dirección local que indique Streamlit. Usa `Ctrl+C` en la misma terminal para detenerlo. Si aparece `No module named streamlit`, vuelve a ejecutar el comando de instalación con el mismo Python del entorno virtual.

## Añadir y trasladar los datos

- Una instalación recién extraída arranca sin torneos y crea su base SQLite al iniciar. Añade CSV o JSON compatibles a `data/` o usa **Importar torneo** en el panel lateral para cargar un torneo por archivo. Consulta la [guía de datos](../data/README.md) para ver el formato y la ubicación de los archivos de cartas.
- Para trasladar una instalación con sus datos, cierra Streamlit y copia los CSV/JSON de torneos, los archivos de cartas de `data/examples/` o `data/cards/`, la base `data/mtg_standard_analyst.sqlite3` y `data/archetype_labels.json` si existe. Conserva un respaldo antes de reemplazar archivos de destino.
- El ZIP incluye código, requisitos, pruebas y documentación. Los torneos del piloto, la base de uso local y las etiquetas personales permanecen en la instalación de origen. El piloto documentado tiene 190 listas publicadas de seis torneos.

## Demostración y comprobaciones

Para explorar el dashboard sin cargar torneos reales, usa la [guía de la base de prueba](dashboard_validation.md). El MVP acepta archivos locales, guarda las importaciones y conserva los datos válidos ante rechazos. Se comprobaron los filtros, la cobertura, las etiquetas huérfanas y la evolución. Los resultados y los casos revisados están en la [revisión de aceptación](mvp_acceptance.md).

Para volver a ejecutar las pruebas desde la raíz del proyecto:

```bash
./.venv/Scripts/python.exe -m pytest
```

La prueba que lee el CSV del piloto se omite si ese archivo local no está presente. El [backlog](backlog.md) reúne las mejoras que se pueden priorizar después de esta entrega.
