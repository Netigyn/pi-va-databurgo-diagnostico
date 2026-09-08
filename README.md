# Diagnóstico de Retenção e Relacionamento com Clientes — Databurgo

Projeto Integrador V-A — PUC Goiás (Big Data e Inteligência Artificial)
Aluno: Giancarlo Neves da Cruz | Matrícula: 2025 2.0792.0007-3
Professor: Thalles Bruno Gonçalves Nery dos Santos
Organização parceira: Databurgo Brasil Tecnologia

## O que este projeto é

Uma ferramenta interativa (Streamlit) que compara números agregados de uma
pequena empresa de serviços de tecnologia — clientes ativos, cancelamentos,
receita recorrente (MRR) e contratos múltiplos — a benchmarks de mercado,
apoiando decisões sobre retenção e relacionamento com clientes.



## Contexto

A Databurgo é uma pequena empresa de desenvolvimento de sites e soluções
digitais que, como a maioria dos negócios desse porte, acompanha o
relacionamento com clientes de forma intuitiva, sem métricas objetivas ou
comparação com padrões de mercado. Este projeto transforma os números que a
empresa já possui em um diagnóstico objetivo, comparável e reutilizável a
cada novo período.

Todo o raciocínio, a justificativa dos indicadores e a metodologia estão
detalhados em `relatorio_tecnico_databurgo.docx`.

## Estrutura do repositório

```
PI-VA_Databurgo_CustomerAnalytics/
├── README.md                          este arquivo
├── relatorio_tecnico_databurgo.docx   relatório técnico completo (entregável 3.1)
├── app_diagnostico.py                 dashboard interativo em Streamlit (entregável 3.2 e 3.3)
├── benchmarks_mercado.csv             base de benchmarks de mercado, com fontes citadas
└── fa3e6eed-...pdf                    proposta oficial do Projeto Integrador V-A (enunciado)
```

## Indicadores (KPIs)

| KPI | Perspectiva | O que mede |
|---|---|---|
| Churn mensal (equivalente) | Cliente / Retenção | % da base que cancela contratos por mês |
| MRR e ticket médio por cliente | Financeira | Receita recorrente e sua distribuição pela base |
| Taxa de cross-sell | Relacionamento / Processos internos | % de clientes com mais de um serviço contratado |
| Satisfação percebida | Cliente (qualitativo) | Autoavaliação do fundador — tratada com ressalva, não é pesquisa formal |

A justificativa completa de cada indicador está na seção 6 do relatório técnico.

## Como rodar o dashboard

Pré-requisitos: Python 3.9+ instalado.

```bash
pip install streamlit plotly pandas
streamlit run app_diagnostico.py
```

O app abre no navegador em `http://localhost:8501`. Os campos de entrada
(clientes, cancelamentos, MRR, cross-sell, satisfação) já vêm preenchidos
com os números reais da Databurgo referentes ao período de março a agosto
de 2026, mas podem ser editados livremente — a ferramenta foi desenhada
para ser reutilizada em qualquer período futuro, ou até por outra pequena
empresa de perfil semelhante.

## Fontes dos benchmarks

As faixas de mercado usadas em `benchmarks_mercado.csv` estão documentadas
com fonte em cada linha do próprio arquivo, e também na seção de
Referências do relatório técnico.

## Limitações conhecidas

- Os dados cobrem uma única empresa parceira e uma janela de 6 meses.
- O indicador de satisfação é uma autoavaliação do fundador da Databurgo,
  não uma pesquisa formal aplicada aos clientes finais.
- Não há benchmark público consolidado de cross-sell específico para o
  segmento de pequenas empresas de desenvolvimento web; a faixa usada no
  app é uma linha de base interna, não uma comparação externa rígida.

Detalhes completos em `relatorio_tecnico_databurgo.docx`, seção 12.
