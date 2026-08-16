import json
from pathlib import Path

import pandas as pd
import streamlit as st


RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_JSON = RAIZ / "output" / "resumo.json"


st.set_page_config(
    page_title="Dashboard de Atendimentos",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def carregar_dados() -> dict:
    """Carrega os indicadores gerados pelo pipeline."""

    if not CAMINHO_JSON.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {CAMINHO_JSON}"
        )

    with CAMINHO_JSON.open(
        "r",
        encoding="utf-8",
    ) as arquivo:
        return json.load(arquivo)


st.title("📊 Sistema de Análise de Atendimentos")
st.caption("Dashboard baseado nos resultados do pipeline de processamento.")


try:
    dados = carregar_dados()

except FileNotFoundError as erro:
    st.error(str(erro))
    st.info(
        "Execute primeiro: python -m src.main"
    )
    st.stop()


resumo = dados["resumo"]
indicadores = dados["indicadores"]
distribuicao = dados["distribuicao"]
qualidade = dados["qualidade_dados"]


# =========================================================
# Indicadores principais
# =========================================================

st.subheader("Indicadores principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Atendimentos",
        resumo["total_processado"],
    )

with col2:
    st.metric(
        "Resolvidos",
        distribuicao["por_status"].get(
            "Resolvido",
            0,
        ),
    )

with col3:
    st.metric(
        "Pendentes",
        distribuicao["por_status"].get(
            "Pendente",
            0,
        ),
    )

with col4:
    st.metric(
        "Em andamento",
        distribuicao["por_status"].get(
            "Em Andamento",
            0,
        ),
    )


st.divider()


# =========================================================
# Indicadores de desempenho
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Tempo médio",
        f"{indicadores['tempo_medio_atendimento']:.2f} min",
    )

with col2:
    st.metric(
        "Categoria mais frequente",
        indicadores["categoria_mais_frequente"],
    )

with col3:
    st.metric(
        "Duplicidades removidas",
        resumo["duplicidades_removidas"],
    )


st.divider()


# =========================================================
# Gráficos
# =========================================================

st.subheader("Distribuição dos atendimentos")

col1, col2 = st.columns(2)

with col1:
    st.write("### Por categoria")

    categorias = pd.DataFrame(
        {
            "Categoria": list(
                distribuicao["por_categoria"].keys()
            ),
            "Quantidade": list(
                distribuicao["por_categoria"].values()
            ),
        }
    )

    st.bar_chart(
        categorias.set_index("Categoria")
    )


with col2:
    st.write("### Por status")

    status = pd.DataFrame(
        {
            "Status": list(
                distribuicao["por_status"].keys()
            ),
            "Quantidade": list(
                distribuicao["por_status"].values()
            ),
        }
    )

    st.bar_chart(
        status.set_index("Status")
    )


st.divider()


# =========================================================
# Qualidade dos dados
# =========================================================

st.subheader("⚠️ Qualidade dos dados")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Registros incompletos",
        qualidade["registros_incompletos"],
    )

with col2:
    st.metric(
        "Percentual de incompletos",
        f"{qualidade['percentual_incompletos']:.2f}%",
    )


if qualidade.get("registros_com_problemas", 0) > 0:

    st.write("### Registros com problemas")

    detalhes = qualidade.get(
        "detalhes_problemas",
        [],
    )

    if detalhes:
        problemas = []

        for item in detalhes:
            problemas.append(
                {
                    "Protocolo": item["protocolo"],
                    "Problemas": ", ".join(
                        item["problemas"]
                    ),
                }
            )

        st.dataframe(
            pd.DataFrame(problemas),
            use_container_width=True,
            hide_index=True,
        )

    st.metric(
        "Registros com problemas",
        qualidade["registros_com_problemas"],
    )

    st.metric(
        "Percentual com problemas",
        f"{qualidade['percentual_com_problemas']:.2f}%",
    )


st.divider()

st.caption(
    "Dados atualizados a partir de output/resumo.json."
)