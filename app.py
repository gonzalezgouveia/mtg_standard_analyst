from pathlib import Path
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data import (
    DataValidationError,
    add_display_archetype,
    deck_key,
    load_label_overrides,
    load_tournament_file,
    save_label_overrides,
)
from src.database import query_card_counts, query_decks, sync_local_data

ROOT = Path(__file__).parent
LABELS_PATH = ROOT / "data" / "archetype_labels.json"
DATA_PATH = ROOT / "data"
DATABASE_PATH = DATA_PATH / "mtg_standard_analyst.sqlite3"

st.set_page_config(page_title="MTG Standard Metagame", layout="wide")
st.title("MTG Standard Metagame Analytics")
st.caption("Análisis local de listas publicadas guardadas en la carpeta de datos.")

if "database_initialized" not in st.session_state:
    _, startup_errors = sync_local_data(DATA_PATH, DATABASE_PATH)
    st.session_state.startup_errors = startup_errors
    st.session_state.database_initialized = True
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
    st.caption("Los torneos se guardan en SQLite local. Al iniciar, se sincronizan los archivos de `data`.")
    st.header("Filtros del dashboard")
    period_label = st.selectbox(
        "Periodo del torneo",
        ["7 días", "15 días", "30 días", "2 meses naturales", "3 meses naturales"],
        index=2,
    )
    category_label = st.selectbox(
        "Tipo de torneo",
        ["Ambos", "Standard Challenge", "Standard Showcase Challenge"],
        index=0,
    )
    st.header("Importar torneo")
    uploaded = st.file_uploader("Archivo CSV o JSON", type=["csv", "json"])
    if uploaded is not None and st.button("Importar archivo", type="primary"):
        try:
            incoming = load_tournament_file(uploaded)
            if incoming["tournament_id"].nunique() != 1:
                raise DataValidationError(
                    "Desde el panel lateral importa un torneo por archivo. "
                    "Para cargar varios, guarda sus archivos en data."
                )
            filename = Path(uploaded.name).name
            if filename.lower() == "archetype_labels.json":
                raise DataValidationError("Ese nombre está reservado para las etiquetas manuales.")
            destination = DATA_PATH / filename
            old_content = destination.read_bytes() if destination.exists() else None
            destination.write_bytes(uploaded.getvalue())
            _, errors = sync_local_data(DATA_PATH, DATABASE_PATH)
            upload_errors = [error for error in errors if filename in error]
            if upload_errors:
                if old_content is None:
                    destination.unlink(missing_ok=True)
                else:
                    destination.write_bytes(old_content)
                sync_local_data(DATA_PATH, DATABASE_PATH)
                raise DataValidationError(" ".join(upload_errors))
            st.session_state.startup_errors = errors
            st.success(f"Archivo guardado en data e importado. {len(incoming)} listas procesadas.")
            st.rerun()
        except DataValidationError as exc:
            st.error(str(exc))
        except OSError as exc:
            st.error(f"No se pudo guardar o importar el archivo: {exc}")

data = query_decks(DATABASE_PATH)
if data.empty:
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

overrides = st.session_state.label_overrides
today = date.today()
if period_label.endswith("días"):
    days = int(period_label.split()[0])
    start_date = today - pd.Timedelta(days=days - 1)
else:
    months = int(period_label.split()[0])
    first_month = today.replace(day=1)
    start_date = (pd.Timestamp(first_month) - pd.DateOffset(months=months - 1)).date()

data["_tournament_date"] = pd.to_datetime(data["tournament_date"], errors="coerce").dt.date
filtered_data = data[data["_tournament_date"].between(start_date, today)].copy()
if category_label != "Ambos":
    filtered_data = filtered_data[filtered_data["tournament_category"] == category_label]
filtered_data = filtered_data.drop(columns="_tournament_date")
view = add_display_archetype(filtered_data, overrides)
all_view = add_display_archetype(data.drop(columns="_tournament_date"), overrides)
card_counts = query_card_counts(
    DATABASE_PATH, filtered_data["tournament_id"].drop_duplicates().tolist()
)
loaded_keys = {deck_key(row) for _, row in all_view.iterrows()}
orphaned_labels = set(overrides) - loaded_keys
if orphaned_labels:
    st.info(
        f"Se conservaron {len(orphaned_labels)} etiquetas manuales de listas que ya no están "
        "en los datos actuales; revísalas si actualizaste un torneo."
    )

st.caption(
    f"Periodo: {start_date:%Y-%m-%d} a {today:%Y-%m-%d} · Tipo: {category_label}. "
    f"Cobertura: {len(view)} mazos publicados en {view['tournament_id'].nunique()} torneo(s); "
    "no representa necesariamente a todos los participantes."
)
if view.empty:
    st.info("No hay listas para el periodo y el tipo de torneo seleccionados.")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mazos importados", len(view))
c2.metric("Jugadores identificados", view.loc[view.player != "", "player"].nunique())
c3.metric("Posiciones disponibles", int((view.placement != "").sum()))
c4.metric("Listas disponibles", int((view.decklist != "").sum()))

st.subheader("Cobertura de participantes")
if filtered_data.empty:
    st.info("No hay torneos seleccionados para calcular la cobertura.")
else:
    event_coverage = (
        filtered_data.groupby("tournament_id", as_index=False)
        .agg(
            Fecha=("tournament_date", "first"),
            Evento=("tournament_type", "first"),
            **{
                "Listas publicadas": ("deck_id", "size"),
                "Participantes reales": ("participants_total", "first"),
            },
        )
    )
    event_coverage["Participantes reales"] = pd.to_numeric(
        event_coverage["Participantes reales"], errors="coerce"
    )
    known_totals = event_coverage["Participantes reales"].notna()
    event_coverage["Cobertura (%)"] = None
    event_coverage.loc[known_totals, "Cobertura (%)"] = (
        event_coverage.loc[known_totals, "Listas publicadas"]
        / event_coverage.loc[known_totals, "Participantes reales"]
        * 100
    )
    event_coverage["Participantes reales"] = event_coverage["Participantes reales"].map(
        lambda value: int(value) if pd.notna(value) else "Desconocido"
    )
    st.dataframe(
        event_coverage[
            ["Fecha", "Evento", "Listas publicadas", "Participantes reales", "Cobertura (%)"]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Cobertura (%)": st.column_config.NumberColumn(format="%.1f%%"),
        },
    )
    if known_totals.all():
        total_participants = int(
            pd.to_numeric(event_coverage["Participantes reales"]).sum()
        )
        combined_coverage = len(filtered_data) / total_participants * 100
        st.metric(
            "Cobertura conjunta",
            f"{combined_coverage:.1f}%",
            help=(
                f"{len(filtered_data)} listas publicadas de {total_participants} participantes "
                "reales en los torneos seleccionados."
            ),
        )
    else:
        st.metric("Cobertura conjunta", "Incompleta")
        st.caption(
            "Falta el total real de participantes de al menos un torneo seleccionado; "
            "por eso no se calcula un porcentaje conjunto."
        )
if card_counts["rows"]:
    st.caption(
        f"Cartas registradas: {card_counts['rows']} filas de cartas en "
        f"{card_counts['decks']} listas."
    )

st.subheader("Evolución por fecha")
if view.empty:
    st.info("No hay listas para mostrar en la evolución del periodo seleccionado.")
else:
    evolution = (
        view.groupby(["tournament_date", "archetype_display"], as_index=False)
        .size()
        .rename(
            columns={
                "tournament_date": "Fecha",
                "archetype_display": "Arquetipo",
                "size": "Listas",
            }
        )
    )
    denominators = view.groupby("tournament_date").size()
    evolution["Denominador"] = evolution["Fecha"].map(denominators)
    evolution["Presencia (%)"] = evolution["Listas"] / evolution["Denominador"] * 100
    evolution["Fecha"] = pd.to_datetime(evolution["Fecha"])
    evolution = evolution.sort_values(["Fecha", "Arquetipo"])
    evolution_chart = px.line(
        evolution,
        x="Fecha",
        y="Presencia (%)",
        color="Arquetipo",
        markers=True,
        custom_data=["Listas", "Denominador"],
        labels={"Fecha": "Fecha del torneo", "Presencia (%)": "Presencia (%)"},
    )
    evolution_chart.update_traces(
        hovertemplate=(
            "%{fullData.name}<br>Fecha: %{x|%Y-%m-%d}<br>Presencia: %{y:.1f}%"
            "<br>Listas: %{customdata[0]} de %{customdata[1]}<extra></extra>"
        )
    )
    st.plotly_chart(evolution_chart, use_container_width=True)
    st.dataframe(
        evolution.assign(Fecha=evolution["Fecha"].dt.strftime("%Y-%m-%d")),
        use_container_width=True,
        hide_index=True,
        column_config={"Presencia (%)": st.column_config.NumberColumn(format="%.1f%%")},
    )

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Distribución de arquetipos")
    counts = view.groupby("archetype_display", dropna=False).size().reset_index(name="Mazos")
    denominator = len(view)
    if denominator:
        counts["Porcentaje"] = counts["Mazos"] / denominator * 100
        counts["Base"] = denominator
        fig = px.pie(
            counts,
            names="archetype_display",
            values="Mazos",
            hole=0.42,
            custom_data=["Porcentaje", "Base"],
        )
        fig.update_traces(
            textinfo="label+percent",
            hovertemplate=(
                "%{label}<br>Listas: %{value}<br>Presencia: %{customdata[0]:.1f}%"
                "<br>Base: %{customdata[1]} listas<extra></extra>"
            ),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Base del cálculo: {denominator} listas publicadas incluidas en los filtros.")
        st.dataframe(
            counts[["archetype_display", "Mazos", "Porcentaje", "Base"]].rename(
                columns={
                    "archetype_display": "Arquetipo",
                    "Mazos": "Listas",
                    "Porcentaje": "Presencia (%)",
                    "Base": "Denominador",
                }
            ),
            use_container_width=True,
            hide_index=True,
            column_config={"Presencia (%)": st.column_config.NumberColumn(format="%.1f%%")},
        )
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
unlabeled = all_view[all_view.archetype_display == "Sin etiquetar"]
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
