# Diagnóstico de Retenção e Relacionamento com Clientes — Databurgo

Projeto Integrador V-A — PUC Goiás (Big Data e Inteligência Artificial)
Aluno: Giancarlo Neves da Cruz | Matrícula: 2025 2.0792.0007-3
Professor: Thalles Bruno Gonçalves Nery dos Santos
Organização parceira: Databurgo Brasil Tecnologia

## Acesse o dashboard online

🔗 **https://databurgo-diagnostico.streamlit.app**

Não precisa instalar nada — abra o link acima direto no navegador. Se preferir
rodar localmente (ou o link estiver fora do ar), veja a seção "Como rodar o
dashboard" mais abaixo.

> ⚠️ **Nota:** por ser hospedado no plano gratuito do Streamlit Community
> Cloud, o app "adormece" automaticamente após um período sem acessos. Se a
> tela mostrar "Zzzz — This app has gone to sleep due to inactivity", basta
> clicar em **"Yes, get this app back up!"** — em cerca de 20 a 30 segundos
> ele volta a funcionar normalmente, com os mesmos dados. Não é um erro do
> projeto, apenas o comportamento padrão do serviço gratuito.

Repositório no GitHub: https://github.com/Netigyn/pi-va-databurgo-diagnostico

## O que este projeto é

Uma ferramenta interativa (Streamlit) que compara números agregados de uma
pequena empresa de serviços de tecnologia — clientes ativos, cancelamentos,
receita recorrente (MRR) e contratos múltiplos — a benchmarks de mercado,
apoiando decisões sobre retenção e relacionamento com clientes.

**Não** utiliza nem simula dados individuais de clientes. Todos os cálculos
partem de totais agregados informados diretamente pela organização parceira,
conforme descrito na seção 5 do relatório técnico.

## Contexto

A Databurgo é uma pequena empresa de desenvolvimento de sites e soluções
digitais que, como a maioria dos negócios desse porte, acompanha o
relacionamento com clientes de forma intuitiva, sem métricas objetivas ou
comparação com padrões de mercado. Este projeto transforma os números que a
empresa já possui em um diagnóstico objetivo, comparável e reutilizável a
cada novo período.

Todo o raciocínio, a justificativa dos indicadores e a metodologia estão
detalhados em `relatorio_tecnico_databurgo.pdf`.

## Estrutura do repositório

```
PI-VA_Databurgo_CustomerAnalytics/
├── README.md                          este arquivo
├── relatorio_tecnico_databurgo.pdf    relatório técnico completo (entregável 3.1)
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

**Opção 1 — Online (recomendado):** acesse
https://databurgo-diagnostico.streamlit.app direto no navegador, sem instalar
nada. Se o app estiver "dormindo" por inatividade, veja a nota no topo deste
documento sobre como reativá-lo.

**Opção 2 — Localmente:** pré-requisitos: Python 3.9+ instalado.

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

Detalhes completos em `relatorio_tecnico_databurgo.pdf`, seção 12.
