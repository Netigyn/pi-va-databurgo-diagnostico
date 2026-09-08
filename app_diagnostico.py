"""
Projeto Integrador V-A — PUC Goiás
Diagnóstico de Indicadores de Retenção e Relacionamento com Clientes
Organização parceira: Databurgo Brasil Tecnologia

Este aplicativo compara números agregados informados pelo usuário (MRR, clientes
ativos, cancelamentos, cross-sell, satisfação percebida) a benchmarks de mercado
carregados de benchmarks_mercado.csv. Não simula nem utiliza dados individuais de
clientes — trabalha apenas com totais agregados, conforme descrito no relatório
técnico (seção 5 — Descrição da Base de Dados).

Para rodar: streamlit run app_diagnostico.py
"""

import math
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Configuração da página
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Diagnóstico Databurgo — Retenção e Relacionamento",
    page_icon="📊",
    layout="wide",
)

BASE_DIR = Path(__file__).parent
BENCHMARKS_PATH = BASE_DIR / "benchmarks_mercado.csv"

COR_BOM = "#2E7D32"
COR_ATENCAO = "#F9A825"
COR_CRITICO = "#C62828"
COR_NEUTRO = "#5B7FA6"


@st.cache_data
def carregar_benchmarks() -> pd.DataFrame:
    return pd.read_csv(BENCHMARKS_PATH)


def faixa_do_indicador(df: pd.DataFrame, indicador: str) -> pd.DataFrame:
    return df[df["indicador"] == indicador].reset_index(drop=True)


def classificar_churn(valor: float) -> tuple[str, str]:
    """Classifica o churn mensal (%) e retorna (rótulo, cor)."""
    if valor < 3:
        return "Excelente — abaixo da faixa saudável de mercado", COR_BOM
    if valor <= 5:
        return "Dentro do esperado — faixa saudável de mercado (3% a 5%)", COR_BOM
    if valor <= 7:
        return "Atenção — acima da faixa saudável, dentro da média de mercado", COR_ATENCAO
    return "Crítico — bem acima do que o mercado considera saudável", COR_CRITICO


def classificar_cross_sell(valor: float) -> tuple[str, str]:
    if valor >= 40:
        return "Forte aproveitamento da base — acima da linha de base interna", COR_BOM
    if valor >= 20:
        return "Dentro da linha de base interna de referência (20% a 40%)", COR_ATENCAO
    return "Abaixo da linha de base interna — oportunidade de cross-sell", COR_CRITICO


def gauge_comparativo(valor: float, faixa_min: float, faixa_max: float, titulo: str, unidade: str, cor: str, eixo_max: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=valor,
            number={"suffix": f" {unidade}", "font": {"size": 34}},
            title={"text": titulo, "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, eixo_max]},
                "bar": {"color": cor},
                "steps": [
                    {"range": [faixa_min, faixa_max], "color": "#E8F5E9"},
                ],
                "threshold": {
                    "line": {"color": "#333333", "width": 3},
                    "thickness": 0.85,
                    "value": faixa_max,
                },
            },
        )
    )
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=10))
    return fig


# ----------------------------------------------------------------------------
# Cabeçalho / Data Storytelling — a pergunta antes da resposta
# ----------------------------------------------------------------------------
st.title("📊 Diagnóstico de Retenção e Relacionamento com Clientes")
st.caption("Databurgo Brasil Tecnologia — Projeto Integrador V-A | PUC Goiás")

st.markdown(
    """
> **A pergunta que motiva este diagnóstico:** comparada a outras pequenas empresas
> de tecnologia, a Databurgo está perdendo clientes rápido demais — ou está indo
> bem, só que sem saber disso?

Insira abaixo os números agregados do período que deseja avaliar. Nenhum dado
individual de cliente é solicitado ou armazenado — apenas totais da carteira.
"""
)

benchmarks = carregar_benchmarks()

st.divider()

# ----------------------------------------------------------------------------
# Entradas do usuário
# ----------------------------------------------------------------------------
st.subheader("1. Números agregados do período")

col1, col2, col3 = st.columns(3)
with col1:
    clientes_inicio = st.number_input("Clientes ativos no início do período", min_value=1, value=38, step=1)
    clientes_fim = st.number_input("Clientes ativos no fim do período", min_value=1, value=46, step=1)
with col2:
    cancelamentos = st.number_input("Cancelamentos no período", min_value=0, value=5, step=1)
    meses_periodo = st.number_input("Duração do período (meses)", min_value=1, value=6, step=1)
with col3:
    mrr = st.number_input("Receita Recorrente Mensal — MRR (R$)", min_value=0.0, value=19750.0, step=100.0, format="%.2f")
    clientes_cross_sell = st.number_input("Clientes com mais de um serviço contratado", min_value=0, value=14, step=1)

satisfacao = st.slider(
    "Satisfação percebida (autoavaliação — não é pesquisa formal com clientes), escala 0 a 10",
    min_value=0.0, max_value=10.0, value=8.7, step=0.1,
)
st.caption(
    "⚠️ Este número é uma percepção subjetiva de quem responde, não uma pesquisa "
    "de CSAT/NPS aplicada à carteira de clientes. É tratado aqui como referência "
    "qualitativa, nunca como evidência isolada de desempenho."
)

# ----------------------------------------------------------------------------
# Cálculos (seção 8 do relatório técnico)
# ----------------------------------------------------------------------------
churn_acumulado = cancelamentos / clientes_inicio if clientes_inicio else 0
# conversão do churn acumulado no período para uma taxa mensal equivalente
if churn_acumulado < 1:
    churn_mensal = 1 - (1 - churn_acumulado) ** (1 / meses_periodo)
else:
    churn_mensal = 1.0
churn_mensal_pct = churn_mensal * 100

ticket_medio = mrr / clientes_fim if clientes_fim else 0
cross_sell_pct = (clientes_cross_sell / clientes_fim * 100) if clientes_fim else 0

st.divider()

# ----------------------------------------------------------------------------
# Painel geral (big numbers) — visão geral antes do detalhamento
# ----------------------------------------------------------------------------
st.subheader("2. Panorama geral da carteira")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Clientes ativos (fim do período)", f"{clientes_fim}", delta=f"{clientes_fim - clientes_inicio:+d} no período")
m2.metric("MRR", f"R$ {mrr:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
m3.metric("Ticket médio por cliente", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
m4.metric("Cross-sell", f"{cross_sell_pct:.1f}%")

st.caption(
    "Volume de clientes, isoladamente, não indica desempenho — uma base que cresce "
    "também pode estar perdendo clientes rápido, se o churn for alto. Por isso o "
    "indicador central deste diagnóstico é o churn mensal, na seção seguinte."
)

st.divider()

# ----------------------------------------------------------------------------
# Indicador central: Churn mensal vs benchmark
# ----------------------------------------------------------------------------
st.subheader("3. Indicador central — Churn mensal vs. benchmark de mercado")

churn_bench = faixa_do_indicador(benchmarks, "Churn mensal")
faixa_saudavel = churn_bench[churn_bench["classificacao_faixa"] == "saudavel"].iloc[0]

label_churn, cor_churn = classificar_churn(churn_mensal_pct)

colA, colB = st.columns([1, 1.3])
with colA:
    st.plotly_chart(
        gauge_comparativo(
            churn_mensal_pct,
            faixa_saudavel["valor_min"],
            faixa_saudavel["valor_max"],
            "Churn mensal equivalente (%)",
            "%",
            cor_churn,
            eixo_max=max(10.0, churn_mensal_pct * 1.3),
        ),
        use_container_width=True,
    )
with colB:
    st.markdown(f"**Leitura:** <span style='color:{cor_churn}'>{label_churn}</span>", unsafe_allow_html=True)
    st.markdown(
        f"- Churn acumulado no período informado: **{churn_acumulado*100:.2f}%** "
        f"em {int(meses_periodo)} meses\n"
        f"- Churn mensal equivalente: **{churn_mensal_pct:.2f}% ao mês**\n"
        f"- Faixa de mercado considerada saudável: **"
        f"{faixa_saudavel['valor_min']:.1f}% a {faixa_saudavel['valor_max']:.1f}% ao mês** "
        f"(fonte: {faixa_saudavel['fonte']})"
    )

st.divider()

# ----------------------------------------------------------------------------
# Indicadores complementares: Cross-sell e Satisfação
# ----------------------------------------------------------------------------
st.subheader("4. Indicadores complementares — relacionamento e percepção")

col_cs, col_sat = st.columns(2)

with col_cs:
    label_cs, cor_cs = classificar_cross_sell(cross_sell_pct)
    cs_bench = faixa_do_indicador(benchmarks, "Cross-sell").iloc[0]
    st.plotly_chart(
        gauge_comparativo(
            cross_sell_pct, cs_bench["valor_min"], cs_bench["valor_max"],
            "Cross-sell (%)", "%", cor_cs, eixo_max=100,
        ),
        use_container_width=True,
    )
    st.markdown(f"**Leitura:** <span style='color:{cor_cs}'>{label_cs}</span>", unsafe_allow_html=True)
    st.caption(f"Sem benchmark público consolidado para o segmento — faixa usada como linha de base interna ({cs_bench['fonte']}).")

with col_sat:
    sat_bench = faixa_do_indicador(benchmarks, "Satisfacao percebida (CSAT 0-10)").iloc[0]
    st.plotly_chart(
        gauge_comparativo(
            satisfacao, sat_bench["valor_min"], sat_bench["valor_max"],
            "Satisfação percebida (0–10)", "", COR_NEUTRO, eixo_max=10,
        ),
        use_container_width=True,
    )
    st.markdown(
        "**Leitura:** indicador qualitativo — tratado apenas como referência de "
        "contexto, não como evidência objetiva de desempenho."
    )
    st.caption(f"Metodologia não comparável a NPS de mercado ({sat_bench['fonte']}).")

st.divider()

# ----------------------------------------------------------------------------
# Conclusão da narrativa
# ----------------------------------------------------------------------------
st.subheader("5. Conclusão do diagnóstico")

if churn_mensal_pct <= 5:
    st.success(
        f"Com os números informados, a retenção de clientes está **dentro ou melhor "
        f"do que a faixa que o mercado considera saudável** ({faixa_saudavel['valor_min']:.0f}% "
        f"a {faixa_saudavel['valor_max']:.0f}% ao mês). O crescimento de "
        f"{clientes_inicio} para {clientes_fim} clientes é uma boa notícia justamente "
        f"porque vem acompanhado de um churn controlado — não seria o caso se o "
        f"churn estivesse acima da faixa saudável."
    )
else:
    st.warning(
        "Com os números informados, o churn mensal equivalente está **acima da faixa "
        "que o mercado considera saudável**. Recomenda-se investigar as causas dos "
        "cancelamentos antes de comemorar o crescimento bruto da base de clientes."
    )

st.caption(
    "Ferramenta reutilizável: atualize os campos acima a cada novo período para "
    "repetir este diagnóstico, sem depender de nova análise externa."
)
