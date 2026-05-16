import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="UISEK — Deserción Estudiantil",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .big-title  { font-size:2.1rem; font-weight:700; color:#e8f4ff; margin-bottom:.2rem; }
    .sec-title  { font-size:1.2rem; font-weight:700; color:#7ecfff; margin:1rem 0 .4rem 0; }
    .insight    { background:#1a3a5c; border-left:4px solid #42a5f5;
                  padding:.7rem 1rem; border-radius:0 8px 8px 0;
                  margin:.5rem 0; font-size:.87rem; line-height:1.6;
                  color:#d6eaff !important; }
    .insight *  { color:#d6eaff !important; }
    .warn       { background:#3d2e00; border-left:4px solid #ffb300;
                  padding:.7rem 1rem; border-radius:0 8px 8px 0;
                  margin:.5rem 0; font-size:.87rem; line-height:1.6;
                  color:#ffe9a0 !important; }
    .warn *     { color:#ffe9a0 !important; }
    .ok         { background:#1a3b1e; border-left:4px solid #66bb6a;
                  padding:.7rem 1rem; border-radius:0 8px 8px 0;
                  margin:.5rem 0; font-size:.87rem; line-height:1.6;
                  color:#c8f0ca !important; }
    .ok *       { color:#c8f0ca !important; }
    .danger     { background:#3e0a15; border-left:4px solid #ef5350;
                  padding:.7rem 1rem; border-radius:0 8px 8px 0;
                  margin:.5rem 0; font-size:.87rem; line-height:1.6;
                  color:#ffd6de !important; }
    .danger *   { color:#ffd6de !important; }
    div[data-testid="stMetricValue"] { font-size:1.7rem !important; font-weight:700 !important; }
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ─────────────────────────────────────────────────────────────
@st.cache_data
def cargar():
    return pd.read_csv("uisek_desercion_CLEAN.csv")

df = cargar()

COLS_NUM = [
    "semestre_actual", "promedio_notas", "asistencia_porcentaje",
    "materias_reprobadas_acum", "trabaja", "horas_trabajo_semanal",
    "actividad_canvas_semanal", "tiene_beca", "deuda_pendiente_usd",
    "vive_fuera_de_quito", "visitas_tutoria_semestre", "participa_extracurricular",
]
COLS_CLAVE = [
    "promedio_notas", "asistencia_porcentaje", "materias_reprobadas_acum",
    "horas_trabajo_semanal", "deuda_pendiente_usd", "visitas_tutoria_semestre",
]
C0, C1 = "#2E7D32", "#E05555"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 UISEK — Filtros")
    st.markdown("---")
    carreras = ["Todas"] + sorted(df["carrera"].unique())
    carrera_sel  = st.selectbox("📚 Carrera", carreras)
    sem_max_val  = int(df["semestre_actual"].max())
    sem_range    = st.slider("📅 Semestre", 1, sem_max_val, (1, sem_max_val))
    beca_sel     = st.radio("🎖️ Beca",    ["Todos", "Con beca", "Sin beca"])
    trabaja_sel  = st.radio("💼 Trabaja",  ["Todos", "Trabaja", "No trabaja"])
    st.markdown("---")
    st.caption("📁 uisek_desercion_CLEAN.csv")

# ── Filtrado ───────────────────────────────────────────────────────────────────
df_f = df.copy()
if carrera_sel != "Todas":
    df_f = df_f[df_f["carrera"] == carrera_sel]
df_f = df_f[df_f["semestre_actual"].between(*sem_range)]
if beca_sel    == "Con beca":    df_f = df_f[df_f["tiene_beca"] == 1]
elif beca_sel  == "Sin beca":    df_f = df_f[df_f["tiene_beca"] == 0]
if trabaja_sel == "Trabaja":     df_f = df_f[df_f["trabaja"] == 1]
elif trabaja_sel == "No trabaja":df_f = df_f[df_f["trabaja"] == 0]

n = len(df_f)
if n == 0:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ── Pre-cómputos globales ──────────────────────────────────────────────────────
deser_rate  = df_f["deserto_semestre"].mean() * 100
g0          = df_f[df_f["deserto_semestre"] == 0]
g1          = df_f[df_f["deserto_semestre"] == 1]
corr_matrix = df_f[COLS_NUM + ["deserto_semestre"]].corr()
corr_target = corr_matrix["deserto_semestre"].drop("deserto_semestre")

# ── Header & KPIs ──────────────────────────────────────────────────────────────
st.markdown('<div class="big-title">🎓 Dashboard EDA — Deserción Estudiantil UISEK</div>',
            unsafe_allow_html=True)
st.markdown(
    f"**{n:,} estudiantes** filtrados de {len(df):,} totales &nbsp;·&nbsp; "
    f"Ingeniería de Data Science"
)
st.markdown("---")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🚨 Tasa de Deserción",  f"{deser_rate:.1f}%",
          f"{deser_rate - df['deserto_semestre'].mean()*100:+.1f}pp vs total")
k2.metric("📝 Promedio Notas",     f"{df_f['promedio_notas'].mean():.2f}")
k3.metric("📅 Asistencia",         f"{df_f['asistencia_porcentaje'].mean():.1f}%")
k4.metric("💰 Deuda Promedio",     f"${df_f['deuda_pendiente_usd'].mean():,.0f}")
k5.metric("🎖️ Con Beca",          f"{df_f['tiene_beca'].mean()*100:.1f}%")
st.markdown("---")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Estadísticas Descriptivas",
    "📦 Distribuciones",
    "🔗 Análisis Bivariado",
    "🌡️ Correlaciones",
    "📋 Perfil & Resumen",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ESTADÍSTICAS DESCRIPTIVAS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-title">📊 Estadísticas Descriptivas Avanzadas</div>',
                unsafe_allow_html=True)

    def dist_label(sk):
        a = abs(sk)
        if a < 0.5:  return "simétrica"
        if a < 1.0:  return "moderadamente sesgada"
        return "muy sesgada"

    stats_rows = []
    for col in COLS_NUM:
        s  = df_f[col]
        sk = s.skew()
        ku = s.kurt()
        stats_rows.append({
            "Variable": col, "Media": round(s.mean(), 2), "Mediana": round(s.median(), 2),
            "Std": round(s.std(), 2), "Min": round(s.min(), 2), "Max": round(s.max(), 2),
            "Skewness": round(sk, 2), "Kurtosis": round(ku, 2),
            "Distribución": dist_label(sk),
        })

    stats_df = pd.DataFrame(stats_rows)

    def color_dist(val):
        m = {"simétrica": "background:#e8f5e9;color:#1b5e20",
             "muy sesgada": "background:#fce4ec;color:#b71c1c",
             "moderadamente sesgada": "background:#fff8e1;color:#e65100"}
        return m.get(val, "")

    def color_skew(val):
        if abs(val) >= 1:  return "color:#c62828;font-weight:600"
        if abs(val) >= .5: return "color:#e65100"
        return "color:#2e7d32"

    st.dataframe(
        stats_df.style
        .map(color_dist, subset=["Distribución"])
        .map(color_skew,  subset=["Skewness"])
        .format({"Media":"{:.2f}","Mediana":"{:.2f}","Std":"{:.2f}",
                 "Min":"{:.2f}","Max":"{:.2f}","Skewness":"{:.2f}","Kurtosis":"{:.2f}"}),
        use_container_width=True, hide_index=True,
    )

    sesgadas   = stats_df[stats_df["Distribución"] == "muy sesgada"]["Variable"].tolist()
    m_gt_med   = stats_df[stats_df["Media"] > stats_df["Mediana"]]["Variable"].tolist()

    st.markdown(
        f'<div class="insight">💡 <b>Skewness &gt; 1</b> → distribución muy sesgada → puede necesitar '
        f'transformación logarítmica<br>Variables afectadas: '
        f'<b>{", ".join(sesgadas) if sesgadas else "ninguna"}</b></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="warn">💡 <b>Media &gt; Mediana</b> → cola larga hacia la derecha. '
        f'Variables: <b>{", ".join(m_gt_med[:5])}</b> muestran muchos estudiantes en valores bajos.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<div class="sec-title">📊 Distribución por Carrera</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        cnt = df_f["carrera"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 4))
        pal = sns.color_palette("Blues_d", len(cnt))
        ax.barh(cnt.index, cnt.values, color=pal[::-1])
        for i, v in enumerate(cnt.values):
            ax.text(v + .5, i, str(v), va="center", fontsize=9)
        ax.set_xlabel("Número de estudiantes")
        ax.set_title("Estudiantes por Carrera", fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    with col_b:
        churn_c = df_f.groupby("carrera")["deserto_semestre"].mean().sort_values() * 100
        fig, ax = plt.subplots(figsize=(7, 4))
        colores_c = [C1 if v > deser_rate else C0 for v in churn_c]
        ax.barh(churn_c.index, churn_c.values, color=colores_c)
        ax.axvline(deser_rate, linestyle="--", color="black", alpha=.5,
                   label=f"Media global {deser_rate:.1f}%")
        for i, v in enumerate(churn_c.values):
            ax.text(v + .3, i, f"{v:.1f}%", va="center", fontsize=9)
        ax.set_xlabel("Tasa de Deserción (%)")
        ax.set_title("Tasa de Deserción por Carrera", fontweight="bold")
        ax.legend(fontsize=8); ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig); plt.close()

    st.markdown(
        f'<div class="insight">💡 La tasa de deserción global es del <b>{deser_rate:.1f}%</b>, '
        f'aproximadamente 1 de cada {round(100/deser_rate):.0f} estudiantes deserta en el semestre.<br>'
        f'Existe disparidad notable entre carreras, lo que sugiere factores específicos por facultad.</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DISTRIBUCIONES (boxplots + violin)
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-title">📦 Boxplots — Detección de Outliers (Persiste vs Deserta)</div>',
                unsafe_allow_html=True)

    n_cols_bp = 3
    n_rows_bp = int(np.ceil(len(COLS_NUM) / n_cols_bp))
    fig, axes = plt.subplots(n_rows_bp, n_cols_bp, figsize=(16, n_rows_bp * 3.3))
    axes = axes.flatten()

    for i, col in enumerate(COLS_NUM):
        ax = axes[i]
        d0 = df_f[df_f["deserto_semestre"] == 0][col].dropna()
        d1 = df_f[df_f["deserto_semestre"] == 1][col].dropna()
        bp = ax.boxplot(
            [d0, d1], patch_artist=True, notch=False,
            medianprops={"color": "black", "linewidth": 2},
            flierprops={"marker": "o", "markerfacecolor": C1, "markersize": 4, "alpha": .5},
        )
        bp["boxes"][0].set_facecolor("#a8d5a2")
        bp["boxes"][1].set_facecolor("#f5a0a0")
        ax.set_title(col.replace("_", " "), fontsize=9, fontweight="bold")
        ax.set_xticklabels(["Persiste", "Deserta"], fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)

    for j in range(len(COLS_NUM), len(axes)):
        axes[j].set_visible(False)

    plt.suptitle("Distribuciones por Estado de Deserción — Boxplots",
                 fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown(
        '<div class="insight">💡 Los puntos rojos fuera de los bigotes son <b>outliers</b> '
        'según la regla IQR (&gt; Q3 + 1.5×IQR).<br>'
        'Variables como <b>materias_reprobadas_acum</b> o <b>horas_trabajo_semanal</b> '
        'pueden mostrar casos atípicos relevantes.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<div class="sec-title">🎻 Violin Plots — Forma de la Distribución por Grupo</div>',
                unsafe_allow_html=True)

    df_vio = df_f.copy()
    df_vio["grupo"] = df_vio["deserto_semestre"].map({0: "Persiste (0)", 1: "Deserta (1)"})

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()

    for i, col in enumerate(COLS_CLAVE):
        ax = axes[i]
        sns.violinplot(
            data=df_vio, x="grupo", y=col, ax=ax,
            order=["Persiste (0)", "Deserta (1)"],
            palette={"Persiste (0)": "#a8d5a2", "Deserta (1)": "#f5a0a0"},
            inner="box", cut=0,
        )
        ax.set_title(col.replace("_", " "), fontweight="bold")
        ax.set_xlabel("")
        ax.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Violin Plots — Comparación Persiste vs Deserta",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown(
        '<div class="insight">💡 <b>Interpretación de violin plots:</b><br>'
        '· <b>promedio_notas</b>: los estudiantes que desertan tienden a tener promedios más bajos.<br>'
        '· <b>materias_reprobadas_acum</b>: los desertores suelen tener más materias reprobadas.<br>'
        '· <b>asistencia_porcentaje</b>: la asistencia es menor en el grupo que deserta.</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANÁLISIS BIVARIADO
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-title">📊 Resumen Bivariado — Medias por Grupo y Diferencia</div>',
                unsafe_allow_html=True)

    biv_rows = []
    for col in COLS_NUM:
        m0v   = g0[col].mean()
        m1v   = g1[col].mean()
        diff  = m1v - m0v
        pstd  = df_f[col].std()
        d     = abs(diff) / pstd if pstd > 0 else 0
        poder = "🔴 ALTO" if d > 0.3 else ("🟡 MEDIO" if d > 0.1 else "🟢 BAJO")
        arrow = "↑" if diff > 0 else "↓"
        biv_rows.append({
            "Variable": col,
            "No Deserta": round(m0v, 2),
            "Deserta": round(m1v, 2),
            "Diff": f"{arrow}  {abs(diff):.2f}",
            "Cohen d": round(d, 3),
            "Poder": poder,
        })

    biv_df = pd.DataFrame(biv_rows)

    def color_poder(val):
        if "ALTO"  in val: return "background:#fce4ec;color:#b71c1c;font-weight:600"
        if "MEDIO" in val: return "background:#fff8e1;color:#e65100;font-weight:600"
        return "background:#e8f5e9;color:#2e7d32"

    st.dataframe(
        biv_df.style.map(color_poder, subset=["Poder"]),
        use_container_width=True, hide_index=True,
    )

    st.markdown(
        '<div class="insight">💡 <b>↑</b> = deserción tiene valores <b>más altos</b> &nbsp;|&nbsp; '
        '<b>↓</b> = deserción tiene valores <b>más bajos</b><br>'
        '<b>Poder (d de Cohen):</b> 🔴 ALTO &gt;0.3 &nbsp;|&nbsp; 🟡 MEDIO 0.1–0.3 &nbsp;|&nbsp; '
        '🟢 BAJO &lt;0.1</div>',
        unsafe_allow_html=True,
    )

    # Variables categóricas
    st.markdown("---")
    st.markdown('<div class="sec-title">📊 Tasas de Deserción por Variables Categóricas</div>',
                unsafe_allow_html=True)

    cat_map = [
        ("tiene_beca",              {0: "Sin beca",   1: "Con beca"}),
        ("trabaja",                 {0: "No trabaja", 1: "Trabaja"}),
        ("vive_fuera_de_quito",     {0: "En Quito",   1: "Fuera Quito"}),
        ("participa_extracurricular",{0: "No participa",1: "Participa"}),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for i, (col, lbl) in enumerate(cat_map):
        ax = axes[i]
        tasa = df_f.groupby(col)["deserto_semestre"].mean() * 100
        tasa.index = [lbl[k] for k in tasa.index]
        colors_cat = [C1 if v > deser_rate else C0 for v in tasa.values]
        bars = ax.bar(tasa.index, tasa.values, color=colors_cat, width=.5, edgecolor="white")
        ax.axhline(deser_rate, linestyle="--", color="gray", alpha=.6, linewidth=1.2)
        ax.set_title(col.replace("_", " "), fontweight="bold", fontsize=9)
        ax.set_ylim(0, min(tasa.max() * 1.35, 100))
        if i == 0: ax.set_ylabel("Tasa deserción (%)")
        for bar, v in zip(bars, tasa.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f"{v:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Tasa de Deserción por Variables Categóricas", fontsize=12, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    sin_beca_r = df_f[df_f["tiene_beca"] == 0]["deserto_semestre"].mean() * 100
    con_beca_r = df_f[df_f["tiene_beca"] == 1]["deserto_semestre"].mean() * 100
    st.markdown(
        f'<div class="danger">💡 <b>Factor protector de la beca:</b> '
        f'SIN BECA: <b>{sin_beca_r:.1f}%</b> de deserción | '
        f'CON BECA: <b>{con_beca_r:.1f}%</b> de deserción<br>'
        f'Diferencia: <b>{sin_beca_r - con_beca_r:.1f} puntos</b> de protección gracias a la beca.</div>',
        unsafe_allow_html=True,
    )

    # Scatter plots
    st.markdown("---")
    st.markdown('<div class="sec-title">🔍 Scatter Plots — Variables Clave</div>',
                unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        fig, ax = plt.subplots(figsize=(7, 5))
        for val, lbl, color, marker in [(0, "Persiste", C0, "o"), (1, "Deserta", C1, "^")]:
            sub = df_f[df_f["deserto_semestre"] == val]
            ax.scatter(sub["promedio_notas"], sub["asistencia_porcentaje"],
                       c=color, marker=marker, alpha=.4, s=25, label=lbl)
        ax.axvline(6.0, linestyle="--", color="gray", alpha=.7, linewidth=1.5, label="Umbral 6.0")
        ax.set_xlabel("Promedio de Notas"); ax.set_ylabel("Asistencia (%)")
        ax.set_title("Promedio vs Asistencia", fontweight="bold")
        ax.legend(fontsize=9); ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig); plt.close()
        st.markdown(
            '<div class="insight">💡 Los triángulos rojos (deserción) se concentran a la '
            'izquierda del umbral de 6.0 y con baja asistencia.</div>',
            unsafe_allow_html=True,
        )

    with col_s2:
        fig, ax = plt.subplots(figsize=(7, 5))
        for val, lbl, color, marker in [(0, "Persiste", C0, "o"), (1, "Deserta", C1, "^")]:
            sub = df_f[df_f["deserto_semestre"] == val]
            ax.scatter(sub["deuda_pendiente_usd"], sub["actividad_canvas_semanal"],
                       c=color, marker=marker, alpha=.4, s=25, label=lbl)
        ax.axvline(800, linestyle="--", color="gray", alpha=.7, linewidth=1.5, label="$800 umbral")
        ax.set_xlabel("Deuda Pendiente (USD)"); ax.set_ylabel("Actividad Canvas Semanal")
        ax.set_title("Deuda vs Actividad Canvas", fontweight="bold")
        ax.legend(fontsize=9); ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig); plt.close()
        st.markdown(
            '<div class="insight">💡 Nube de deserción en estudiantes con alta deuda y baja '
            'actividad en Canvas. La desconexión digital y financiera son predictores clave.</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CORRELACIONES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-title">🌡️ Heatmap de Correlaciones</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(14, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(
        corr_matrix, mask=mask, annot=True, fmt=".2f",
        cmap="RdYlGn", center=0, vmin=-1, vmax=1,
        square=True, linewidths=.5, ax=ax,
        annot_kws={"size": 8},
    )
    ax.set_title("Matriz de Correlaciones — Variables UISEK",
                 fontsize=13, fontweight="bold", pad=15)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    # Correlación con la variable objetivo
    col_h1, col_h2 = st.columns(2)
    pos_corrs = corr_target[corr_target > 0].sort_values(ascending=False)
    neg_corrs = corr_target[corr_target < 0].sort_values()

    with col_h1:
        st.markdown(
            '<div class="danger">💡 <b>Correlaciones POSITIVAS con deserción</b> '
            '(↑ variable → ↑ deserción):<br>' +
            "".join(f"· <b>{k}</b>: r=+{v:.3f}<br>" for k, v in pos_corrs.items()) +
            "</div>", unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="ok">💡 <b>Correlaciones NEGATIVAS con deserción</b> '
            '(↑ variable → ↓ deserción):<br>' +
            "".join(f"· <b>{k}</b>: r={v:.3f}<br>" for k, v in neg_corrs.items()) +
            "</div>", unsafe_allow_html=True,
        )

    with col_h2:
        fig, ax = plt.subplots(figsize=(7, 5))
        sorted_ct = corr_target.sort_values()
        colors_ct = [C1 if v > 0 else C0 for v in sorted_ct.values]
        ax.barh(sorted_ct.index, sorted_ct.values, color=colors_ct)
        ax.axvline(0, color="black", linewidth=.8)
        ax.set_xlabel("Correlación de Pearson (r)")
        ax.set_title("Correlación con Deserción", fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    r_trab_h = corr_matrix.loc["trabaja", "horas_trabajo_semanal"]
    r_beca_d = corr_matrix.loc["tiene_beca", "deuda_pendiente_usd"]
    st.markdown(
        f'<div class="warn">💡 <b>Multicolinealidad entre predictores:</b><br>'
        f'· trabaja × horas_trabajo_semanal: r=<b>{r_trab_h:.3f}</b> ← Alta correlación<br>'
        f'· tiene_beca × deuda_pendiente_usd: r=<b>{r_beca_d:.3f}</b> ← Alta correlación</div>',
        unsafe_allow_html=True,
    )

    # Pair plot (variables clave)
    st.markdown("---")
    st.markdown('<div class="sec-title">🔵 Pair Plot — Variables Clave</div>', unsafe_allow_html=True)

    sub_pair = df_f[COLS_CLAVE + ["deserto_semestre"]].sample(
        min(400, n), random_state=42
    ).copy()
    sub_pair["Grupo"] = sub_pair["deserto_semestre"].map({0: "Persiste", 1: "Deserta"})
    fig_pair = sns.pairplot(
        sub_pair.drop(columns=["deserto_semestre"]), hue="Grupo",
        palette={"Persiste": C0, "Deserta": C1},
        corner=True, plot_kws={"alpha": .35, "s": 15},
        diag_kind="kde",
    )
    fig_pair.figure.suptitle(
        "Pair Plot — Variables Clave (muestra 400 obs.)",
        fontsize=12, fontweight="bold", y=1.01,
    )
    handles = [
        mpatches.Patch(color=C0, label="Persiste"),
        mpatches.Patch(color=C1, label="Deserta"),
    ]
    fig_pair.figure.legend(handles=handles, loc="upper right", fontsize=10)
    st.pyplot(fig_pair.figure); plt.close("all")

    st.markdown(
        '<div class="insight">💡 En el cruce Promedio vs Deuda se observa un cluster de '
        'deserción (triángulos rojos) en zona de bajo promedio y alta deuda.<br>'
        'La diagonal (KDE) muestra que las distribuciones de desertores están desplazadas '
        'hacia la izquierda en notas y asistencia.</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PERFIL & RESUMEN EJECUTIVO
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-title">📋 Perfil Comparativo de Deserción — UISEK</div>',
                unsafe_allow_html=True)

    perfil = df_f.groupby("deserto_semestre")[COLS_CLAVE].mean().round(3)
    perfil.index = ["Estudiante Persistente (0)", "Estudiante en Riesgo (1)"]
    st.dataframe(perfil.T.style.format("{:.3f}"), use_container_width=True)

    nota_r  = g1["promedio_notas"].mean()
    nota_0  = g0["promedio_notas"].mean()
    asist_r = g1["asistencia_porcentaje"].mean()
    deuda_r = g1["deuda_pendiente_usd"].mean()
    deuda_0 = g0["deuda_pendiente_usd"].mean()
    mat_r   = g1["materias_reprobadas_acum"].mean()

    st.markdown(
        f'<div class="danger">💡 <b>RETRATO DEL ESTUDIANTE EN RIESGO UISEK:</b><br>'
        f'· <b>Rendimiento:</b> Promedio cercano a {nota_r:.1f} (vs {nota_0:.1f} del persistente).<br>'
        f'· <b>Asistencia:</b> Suele faltar más, con un {asist_r:.1f}% de asistencia.<br>'
        f'· <b>Financiero:</b> Carga una deuda promedio de ${deuda_r:,.2f}.<br>'
        f'· <b>Académico:</b> Tiene acumuladas {mat_r:.1f} materias reprobadas.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ok">🚀 <b>Estrategia Recomendada:</b> Priorizar intervención en '
        'estudiantes con <b>Deuda &gt; $800 Y Promedio &lt; 6.5</b>.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<div class="sec-title">🏆 Resumen Ejecutivo del EDA — UISEK Deserción</div>',
                unsafe_allow_html=True)

    r_deuda  = corr_target["deuda_pendiente_usd"]
    r_nota   = corr_target["promedio_notas"]
    r_beca   = corr_target["tiene_beca"]
    r_asist  = corr_target["asistencia_porcentaje"]
    r_trab_h = corr_matrix.loc["trabaja", "horas_trabajo_semanal"]
    sin_beca = df_f[df_f["tiene_beca"] == 0]["deserto_semestre"].mean() * 100
    con_beca = df_f[df_f["tiene_beca"] == 1]["deserto_semestre"].mean() * 100
    asist_0  = g0["asistencia_porcentaje"].mean()
    asist_1  = g1["asistencia_porcentaje"].mean()

    resumen = (
        f"═══════════════════════════════════════════════════════════════\n"
        f"  RESUMEN EJECUTIVO DEL EDA — Caso UISEK Deserción\n"
        f"  Dataset: {n:,} estudiantes filtrados | Tasa global: {deser_rate:.1f}%\n"
        f"═══════════════════════════════════════════════════════════════\n\n"
        f"HALLAZGO 1 — Predictor Principal (Financiero):\n"
        f"  La deuda_pendiente_usd es el factor crítico (r={r_deuda:+.3f}).\n"
        f"  Los desertores deben en promedio ${deuda_r:,.2f} vs ${deuda_0:,.2f} de persistentes.\n\n"
        f"HALLAZGO 2 — Desempeño Académico:\n"
        f"  El promedio_notas tiene una correlación negativa (r={r_nota:.3f}).\n"
        f"  Se identificó un umbral de riesgo visual por debajo de 6.5 puntos.\n\n"
        f"HALLAZGO 3 — El factor protector de la Beca:\n"
        f"  Tasa deserción SIN BECA: {sin_beca:.1f}% | CON BECA: {con_beca:.1f}%\n"
        f"  Diferencia: {sin_beca - con_beca:.1f} puntos de protección.\n\n"
        f"HALLAZGO 4 — Comportamiento y Asistencia:\n"
        f"  La asistencia cae de {asist_0:.1f}% a {asist_1:.1f}% en estudiantes desertores.\n"
        f"  Existe alta redundancia (r={r_trab_h:.2f}) entre 'trabaja' y 'horas_trabajo_semanal'.\n\n"
        f"IMPLICACIÓN PARA S9 (Modelado):\n"
        f"  1. Manejo de desbalance: La clase minoritaria (Deserción) es el {deser_rate:.1f}%.\n"
        f"  2. Reducción de variables: Eliminar 'trabaja', mantener 'horas_trabajo'.\n"
        f"  3. Feature Engineering: Variable de riesgo (Deuda > 800 & Nota < 6.5).\n"
        f"═══════════════════════════════════════════════════════════════"
    )
    st.code(resumen, language=None)

    # Gráfico de importancia por correlación absoluta
    st.markdown("---")
    st.markdown('<div class="sec-title">📊 Top Predictores por Correlación Absoluta</div>',
                unsafe_allow_html=True)

    corr_abs = corr_target.abs().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    colors_pred = [C1 if corr_target[col] > 0 else C0 for col in corr_abs.index]
    bars = ax.barh(corr_abs.index, corr_abs.values, color=colors_pred)
    ax.axvline(0, color="black", linewidth=.5)
    ax.set_xlabel("|Correlación de Pearson| con Deserción")
    ax.set_title("Importancia de Predictores (Correlación Absoluta con deserto_semestre)",
                 fontweight="bold")
    p0 = mpatches.Patch(color=C0, label="Correlación negativa (factor protector)")
    p1 = mpatches.Patch(color=C1, label="Correlación positiva (factor de riesgo)")
    ax.legend(handles=[p0, p1], fontsize=9)
    for bar, v in zip(bars, corr_abs.values):
        ax.text(v + .002, bar.get_y() + bar.get_height() / 2,
                f"{v:.3f}", va="center", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

st.markdown("---")
st.caption(
    "🎓 Dashboard generado con Streamlit · UISEK — Deserción Estudiantil · "
    "Ingeniería de Data Science"
)
