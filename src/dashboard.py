import json
from pathlib import Path

import pandas as pd
import streamlit as st


RAIZ = Path(__file__).resolve().parent.parent

CAMINHO_JSON = RAIZ / "output" / "resumo.json"
CAMINHO_CSV = RAIZ / "output" / "atendimentos_processados.csv"


# =========================================================
# Configuração da página
# =========================================================

st.set_page_config(
    page_title="Dashboard de Atendimentos",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# Carregamento dos dados
# =========================================================

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


@st.cache_data
def carregar_atendimentos() -> pd.DataFrame:
    """Carrega os atendimentos processados."""

    if not CAMINHO_CSV.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {CAMINHO_CSV}"
        )

    return pd.read_csv(
        CAMINHO_CSV,
        encoding="utf-8",
    )


# =========================================================
# Título
# =========================================================

st.title("📊 Sistema de Análise de Atendimentos")

st.caption(
    "Dashboard baseado nos resultados do pipeline de processamento."
)


# =========================================================
# Carregar informações
# =========================================================

try:
    dados = carregar_dados()
    df = carregar_atendimentos()

except FileNotFoundError as erro:
    st.error(str(erro))
    st.info("Execute primeiro: python -m src.main")
    st.stop()


resumo = dados["resumo"]
indicadores = dados["indicadores"]
distribuicao = dados["distribuicao"]
qualidade = dados["qualidade_dados"]


# =========================================================
# Atualização dos dados
# =========================================================

if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()


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
        distribuicao["por_status"].get("Resolvido", 0),
    )

with col3:
    st.metric(
        "Pendentes",
        distribuicao["por_status"].get("Pendente", 0),
    )

with col4:
    st.metric(
        "Em andamento",
        distribuicao["por_status"].get("Em Andamento", 0),
    )


st.divider()


# =========================================================
# Indicadores de desempenho
# =========================================================

st.subheader("Indicadores de desempenho")

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
# Filtros
# =========================================================

st.subheader("🔎 Filtros")

col1, col2 = st.columns(2)

categorias_disponiveis = sorted(
    df["categoria"].dropna().unique().tolist()
)

status_disponiveis = sorted(
    df["status"].dropna().unique().tolist()
)

with col1:
    categorias_selecionadas = st.multiselect(
        "Filtrar por categoria",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
    )

with col2:
    status_selecionados = st.multiselect(
        "Filtrar por status",
        options=status_disponiveis,
        default=status_disponiveis,
    )


df_filtrado = df[
    df["categoria"].isin(categorias_selecionadas)
    & df["status"].isin(status_selecionados)
].copy()


# =========================================================
# Resultado dos filtros
# =========================================================

st.write(
    f"**Registros encontrados:** {len(df_filtrado)}"
)


# =========================================================
# Exportação dos dados filtrados
# =========================================================

st.subheader("📥 Exportação")

if df_filtrado.empty:

    st.info(
        "Selecione pelo menos uma categoria e um status "
        "para exportar os registros."
    )

else:

    dados_csv = df_filtrado.to_csv(
        index=False,
        encoding="utf-8-sig",
    )

    st.download_button(
        label="📥 Baixar atendimentos filtrados",
        data=dados_csv,
        file_name="atendimentos_filtrados.csv",
        mime="text/csv",
        width="stretch",
    )


st.divider()


# =========================================================
# Tabela de atendimentos
# =========================================================

st.subheader("📋 Atendimentos")

if df_filtrado.empty:

    st.warning(
        "Nenhum atendimento encontrado com os filtros selecionados."
    )

else:

    colunas_exibicao = [
        "protocolo",
        "nome",
        "email",
        "categoria",
        "data",
        "tempo_atendimento",
        "status",
    ]

    st.dataframe(
        df_filtrado[colunas_exibicao],
        width="stretch",
        hide_index=True,
    )


st.divider()


# =========================================================
# Gráficos
# =========================================================

st.subheader("📈 Distribuição dos atendimentos")

col1, col2 = st.columns(2)


with col1:

    st.write("### Por categoria")

    if df_filtrado.empty:

        st.info("Não há dados para exibir.")

    else:

        categorias = (
            df_filtrado["categoria"]
            .value_counts()
            .rename_axis("Categoria")
            .to_frame("Quantidade")
        )

        st.bar_chart(categorias)


with col2:

    st.write("### Por status")

    if df_filtrado.empty:

        st.info("Não há dados para exibir.")

    else:

        status = (
            df_filtrado["status"]
            .value_counts()
            .rename_axis("Status")
            .to_frame("Quantidade")
        )

        st.bar_chart(status)


st.divider()


# =========================================================
# Qualidade dos dados
# =========================================================

st.subheader("⚠️ Qualidade dos dados")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Registros incompletos",
        qualidade["registros_incompletos"],
    )

with col2:

    st.metric(
        "Percentual incompleto",
        f"{qualidade['percentual_incompletos']:.2f}%",
    )

with col3:

    st.metric(
        "Registros com problemas",
        qualidade.get("registros_com_problemas", 0),
    )

with col4:

    st.metric(
        "Percentual com problemas",
        f"{qualidade.get('percentual_com_problemas', 0):.2f}%",
    )


# =========================================================
# Detalhes dos problemas
# =========================================================

detalhes = qualidade.get(
    "detalhes_problemas",
    [],
)

if detalhes:

    st.write("### Registros com problemas")

    problemas = []

    for item in detalhes:

        problemas.append(
            {
                "Protocolo": item["protocolo"],
                "Problemas": ", ".join(item["problemas"]),
            }
        )

    st.dataframe(
        pd.DataFrame(problemas),
        width="stretch",
        hide_index=True,
    )


# =========================================================
# Informações do processamento
# =========================================================

st.divider()

st.subheader("ℹ️ Informações do processamento")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Registros originais",
        resumo["total_original"],
    )

with col2:

    st.metric(
        "Registros processados",
        resumo["total_processado"],
    )

with col3:

    st.metric(
        "Duplicidades removidas",
        resumo["duplicidades_removidas"],
    )


# =========================================================
# Rodapé
# =========================================================

st.caption(
    "Dados carregados de output/resumo.json e "
    "output/atendimentos_processados.csv."
)