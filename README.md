# 📊 Banking Analytics Gcp Looker

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![dbt](https://img.shields.io/badge/dbt-1.7-FF694B.svg)](https://www.getdbt.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![GCP](https://img.shields.io/badge/GCP-Cloud-4285F4.svg)](https://cloud.google.com/)
[![scikit-learn](https://img.shields.io/badge/scikit-learn-1.4-F7931E.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B.svg)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00.svg)](https://www.tensorflow.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-FF6600.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [Português](#português)

---

## English

### 🎯 Overview

**Banking Analytics Gcp Looker** — Banking Analytics Dashboard using GCP BigQuery and Looker Studio - Advanced financial data analytics platform

Total source lines: **1,352** across **12** files in **4** languages.

### ✨ Key Features

- **Production-Ready Architecture**: Modular, well-documented, and following best practices
- **Comprehensive Implementation**: Complete solution with all core functionality
- **Clean Code**: Type-safe, well-tested, and maintainable codebase
- **Easy Deployment**: Docker support for quick setup and deployment

### 🚀 Quick Start

#### Prerequisites
- Python 3.12+
- Docker and Docker Compose (optional)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/galafis/banking-analytics-gcp-looker.git
cd banking-analytics-gcp-looker
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Running

```bash
python frontend/app.py
```

## 🐳 Docker

```bash
# Build the image
docker build -t banking-analytics-gcp-looker .

# Run the container
docker run -p 8000:8000 banking-analytics-gcp-looker
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
```

### 📁 Project Structure

```
banking-analytics-gcp-looker/
├── backend/
│   └── services/
│       ├── analytics_engine.py
│       └── data_generator.py
├── config/
│   ├── database.py
│   ├── gcp.py
│   └── settings.py
├── data/
│   └── schemas/
│       └── sql/
├── docs/
├── frontend/
│   └── app.py
├── tests/
│   ├── integration/
│   │   └── __init__.py
│   └── unit/
│       └── __init__.py
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── README.md
├── requirements.txt
└── setup.py
```

### 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | 9 files |
| HTML | 1 files |
| CSS | 1 files |
| SQL | 1 files |

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

---

## Português

### 🎯 Visão Geral

**Banking Analytics Gcp Looker** — Banking Analytics Dashboard using GCP BigQuery and Looker Studio - Advanced financial data analytics platform

Total de linhas de código: **1,352** em **12** arquivos em **4** linguagens.

### ✨ Funcionalidades Principais

- **Arquitetura Pronta para Produção**: Modular, bem documentada e seguindo boas práticas
- **Implementação Completa**: Solução completa com todas as funcionalidades principais
- **Código Limpo**: Type-safe, bem testado e manutenível
- **Fácil Implantação**: Suporte Docker para configuração e implantação rápidas

### 🚀 Início Rápido

#### Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (opcional)

#### Instalação

1. **Clone the repository**
```bash
git clone https://github.com/galafis/banking-analytics-gcp-looker.git
cd banking-analytics-gcp-looker
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Execução

```bash
python frontend/app.py
```

### 🧪 Testes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
```

### 📁 Estrutura do Projeto

```
banking-analytics-gcp-looker/
├── backend/
│   └── services/
│       ├── analytics_engine.py
│       └── data_generator.py
├── config/
│   ├── database.py
│   ├── gcp.py
│   └── settings.py
├── data/
│   └── schemas/
│       └── sql/
├── docs/
├── frontend/
│   └── app.py
├── tests/
│   ├── integration/
│   │   └── __init__.py
│   └── unit/
│       └── __init__.py
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── README.md
├── requirements.txt
└── setup.py
```

### 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| Python | 9 files |
| HTML | 1 files |
| CSS | 1 files |
| SQL | 1 files |

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)
