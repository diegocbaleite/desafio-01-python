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

Durante a execução, o pipeline realiza:
1. Verificação dos arquivos de entrada configurados em `config.json`;
2. Leitura dos dados em CSV, JSON e TXT;
3. Extração de contatos e protocolos das observações em TXT via Regex;
4. Auditoria e classificação dos registros em válidos/inválidos;
5. Processamento dos dados (normalização, remoção de duplicidades e filtragem de inválidos);
6. Cálculo de estatísticas e indicadores com Pandas e NumPy;
7. Exportação dos arquivos em `output/` (`atendimentos_processados.csv`, `resumo.json` e `erros.log`);
8. Geração das imagens dos gráficos em PNG (`output/graficos/`);
9. Exibição do relatório gerencial formatado no terminal.

---

## 📊 Dashboard Interativo (Streamlit)

Para iniciar a interface gráfica interativa desenvolvida em Streamlit:

```bash
python -m streamlit run src/dashboard.py
```

Acesse o endereço exibido no terminal (por padrão: `http://localhost:8501`).

O dashboard oferece:
- Métricas em tempo real (Total de atendimentos, Resolvidos, Pendentes, Em Andamento);
- Indicadores de desempenho de tempo (Média, Mediana, Mínimo e Máximo);
- Filtros dinâmicos por categoria, status, período e busca por texto;
- Tabela interativa de atendimentos com opção de download dos dados filtrados em CSV;
- Gráficos visuais por categoria e status;
- Indicadores de qualidade de dados.

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

## 🤖 Uso de Ferramentas de IA

No desenvolvimento do projeto foi utilizada assistência de IA generativa (ChatGPT e Gemini Antigravity) como apoio ao aprendizado e par programação:

- Auxílio na interpretação de mensagens de erro do Python/Pandas;
- Sugestões para estruturação de expressões regulares;
- Apoio na organização dos testes unitários com Pytest;
- Revisão da documentação e alinhamento aos requisitos do desafio.

Todas as sugestões foram analisadas, testadas e adaptadas pelos alunos, mantendo a responsabilidade integral pelo código e entrega final.

---

## 👨‍💻 Autores

- **Diego Assunção Leite**
- **Leonardo de Oliveira Ramos**

**Turma:** Vespertino — FIC_DEV Módulo Python para IA (SECITECI)