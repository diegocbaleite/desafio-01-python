import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# =========================================================
# Configuração dos caminhos
# =========================================================

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
# Funções de carregamento
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
# Funções auxiliares
# =========================================================

def calcular_indicadores_filtrados(
    df: pd.DataFrame,
) -> dict:
    """Calcula indicadores usando apenas os dados filtrados."""

    total = len(df)

    resolvidos = int(
        (df["status"] == "Resolvido").sum()
    )

    pendentes = int(
        (df["status"] == "Pendente").sum()
    )

    em_andamento = int(
        (df["status"] == "Em Andamento").sum()
    )

    tempos = pd.to_numeric(
        df["tempo_atendimento"],
        errors="coerce",
    ).dropna()

    if tempos.empty:

        tempo_medio = 0.0
        tempo_mediano = 0.0
        tempo_minimo = 0.0
        tempo_maximo = 0.0

    else:

        tempo_medio = float(tempos.mean())
        tempo_mediano = float(tempos.median())
        tempo_minimo = float(tempos.min())
        tempo_maximo = float(tempos.max())

    if total > 0:

        categorias = (
            df["categoria"]
            .value_counts()
        )

        if not categorias.empty:
            categoria_mais_frequente = categorias.index[0]
        else:
            categoria_mais_frequente = "N/A"

    else:

        categoria_mais_frequente = "N/A"

    return {
        "total": total,
        "resolvidos": resolvidos,
        "pendentes": pendentes,
        "em_andamento": em_andamento,
        "tempo_medio": tempo_medio,
        "tempo_mediano": tempo_mediano,
        "tempo_minimo": tempo_minimo,
        "tempo_maximo": tempo_maximo,
        "categoria_mais_frequente": (
            categoria_mais_frequente
        ),
    }


# =========================================================
# Título
# =========================================================

st.title(
    "📊 Sistema de Análise de Atendimentos"
)

st.caption(
    "Dashboard interativo baseado nos resultados "
    "do pipeline de processamento."
)


# =========================================================
# Carregamento dos dados
# =========================================================

try:

    dados = carregar_dados()

    df = carregar_atendimentos()

except FileNotFoundError as erro:

    st.error(str(erro))

    st.info(
        "Execute primeiro: python -m src.main"
    )

    st.stop()


# =========================================================
# Organização dos dados
# =========================================================

resumo = dados["resumo"]

indicadores = dados["indicadores"]

distribuicao = dados["distribuicao"]

qualidade = dados["qualidade_dados"]


# =========================================================
# Preparação do DataFrame
# =========================================================

df["data"] = pd.to_datetime(
    df["data"],
    errors="coerce",
)

df["tempo_atendimento"] = pd.to_numeric(
    df["tempo_atendimento"],
    errors="coerce",
)


# =========================================================
# Atualização dos dados
# =========================================================

if st.button("🔄 Atualizar dados"):

    st.cache_data.clear()

    st.rerun()


# =========================================================
# Filtros
# =========================================================

st.subheader("🔎 Filtros")


categorias_disponiveis = sorted(
    df["categoria"]
    .dropna()
    .unique()
    .tolist()
)

status_disponiveis = sorted(
    df["status"]
    .dropna()
    .unique()
    .tolist()
)


col1, col2 = st.columns(2)


with col1:

    categorias_selecionadas = st.multiselect(
        "📂 Filtrar por categoria",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
    )


with col2:

    status_selecionados = st.multiselect(
        "📌 Filtrar por status",
        options=status_disponiveis,
        default=status_disponiveis,
    )


# =========================================================
# Filtro de período
# =========================================================

col3, col4 = st.columns(2)


data_minima = df["data"].min()
data_maxima = df["data"].max()


with col3:

    if pd.notna(data_minima) and pd.notna(data_maxima):

        periodo = st.date_input(
            "📅 Período",
            value=(
                data_minima.date(),
                data_maxima.date(),
            ),
        )

    else:

        periodo = None


# =========================================================
# Busca
# =========================================================

with col4:

    busca = st.text_input(
        "🔍 Buscar por protocolo ou nome",
        placeholder="Digite o protocolo ou nome...",
    )


# =========================================================
# Botão limpar filtros
# =========================================================

if st.button("🧹 Limpar filtros"):

    st.rerun()


# =========================================================
# Aplicação dos filtros
# =========================================================

df_filtrado = df.copy()


# ---------------------------------------------------------
# Categoria
# ---------------------------------------------------------

df_filtrado = df_filtrado[
    df_filtrado["categoria"].isin(
        categorias_selecionadas
    )
]


# ---------------------------------------------------------
# Status
# ---------------------------------------------------------

df_filtrado = df_filtrado[
    df_filtrado["status"].isin(
        status_selecionados
    )
]


# ---------------------------------------------------------
# Período
# ---------------------------------------------------------

if periodo and len(periodo) == 2:

    data_inicio, data_fim = periodo

    df_filtrado = df_filtrado[
        (
            df_filtrado["data"].dt.date
            >= data_inicio
        )
        &
        (
            df_filtrado["data"].dt.date
            <= data_fim
        )
    ]


# ---------------------------------------------------------
# Busca
# ---------------------------------------------------------

if busca.strip():

    termo = busca.strip().lower()

    filtro_busca = (
        df_filtrado["protocolo"]
        .astype(str)
        .str.lower()
        .str.contains(
            termo,
            na=False,
        )
        |
        df_filtrado["nome"]
        .astype(str)
        .str.lower()
        .str.contains(
            termo,
            na=False,
        )
    )

    df_filtrado = df_filtrado[
        filtro_busca
    ]


# =========================================================
# Indicadores filtrados
# =========================================================

indicadores_filtrados = (
    calcular_indicadores_filtrados(
        df_filtrado
    )
)


# =========================================================
# Resultado dos filtros
# =========================================================

st.info(
    f"📌 Registros encontrados: "
    f"{len(df_filtrado)} de {len(df)}"
)


st.divider()


# =========================================================
# Indicadores principais
# =========================================================

st.subheader(
    "📊 Indicadores principais"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Atendimentos",
        indicadores_filtrados["total"],
    )


with col2:

    st.metric(
        "Resolvidos",
        indicadores_filtrados["resolvidos"],
    )


with col3:

    st.metric(
        "Pendentes",
        indicadores_filtrados["pendentes"],
    )


with col4:

    st.metric(
        "Em andamento",
        indicadores_filtrados[
            "em_andamento"
        ],
    )


st.divider()


# =========================================================
# Indicadores de desempenho
# =========================================================

st.subheader(
    "⏱️ Indicadores de desempenho"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Tempo médio",
        (
            f"{indicadores_filtrados['tempo_medio']:.2f}"
            " min"
        ),
    )


with col2:

    st.metric(
        "Tempo mediano",
        (
            f"{indicadores_filtrados['tempo_mediano']:.2f}"
            " min"
        ),
    )


with col3:

    st.metric(
        "Tempo mínimo",
        (
            f"{indicadores_filtrados['tempo_minimo']:.2f}"
            " min"
        ),
    )


with col4:

    st.metric(
        "Tempo máximo",
        (
            f"{indicadores_filtrados['tempo_maximo']:.2f}"
            " min"
        ),
    )


st.divider()


# =========================================================
# Outros indicadores
# =========================================================

st.subheader(
    "📌 Outros indicadores"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Categoria mais frequente",
        indicadores_filtrados[
            "categoria_mais_frequente"
        ],
    )


with col2:

    st.metric(
        "Duplicidades removidas",
        resumo["duplicidades_removidas"],
    )


st.divider()


# =========================================================
# Exportação
# =========================================================

st.subheader(
    "📥 Exportação"
)


if df_filtrado.empty:

    st.info(
        "Não existem registros para exportar."
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

st.subheader(
    "📋 Atendimentos"
)


if df_filtrado.empty:

    st.warning(
        "Nenhum atendimento encontrado "
        "com os filtros selecionados."
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

    tabela = df_filtrado[
        colunas_exibicao
    ].copy()

    tabela["data"] = tabela[
        "data"
    ].dt.strftime("%d/%m/%Y")

    st.dataframe(
        tabela,
        width="stretch",
        hide_index=True,
    )


st.divider()


# =========================================================
# Visualização
# =========================================================

st.subheader(
    "📈 Visualização dos atendimentos"
)


col1, col2 = st.columns(2)


# =========================================================
# Gráfico por categoria
# =========================================================

with col1:

    st.write(
        "### Por categoria"
    )

    if df_filtrado.empty:

        st.info(
            "Não há dados para exibir."
        )

    else:

        categorias = (
            df_filtrado["categoria"]
            .value_counts()
        )

        st.bar_chart(
            categorias
        )


# =========================================================
# Gráfico por status
# =========================================================

with col2:

    st.write(
        "### Por status"
    )

    if df_filtrado.empty:

        st.info(
            "Não há dados para exibir."
        )

    else:

        status = (
            df_filtrado["status"]
            .value_counts()
        )

        st.bar_chart(
            status
        )


# =========================================================
# Distribuição dos tempos
# =========================================================

st.write(
    "### ⏱️ Distribuição dos tempos "
    "de atendimento"
)


if df_filtrado.empty:

    st.info(
        "Não há dados para exibir."
    )

else:

    tempos = (
        pd.to_numeric(
            df_filtrado["tempo_atendimento"],
            errors="coerce",
        )
        .dropna()
    )

    if tempos.empty:

        st.info(
            "Não existem tempos válidos "
            "para exibir."
        )

    else:

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.hist(
            tempos,
            bins=6,
        )

        ax.set_title(
            "Distribuição dos tempos "
            "de atendimento"
        )

        ax.set_xlabel(
            "Tempo de atendimento "
            "(minutos)"
        )

        ax.set_ylabel(
            "Quantidade de atendimentos"
        )

        ax.grid(
            axis="y",
            alpha=0.3,
        )

        st.pyplot(
            fig,
            clear_figure=True,
        )

        plt.close(fig)


st.divider()


# =========================================================
# Qualidade dos dados
# =========================================================

st.subheader(
    "⚠️ Qualidade dos dados"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Registros incompletos",
        qualidade[
            "registros_incompletos"
        ],
    )


with col2:

    st.metric(
        "Percentual incompleto",
        (
            f"{qualidade['percentual_incompletos']:.2f}%"
        ),
    )


with col3:

    st.metric(
        "Registros com problemas",
        qualidade.get(
            "registros_com_problemas",
            0,
        ),
    )


with col4:

    st.metric(
        "Percentual com problemas",
        (
            f"{qualidade.get(
                'percentual_com_problemas',
                0,
            ):.2f}%"
        ),
    )


# =========================================================
# Detalhes dos problemas
# =========================================================

detalhes = qualidade.get(
    "detalhes_problemas",
    [],
)


if detalhes:

    st.write(
        "### Registros com problemas"
    )

    problemas = []

    for item in detalhes:

        problemas.append(
            {
                "Protocolo": item[
                    "protocolo"
                ],
                "Problemas": ", ".join(
                    item["problemas"]
                ),
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

st.subheader(
    "ℹ️ Informações do processamento"
)


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
    "Dados carregados de "
    "output/resumo.json e "
    "output/atendimentos_processados.csv."
)