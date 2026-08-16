# 📊 Sistema de Análise de Atendimentos

Sistema desenvolvido em Python para leitura, tratamento, validação e análise de dados de atendimentos de suporte técnico.

O projeto recebe dados provenientes de arquivos CSV, JSON e TXT, realiza limpeza e padronização dos registros, valida os dados, calcula indicadores, gera relatórios, gráficos e disponibiliza um dashboard para análise dos atendimentos.

---

## 👨‍💻 Identificação

**Alunos:**
- Diego Assunção Leite
- Leonardo de Oliveira Ramos

**Turma:** Vespertino

---

## 🎯 Objetivo

O objetivo do projeto é construir uma aplicação completa de análise de dados capaz de:

- Ler arquivos CSV, JSON e TXT;
- Ler configurações armazenadas em JSON;
- Validar registros;
- Identificar registros inválidos ou incompletos;
- Limpar e padronizar dados;
- Padronizar categorias;
- Converter datas para um formato único;
- Tratar tempos de atendimento inválidos;
- Remover registros duplicados;
- Utilizar expressões regulares para validação e extração de dados;
- Calcular indicadores estatísticos;
- Utilizar Pandas para processamento e análise;
- Utilizar NumPy em operações numéricas;
- Gerar relatórios;
- Gerar arquivos CSV e JSON;
- Registrar problemas em arquivo de log;
- Gerar gráficos com Matplotlib;
- Executar testes automatizados;
- Disponibilizar um dashboard para visualização dos resultados.

---

## 🛠️ Tecnologias

- Python 3
- Pandas
- NumPy
- Matplotlib
- Streamlit
- Pytest
- Regex
- Git
- GitHub

---

## 📁 Estrutura do projeto

```text
desafio-01-python/
│
├── data/
│   ├── atendimentos.csv
│   ├── categorias.json
│   ├── observacoes.txt
│   └── config.json
│
├── output/
│   ├── atendimentos_processados.csv
│   ├── resumo.json
│   ├── erros.log
│   └── graficos/
│       ├── atendimentos_por_categoria.png
│       └── tempos_atendimento.png
│
├── src/
│   ├── __init__.py
│   ├── leitura.py
│   ├── processamento.py
│   ├── validacao.py
│   ├── relatorios.py
│   ├── main.py
│   └── dashboard.py
│
├── tests/
│   ├── test_leitura.py
│   ├── test_pipeline.py
│   ├── test_processamento.py
│   └── test_validacao.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuração

As configurações utilizadas pelo sistema ficam armazenadas no arquivo:

```text
data/config.json
```

Exemplo:

```json
{
    "arquivos": {
        "atendimentos": "data/atendimentos.csv",
        "categorias": "data/categorias.json",
        "observacoes": "data/observacoes.txt"
    },
    "saida": {
        "csv": "output/atendimentos_processados.csv",
        "json": "output/resumo.json",
        "log": "output/erros.log",
        "graficos": "output/graficos"
    }
}
```

---

## 🐍 Criação do ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Para verificar o Python utilizado:

```powershell
python -c "import sys; print(sys.executable)"
```

O caminho apresentado deve apontar para o diretório `.venv`.

---

## 📦 Instalação das dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
```

Principais bibliotecas:

- Pandas;
- NumPy;
- Matplotlib;
- Streamlit;
- Pytest.

---

## ▶️ Execução do sistema

Execute o pipeline principal:

```powershell
python -m src.main
```

Durante a execução, o sistema:

1. Verifica os arquivos necessários;
2. Lê os dados;
3. Extrai informações das observações;
4. Valida os registros;
5. Processa os dados;
6. Calcula os indicadores;
7. Salva os resultados;
8. Gera os gráficos;
9. Exibe o relatório no terminal.

---

## 📊 Dashboard

O projeto possui um dashboard desenvolvido com Streamlit.

Execute:

```powershell
python -m streamlit run src/dashboard.py
```

Depois acesse:

```text
http://localhost:8501
```

O dashboard apresenta:

- Indicadores principais;
- Atendimentos resolvidos;
- Atendimentos pendentes;
- Atendimentos em andamento;
- Tempo médio de atendimento;
- Categoria mais frequente;
- Filtros por categoria;
- Filtros por status;
- Tabela de atendimentos;
- Gráficos;
- Indicadores de qualidade dos dados;
- Registros com problemas;
- Exportação dos atendimentos filtrados em CSV;
- Informações do processamento.

---

## 🧪 Testes automatizados

Execute:

```powershell
python -m pytest
```

Resultado da validação final:

```text
33 passed
```

Os testes abrangem:

- Leitura de arquivos;
- Leitura de CSV;
- Leitura de JSON;
- Leitura de TXT;
- Verificação de arquivos;
- Extração de protocolos;
- Extração de telefones;
- Extração de e-mails;
- Validação dos dados;
- Processamento dos registros;
- Pipeline de processamento.

---

## 🧹 Tratamento dos dados

O sistema realiza:

- Remoção de espaços desnecessários;
- Padronização de textos;
- Padronização de e-mails;
- Padronização de status;
- Padronização das categorias;
- Conversão de datas;
- Tratamento de valores ausentes;
- Validação dos campos obrigatórios;
- Validação de e-mails;
- Tratamento de tempos de atendimento inválidos;
- Identificação de registros duplicados;
- Remoção de duplicidades pelo protocolo.

---

## 🗂️ Categorias

As categorias são definidas em:

```text
data/categorias.json
```

Categorias utilizadas:

- Acesso ao AVA;
- Instalação de Programas;
- Configuração Python;
- Problemas com Senha.

Exemplo:

```json
{
    "categorias": {
        "acesso ao ava": "Acesso ao AVA",
        "acesso ao ambiente virtual": "Acesso ao AVA",
        "instalação de programas": "Instalação de Programas",
        "instalacao de programas": "Instalação de Programas",
        "configuração python": "Configuração Python",
        "configuracao python": "Configuração Python",
        "problemas com senha": "Problemas com Senha"
    }
}
```

---

## ⚠️ Registros inválidos

Registros com problemas não interrompem a execução da aplicação.

São identificados problemas como:

- Campos obrigatórios vazios;
- E-mail inválido;
- Tempo de atendimento inválido.

Os problemas são registrados em:

```text
output/erros.log
```

---

## 🔎 Dados em TXT e expressões regulares

O arquivo:

```text
data/observacoes.txt
```

é utilizado como fonte adicional de informações.

O sistema utiliza expressões regulares para identificar:

- Protocolos;
- Telefones;
- E-mails.

Resultado da execução:

```text
Protocolos encontrados nas observações: 13
Telefones encontrados nas observações: 3
E-mails encontrados nas observações: 2
```

---

## 📈 Indicadores gerados

O sistema produz:

- Quantidade total de atendimentos;
- Quantidade por categoria;
- Quantidade por status;
- Tempo médio;
- Tempo mediano;
- Tempo mínimo;
- Tempo máximo;
- Tempo médio normalizado;
- Categoria mais frequente;
- Registros incompletos;
- Percentual de registros incompletos;
- Registros com problemas;
- Percentual de registros com problemas;
- Duplicidades removidas;
- Protocolos encontrados;
- Telefones encontrados;
- E-mails encontrados.

---

## 📊 Gráficos

Os gráficos são gerados com Matplotlib e armazenados em:

```text
output/graficos/
```

Arquivos:

```text
atendimentos_por_categoria.png
tempos_atendimento.png
```

---

## 📤 Arquivos de saída

Após a execução:

```text
output/
├── atendimentos_processados.csv
├── resumo.json
├── erros.log
└── graficos/
    ├── atendimentos_por_categoria.png
    └── tempos_atendimento.png
```

### atendimentos_processados.csv

Contém os registros tratados e padronizados.

### resumo.json

Contém os indicadores calculados.

### erros.log

Registra os problemas encontrados durante a validação e processamento.

---

## 📋 Resultado da execução

Resultado final:

```text
Registros originais: 13
Registros processados: 12
Duplicidades removidas: 1
```

### Atendimentos por categoria

```text
Acesso ao AVA: 3
Instalação de Programas: 3
Configuração Python: 3
Problemas com Senha: 3
```

### Atendimentos por status

```text
Resolvido: 7
Pendente: 3
Em Andamento: 2
```

### Indicadores de tempo

```text
Tempo médio: 35.56 minutos
Tempo mediano: 35.00 minutos
Tempo mínimo: 15.00 minutos
Tempo máximo: 60.00 minutos
Tempo médio normalizado: 7.41%
```

### Categoria mais frequente

```text
Acesso ao AVA
```

### Qualidade dos dados

```text
Registros incompletos: 4
Percentual de incompletos: 30.77%

Registros com problemas: 5
Percentual com problemas: 38.46%
```

### Informações extraídas

```text
Protocolos encontrados: 13
Telefones encontrados: 3
E-mails encontrados: 2
```

---

## 🔄 Fluxo de processamento

```text
Arquivos de entrada
        │
        ▼
   Leitura dos dados
        │
        ▼
Extração de informações
        │
        ▼
      Validação
        │
        ▼
Limpeza e padronização
        │
        ▼
Tratamento de tempos
        │
        ▼
Tratamento de duplicidades
        │
        ▼
Cálculo dos indicadores
        │
        ▼
Geração de relatórios
        │
        ├──────────────► CSV
        │
        ├──────────────► JSON
        │
        ├──────────────► LOG
        │
        └──────────────► Gráficos PNG
```

---

## 🧩 Organização dos módulos

### src/leitura.py

Responsável pela leitura dos arquivos e extração utilizando Regex.

Funções:

- Leitura de CSV;
- Leitura de JSON;
- Leitura de TXT;
- Verificação de arquivos;
- Extração de protocolos;
- Extração de telefones;
- Extração de e-mails.

### src/validacao.py

Responsável pela validação dos registros.

Realiza:

- Validação de e-mail;
- Validação de tempo;
- Validação de campos obrigatórios;
- Identificação dos problemas.

### src/processamento.py

Responsável pelo tratamento e análise dos dados.

Realiza:

- Limpeza de textos;
- Padronização de categorias;
- Conversão de datas;
- Tratamento de tempos;
- Remoção de duplicidades;
- Cálculo dos indicadores.

### src/relatorios.py

Responsável pela geração dos resultados.

Realiza:

- Salvamento do CSV;
- Salvamento do JSON;
- Salvamento do log;
- Geração do resumo;
- Geração dos gráficos.

### src/main.py

Responsável pela execução do pipeline completo.

### src/dashboard.py

Responsável pela interface visual desenvolvida com Streamlit.

---

## 🔐 Tolerância a falhas

O sistema foi desenvolvido para continuar o processamento mesmo quando são encontrados registros inválidos ou incompletos.

Os problemas identificados são registrados para posterior análise, evitando que uma única linha com erro interrompa todo o processamento.

---

## 🔀 Controle de versão

O projeto utiliza Git e GitHub para controle de versão.

Durante o desenvolvimento foram utilizadas branches para separar funcionalidades e posteriormente integrar as alterações.

As funcionalidades foram consolidadas na branch:

```text
main
```

O projeto foi sincronizado com o repositório remoto do GitHub.

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

## 🧪 Validação final

### Testes

```powershell
python -m pytest
```

Resultado:

```text
33 passed
```

### Pipeline

```powershell
python -m src.main
```

Resultado:

```text
Processamento concluído com sucesso!
```

### Dashboard

```powershell
python -m streamlit run src/dashboard.py
```

### Git

```powershell
git status
```

Resultado esperado:

```text
nothing to commit, working tree clean
```

### GitHub

```powershell
git push origin main
```

Resultado final:

```text
Everything up-to-date
```

---

## 👨‍💻 Autores

**Diego Assunção Leite**

**Leonardo de Oliveira Ramos**

**Turma:** Vespertino
