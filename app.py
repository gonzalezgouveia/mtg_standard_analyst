from pathlib import Path

import plotly.express as px
import streamlit as st

from src.data import (
    DataValidationError,
    add_display_archetype,
    deck_key,
    load_label_overrides,
    load_tournament_directory,
    load_tournament_file,
    save_label_overrides,
)

ROOT = Path(__file__).parent
LABELS_PATH = ROOT / "data" / "archetype_labels.json"
DATA_PATH = ROOT / "data"

st.set_page_config(page_title="MTG Standard Metagame", layout="wide")
st.title("MTG Standard Metagame Analytics")
st.caption("Análisis local de listas publicadas guardadas en la carpeta de datos.")

if "tournaments" not in st.session_state:
    st.session_state.tournaments, startup_errors = load_tournament_directory(DATA_PATH)
    st.session_state.startup_errors = startup_errors
if st.session_state.get("startup_errors"):
    with st.expander("Archivos de datos que no se pudieron cargar"):
        for error in st.session_state.startup_errors:
            st.warning(error)
if "label_overrides" not in st.session_state:
    try:
        st.session_state.label_overrides = load_label_overrides(LABELS_PATH)
    except DataValidationError as exc:
        st.session_state.label_overrides = {}
        st.error(str(exc))

with st.sidebar:
    st.caption("Al iniciar, se cargan los CSV/JSON de torneos guardados en la carpeta `data`. Para conservar un archivo importado, guárdalo allí.")
    st.header("Importar torneo")
    uploaded = st.file_uploader("Archivo CSV o JSON", type=["csv", "json"])
    if uploaded is not None and st.button("Importar archivo", type="primary"):
        try:
            incoming = load_tournament_file(uploaded)
            existing = st.session_state.tournaments
            if existing:
                import pandas as pd
                merged = pd.concat([*existing, incoming], ignore_index=True)
                # Revalidate combined imports to prevent duplicate deck records.
                from src.data import validate_records
                incoming_all = validate_records(merged.to_dict("records"))
                st.session_state.tournaments = [incoming_all]
            else:
                st.session_state.tournaments = [incoming]
            st.success(f"Importadas {len(incoming)} listas.")
        except DataValidationError as exc:
            st.error(str(exc))

if not st.session_state.tournaments:
    st.info(
        "No se encontraron torneos válidos en la carpeta `data`. Guarda allí un CSV o JSON "
        "con las listas publicadas, o impórtalo desde el panel lateral. No se consultan datos de MTGO automáticamente."
    )
    with st.expander("Formato de importación"):
        st.code(
            "tournament_id,tournament_date,tournament_type,deck_id,player,placement,archetype,decklist,source_url\n"
            "<id>,YYYY-MM-DD,<tipo>,<id-mazo>,<jugador>,<posición>,<arquetipo>,<lista>,<url>",
            language="csv",
        )
    st.stop()

import pandas as pd
data = pd.concat(st.session_state.tournaments, ignore_index=True)
overrides = st.session_state.label_overrides
view = add_display_archetype(data, overrides)

st.caption(
    f"Cobertura: {len(view)} mazos publicados importados en {view['tournament_id'].nunique()} torneo(s). "
    "No representa necesariamente a todos los participantes."
)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mazos importados", len(view))
c2.metric("Jugadores identificados", view.loc[view.player != "", "player"].nunique())
c3.metric("Posiciones disponibles", int((view.placement != "").sum()))
c4.metric("Listas disponibles", int((view.decklist != "").sum()))

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Distribución de arquetipos")
    counts = view.groupby("archetype_display", dropna=False).size().reset_index(name="Mazos")
    fig = px.pie(counts, names="archetype_display", values="Mazos", hole=0.42)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Mazos importados")
    st.dataframe(
        view[["tournament_id", "tournament_date", "tournament_type", "deck_id", "player", "placement", "archetype_display", "decklist", "source_url"]],
        use_container_width=True,
        hide_index=True,
        column_config={"archetype_display": "Arquetipo"},
    )

st.subheader("Etiquetado manual")
st.caption("Las etiquetas se guardan localmente en data/archetype_labels.json.")
unlabeled = view[view.archetype_display == "Sin etiquetar"]
if unlabeled.empty:
    st.write("Todos los mazos tienen una etiqueta de arquetipo.")
else:
    with st.form("label_form"):
        options = {deck_key(row): f"{row.tournament_id} · {row.deck_id}" for _, row in unlabeled.iterrows()}
        key = st.selectbox("Mazo", options=list(options), format_func=lambda item: options[item])
        label = st.text_input("Etiqueta de arquetipo")
        submitted = st.form_submit_button("Guardar etiqueta")
    if submitted:
        if label.strip():
            overrides[key] = label.strip()
            save_label_overrides(LABELS_PATH, overrides)
            st.session_state.label_overrides = overrides
            st.success("Etiqueta guardada.")
            st.rerun()
        else:
            st.warning("Escribe una etiqueta antes de guardarla.")
