# 📊 Sistema de Análise de Atendimentos

Sistema desenvolvido em Python para leitura, tratamento, validação e análise de dados de atendimentos.

O projeto recebe dados em CSV, realiza limpeza e padronização, valida os registros, calcula indicadores e gera arquivos de saída e gráficos.

---

## 🎯 Objetivo

O objetivo do projeto é construir um pipeline completo de análise de dados capaz de:

- Ler arquivos CSV, JSON e TXT;
- Validar registros;
- Limpar e padronizar dados;
- Padronizar categorias;
- Converter datas para um formato único;
- Tratar tempos de atendimento inválidos;
- Remover registros duplicados;
- Calcular indicadores;
- Gerar relatórios;
- Gerar arquivos CSV e JSON;
- Registrar problemas em log;
- Gerar gráficos;
- Executar testes automatizados.

---

## 🛠️ Tecnologias

- Python
- Pandas
- NumPy
- Matplotlib
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
│   ├── leitura.py
│   ├── processamento.py
│   ├── validacao.py
│   ├── relatorios.py
│   └── main.py
│
├── tests/
│   ├── test_pipeline.py
│   ├── test_processamento.py
│   └── test_validacao.py
│
├── .gitignore
├── requirements.txt
└── README.md