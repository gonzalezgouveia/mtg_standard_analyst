# Validación con una base de prueba

Esta comprobación usa dos eventos ficticios y una copia local del dashboard. La preparación genera un archivo JSON de entrada y una base SQLite en una carpeta nueva dentro de `data/.dashboard-tests/`. La carpeta hereda los permisos de `data/` para que se pueda abrir desde la terminal del usuario en Windows. El importador habitual solo busca archivos de torneos en la raíz de `data/`, así que la copia tiene sus propios datos y etiquetas.

## Preparar y abrir la copia

Desde la raíz del proyecto, con las dependencias instaladas, ejecuta:

```bash
python -m scripts.prepare_dashboard_fixture
```

El comando imprime la ruta de la copia. Usa esa ruta en el siguiente comando. El puerto 8502 permite abrirla junto a la aplicación habitual.

```bash
python -m streamlit run data/.dashboard-tests/dashboard-XXXX/app.py --server.port 8502
```

Abre `http://localhost:8502`. Genera la copia el mismo día que hagas la comprobación para que las fechas queden a ambos lados del límite de siete días. Para comprobar que una subida persiste al reiniciar, vuelve a abrir la misma copia. Si `python` no encuentra Streamlit, ejecuta ambos comandos con el Python que tiene instaladas las dependencias del proyecto.

## Resultados esperados

| Periodo | Tipo de torneo | Resultado esperado |
|---|---|---|
| 30 días | Ambos | 2 listas de 2 torneos. Cobertura conjunta «Incompleta». La tabla conserva el 25,0 % del evento con total conocido y muestra «Desconocido» para el otro total. |
| 7 días | Ambos | 1 lista del evento de hace 6 días y cobertura conjunta del 25,0 % (1 lista de 4 participantes). El evento de hace 7 días queda fuera. |
| 7 o 30 días | Standard Showcase Challenge | 0 listas y aviso «No hay listas para el periodo y el tipo de torneo seleccionados». |

Para probar también el arranque sin ningún torneo, detén la copia, crea otra carpeta con `app.py` y `src/` de la copia y arráncala con su carpeta `data/` vacía. Debería aparecer el aviso «No se encontraron torneos válidos». Cierra el servidor de la copia con `Ctrl+C` al terminar.
