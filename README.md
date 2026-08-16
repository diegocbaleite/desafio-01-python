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

O arquivo define os arquivos de entrada e os arquivos de saída utilizados pelo sistema.

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

No Windows PowerShell, execute:

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

As principais bibliotecas utilizadas são:

- Pandas;
- NumPy;
- Matplotlib;
- Streamlit;
- Pytest.

---

## ▶️ Execução do sistema

A aplicação principal deve ser executada com:

```powershell
python -m src.main
```

Durante a execução, o sistema:

1. Verifica os arquivos necessários;
2. Lê os dados;
3. Valida os registros;
4. Processa os dados;
5. Calcula os indicadores;
6. Salva os resultados;
7. Gera os gráficos;
8. Exibe o relatório no terminal.

---

## 📊 Dashboard

O projeto possui um dashboard desenvolvido com Streamlit.

Para executá-lo:

```powershell
python -m streamlit run src/dashboard.py
```

Depois acesse no navegador:

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
- Exportação dos atendimentos filtrados em CSV.

---

## 🧪 Testes automatizados

Os testes são executados utilizando Pytest:

```powershell
python -m pytest
```

Durante a validação do projeto foram obtidos:

```text
24 passed
```

Os testes abrangem:

- Validação dos dados;
- Processamento dos registros;
- Pipeline de processamento.

---

## 🧹 Tratamento dos dados

O sistema realiza diferentes etapas de tratamento, incluindo:

- Remoção de espaços desnecessários;
- Padronização de textos;
- Padronização das categorias;
- Conversão de datas;
- Tratamento de valores ausentes;
- Validação dos campos obrigatórios;
- Validação de e-mails;
- Tratamento de tempos de atendimento inválidos;
- Identificação de registros duplicados;
- Remoção de duplicidades pelo protocolo.

As categorias utilizadas pelo sistema são definidas no arquivo:

```text
data/categorias.json
```

As categorias configuradas incluem:

- Acesso ao AVA;
- Instalação de programas;
- Configuração do Python;
- Senha;
- Execução de atividades.

---

## ⚠️ Registros inválidos

Registros com problemas não interrompem a execução da aplicação.

Os problemas encontrados durante o processamento são registrados em:

```text
output/erros.log
```

Dessa forma, uma linha inválida não impede o processamento dos demais registros.

---

## 🔎 Dados em TXT e expressões regulares

O arquivo:

```text
data/observacoes.txt
```

é utilizado como fonte adicional de informações.

O sistema utiliza expressões regulares para identificar padrões presentes nas observações, como protocolos e telefones.

O arquivo de observações contém exemplos de contatos associados a protocolos de atendimento.

---

## 📈 Indicadores gerados

O sistema produz indicadores como:

- Quantidade total de atendimentos;
- Quantidade de atendimentos por categoria;
- Quantidade de atendimentos por status;
- Tempo médio de atendimento;
- Categoria com maior número de solicitações;
- Quantidade de registros incompletos;
- Percentual de registros incompletos;
- Quantidade de registros com problemas;
- Percentual de registros com problemas;
- Quantidade de duplicidades removidas.

---

## 📊 Gráficos

Os gráficos são gerados utilizando Matplotlib.

Os arquivos são armazenados em:

```text
output/graficos/
```

Gráficos gerados:

```text
atendimentos_por_categoria.png
tempos_atendimento.png
```

---

## 📤 Arquivos de saída

Após a execução do pipeline, os resultados são armazenados no diretório:

```text
output/
```

São gerados:

```text
output/
├── atendimentos_processados.csv
├── resumo.json
├── erros.log
└── graficos/
    ├── atendimentos_por_categoria.png
    └── tempos_atendimento.png
```

O arquivo `atendimentos_processados.csv` contém os registros tratados.

O arquivo `resumo.json` contém o resumo dos indicadores.

O arquivo `erros.log` registra problemas encontrados durante o processamento.

---

## 📋 Resultado da execução

Durante a validação do projeto foram obtidos os seguintes resultados:

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

### Indicadores

```text
Tempo médio: 35.56 minutos
Categoria mais frequente: Acesso ao AVA
Registros incompletos: 4
Percentual de incompletos: 30.77%
```

---

## 🔄 Fluxo de processamento

O processamento dos dados segue as seguintes etapas:

```text
Arquivos de entrada
        │
        ▼
   Leitura dos dados
        │
        ▼
      Validação
        │
        ▼
  Limpeza e padronização
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

## 🔐 Tolerância a falhas

O sistema foi desenvolvido para continuar o processamento mesmo quando são encontrados registros inválidos ou incompletos.

Os problemas identificados são registrados para posterior análise, evitando que uma única linha com erro interrompa todo o processamento.

---

## 🔀 Controle de versão

O projeto utiliza Git e GitHub para controle de versão.

Durante o desenvolvimento foram utilizadas branches para separar funcionalidades e posteriormente integrar as alterações.

Após a validação, as funcionalidades foram consolidadas na branch principal:

```text
main
```

---

## 🤖 Uso de ferramentas de IA

Durante o desenvolvimento do projeto foi utilizada a ferramenta **ChatGPT** como apoio ao processo de desenvolvimento.

### Finalidades

A ferramenta foi utilizada para:

- Interpretar mensagens de erro;
- Auxiliar na compreensão de bibliotecas Python;
- Sugerir testes;
- Revisar a organização do código;
- Auxiliar na documentação;
- Auxiliar na organização do fluxo de Git e GitHub;
- Auxiliar na implementação e revisão do dashboard.

### Exemplos de prompts utilizados

Alguns exemplos de solicitações realizadas:

- "Me explique esse erro do Python."
- "Como posso organizar esse projeto em módulos?"
- "Como testar essa função com pytest?"
- "Como implementar filtros no dashboard?"
- "Como adicionar exportação dos dados filtrados?"
- "Revise a organização deste código."
- "Explique passo a passo como fazer o merge das branches."

### Participação dos discentes

As sugestões fornecidas pela ferramenta foram analisadas, testadas e adaptadas pelos discentes.

O código foi executado e validado durante o desenvolvimento por meio dos testes automatizados, do pipeline principal e da execução do dashboard.

---

## 👨‍💻 Autores

**Diego Assunção Leite**  
**Leonardo de Oliveira Ramos**

**Turma:** Vespertino