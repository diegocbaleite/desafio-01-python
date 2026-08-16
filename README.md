# 📊 Sistema de Análise de Atendimentos

Sistema desenvolvido em Python para leitura, limpeza, validação, tratamento e análise de dados de atendimentos de suporte técnico de alunos.

O projeto recebe dados provenientes de arquivos CSV, JSON e TXT, realiza limpeza e padronização dos registros, valida a qualidade dos dados, calcula indicadores estatísticos com Pandas e NumPy, gera relatórios, exporta gráficos em formato PNG e disponibiliza um dashboard interativo em Streamlit.

---

## 👨‍💻 Identificação

**Alunos:**
- Diego Assunção Leite
- Leonardo de Oliveira Ramos

**Curso/Módulo:** FIC_DEV — Módulo Python para IA (Aulas 01 a 10)  
**Instituição:** SECITECI / Escola Técnica Estadual de Cuiabá  
**Turma:** Vespertino  

---

## 🎯 Objetivo

Desenvolver uma aplicação modular em linha de comando (CLI) em Python capaz de:

- Ler configurações dinâmicas de caminhos e parâmetros a partir do `config.json`;
- Suportar a leitura de arquivos em formato CSV (com delimitador configurável), JSON e TXT;
- Classificar registros como válidos ou inválidos, registrando motivos de rejeição em log de auditoria;
- Realizar limpeza de texto (remoção de espaços desnecessários e padronização de caixa);
- Padronizar categorias de atendimento utilizando dicionário de sinônimos/palavras-chave;
- Converter múltiplos formatos de data para o padrão ISO (`YYYY-MM-DD`);
- Tratar e filtrar tempos de atendimento (intervalo permitido de 0 a 480 minutos);
- Remover registros duplicados com base no identificador/protocolo;
- Extrair protocolos, telefones e e-mails de arquivos de observações em TXT usando expressões regulares (Regex);
- Calcular métricas estatísticas utilizando **Pandas** e **NumPy** (total de chamados, distribuições por categoria e status, tempo médio, mediano, min/max e tempo médio normalizado);
- Gerar visualizações em formato PNG com **Matplotlib** (`atendimentos_por_categoria.png` e `distribuicao_tempos.png`);
- Exportar resultados limpos em CSV (`atendimentos_processados.csv`), resumo estatístico em JSON (`resumo.json`) e log de erros (`erros.log`);
- Garantir tolerância a falhas (RF08) para que erros em registros não interrompam a execução do pipeline;
- Disponibilizar um Dashboard interativo complementar em **Streamlit**.

---

## 📌 Mapeamento da Implementação dos Requisitos Funcionais

Abaixo está o detalhamento técnico de como cada **Requisito Funcional (RF01 a RF08)** foi implementado nos módulos da aplicação:

### 🔹 RF01 — Inicialização
- **Requisito**: O sistema deverá ser executado pelo comando `python -m src.main`.
- **Implementação**: O módulo de entrada `src/main.py` contém a função de execução principal (`if __name__ == "__main__": main()`). A execução modular via `-m src.main` inicializa todas as etapas do pipeline em sequência a partir do diretório raiz.

### 🔹 RF02 — Leitura dos Dados
- **Requisito**: O sistema deverá ler os arquivos CSV, JSON e TXT indicados no arquivo de configuração.
- **Implementação**: No módulo `src/leitura.py`, foram criadas as funções `ler_json()`, `ler_csv()` e `ler_txt()`. O arquivo `data/config.json` armazena os caminhos dinâmicos dos arquivos de entrada e o parâmetro `"separador_csv": ";"`. A função `ler_csv()` lê o arquivo utilizando o delimitador configurado com fallback automático para vírgula.

### 🔹 RF03 — Validação
- **Requisito**: Cada registro deverá ser classificado como válido ou inválido. A aplicação deverá apresentar o motivo da rejeição de registros inválidos.
- **Implementação**: No módulo `src/validacao.py`, as funções `validar_email()`, `validar_tempo()`, `validar_data()`, `validar_protocolo()` e `validar_registro()` analisam cada linha do dataset. Se um registro for classificado como inválido, a lista de inconsistências encontradas (ex: `"email inválido"`, `"tempo de atendimento inválido"`) é associada ao registro para gravação detalhada no `erros.log`.

### 🔹 RF04 — Tratamento dos Dados
- **Requisito**: O sistema deverá remover espaços desnecessários, uniformizar maiúsculas e minúsculas, padronizar categorias, converter datas, tratar valores ausentes e eliminar duplicidades pelo protocolo.
- **Implementação**: No módulo `src/processamento.py`:
  - **Remover espaços e uniformizar caixa**: `limpar_texto()` e `padronizar_textos()` removem espaços desnecessários (`re.sub(r"\s+", " ", val)`) e ajustam a caixa (`.str.lower()` para e-mails e `.str.title()` para status).
  - **Padronizar categorias**: `padronizar_categorias()` e `mapear_categoria_valor()` utilizam o dicionário de sinônimos/palavras-chave do `data/categorias.json` para mapear variações de escrita para os nomes oficiais das categorias.
  - **Converter datas**: `padronizar_datas()` e `converter_data()` convertem múltiplos formatos (`YYYY-MM-DD`, `DD/MM/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY`) para o padrão ISO (`YYYY-MM-DD`).
  - **Tratar valores ausentes / tempos**: `tratar_tempos()` converte tempos para valores numéricos e transforma valores negativos (`<= 0`) ou outliers (`> 480`) em nulos (`NaN`).
  - **Eliminar duplicidades**: `remover_duplicidades()` utiliza `df.drop_duplicates(subset="protocolo", keep="first")`.
  - **Descarte de inválidos**: `processar_dados()` filtra e remove linhas inconsistentes do dataset final `atendimentos_processados.csv`.

### 🔹 RF05 — Análise Estatística
- **Requisito**: O sistema deverá produzir indicadores estatísticos utilizando Pandas e NumPy.
- **Implementação**: No módulo `src/processamento.py`, a função `calcular_indicadores()` utiliza **Pandas** para agrupamentos e distribuições por categoria/status (`value_counts()`) e **NumPy** para operações matemáticas vetoriais:
  - `np.mean()` (Tempo médio);
  - `np.median()` (Tempo mediano);
  - `np.min()` / `np.max()` (Tempos mínimo e máximo);
  - Normalização estatística do tempo médio referente ao limite de 480 minutos (`(tempo_medio / 480.0) * 100.0`).

### 🔹 RF06 — Visualização
- **Requisito**: O sistema deverá gerar e salvar pelo menos dois gráficos em formato PNG.
- **Implementação**: No módulo `src/relatorios.py`, as funções `gerar_grafico_categorias()` e `gerar_grafico_tempos()` utilizam a biblioteca **Matplotlib** para renderizar e salvar os arquivos de imagem em `output/graficos/`:
  - `atendimentos_por_categoria.png` (Gráfico de barras de distribuição por categoria);
  - `distribuicao_tempos.png` (Histograma de distribuição dos tempos de atendimento).

### 🔹 RF07 — Exportação
- **Requisito**: O sistema deverá gerar um CSV com os dados tratados, um JSON com o resumo dos indicadores e um arquivo de log com os problemas encontrados.
- **Implementação**: No módulo `src/relatorios.py`, as funções `salvar_csv()`, `salvar_json()` e `salvar_log()` exportam os resultados para o diretório `output/`:
  - `output/atendimentos_processados.csv`: Dataset contendo apenas os dados limpos, normalizados e válidos.
  - `output/resumo.json`: Arquivo JSON estruturado contendo todos os indicadores calculados.
  - `output/erros.log`: Arquivo de texto formatado detalhando os erros, advertências e motivos de rejeição por linha/protocolo.

### 🔹 RF08 — Tolerância a Falhas
- **Requisito**: A ocorrência de uma linha inválida não poderá encerrar toda a aplicação.
- **Implementação**: O pipeline em `src/main.py` percorre os registros de forma resiliente. Registros corrompidos ou com falhas de validação são devidamente isolados, auditados no `erros.log` e descartados da saída limpa sem interromper o fluxo de execução nem disparar exceções fatais que parem a aplicação CLI.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.14+**
- **Pandas** (Leitura, agrupamento e transformação de dados)
- **NumPy** (Cálculos matemáticos e normalização estatística)
- **Matplotlib** (Geração de gráficos em imagem PNG)
- **Streamlit** (Dashboard interativo web)
- **Pytest** (Suíte de testes unitários e de integração automatizados)
- **Regex (`re`)** (Extração de padrões de texto)
- **Git / GitHub** (Controle de versão e gestão de branches)

---

## 📁 Estrutura do Projeto

```text
desafio-01-python/
├── data/
│   ├── atendimentos.csv
│   ├── categorias.json
│   ├── config.json
│   └── observacoes.txt
├── output/
│   ├── atendimentos_processados.csv
│   ├── resumo.json
│   ├── erros.log
│   └── graficos/
│       ├── atendimentos_por_categoria.png
│       └── distribuicao_tempos.png
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── leitura.py
│   ├── validacao.py
│   ├── processamento.py
│   ├── relatorios.py
│   └── dashboard.py
├── tests/
│   ├── test_leitura.py
│   ├── test_pipeline.py
│   ├── test_processamento.py
│   └── test_validacao.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuração Dinâmica (`data/config.json`)

As configurações da aplicação ficam centralizadas no arquivo `data/config.json`:

```json
{
  "arquivo_atendimentos": "data/atendimentos.csv",
  "arquivo_categorias": "data/categorias.json",
  "arquivo_observacoes": "data/observacoes.txt",
  "diretorio_saida": "output",
  "separador_csv": ";"
}
```

---

## 🐍 Ambiente Virtual e Instalação

### 1. Criar o Ambiente Virtual

No Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Execução da Aplicação (RF01)

A aplicação principal em linha de comando (CLI) é executada a partir do diretório raiz pelo comando:

```bash
python -m src.main
```

---

## 🧪 Testes Automatizados (Pytest)

A suíte de testes cobre a leitura de arquivos, extração com Regex, validações de campos, tratamento de dados e pipeline completo.

Para executar os testes:

```bash
python -m pytest
```

### Resultado da Validação:

```text
============================== 34 passed in 0.35s ==============================
```

---

## 🔀 Controle de Versão e Branches

O projeto adotou uma estratégia de desenvolvimento modular com git branches por funcionalidade:

- **`main`**: Branch estável do repositório.
- **`develop-leo`**: Branch de consolidação com todas as funcionalidades integradas.
- **`feature/config-e-leitura`**: Adequação da leitura dinâmica e Regex.
- **`feature/padronizacao-categorias`**: Implementação do dicionário de sinônimos de categorias.
- **`feature/validacao-e-descarte`**: Regras de validação estrita, auditoria e filtragem de inválidos.
- **`feature/grafico-distribuicao-tempos`**: Ajustes na geração dos gráficos em PNG.

---

## 🤖 Uso de ferramentas de IA

Durante o desenvolvimento foi utilizada a ferramenta ChatGPT como apoio ao processo de desenvolvimento.

### Finalidades

A ferramenta foi utilizada para:

- Interpretar mensagens de erro;
- Auxiliar na compreensão de bibliotecas Python;
- Sugerir testes;
- Revisar a organização do código;
- Auxiliar na documentação;
- Auxiliar na organização do fluxo de Git e GitHub;
- Auxiliar na implementação e revisão do dashboard;
- Auxiliar na análise e correção de problemas.

### Exemplos de prompts utilizados

- "Me explique esse erro do Python."
- "Como posso organizar esse projeto em módulos?"
- "Como testar essa função com pytest?"
- "Como implementar filtros no dashboard?"
- "Como adicionar exportação dos dados filtrados?"
- "Revise a organização deste código."
- "Explique passo a passo como fazer o merge das branches."
- "Pode fazer uma revisão do projeto?"
- "Vamos corrigir esse problema."
- "Complete essa função."

### Participação dos discentes

As sugestões fornecidas pela ferramenta foram analisadas, testadas e adaptadas pelos discentes.

Os discentes foram responsáveis por:

- Implementar e modificar o código;
- Executar os comandos e testes;
- Analisar os resultados;
- Corrigir erros encontrados;
- Validar o funcionamento do pipeline;
- Decidir quais sugestões seriam incorporadas;
- Organizar os arquivos do projeto;
- Realizar os commits e operações de Git;
- Validar a execução final do sistema e do dashboard.

---

## 👨‍💻 Autores

- **Diego Assunção Leite**
- **Leonardo de Oliveira Ramos**

**Turma:** Vespertino — FIC_DEV Módulo Python para IA (SECITECI)