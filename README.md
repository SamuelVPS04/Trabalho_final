# README Técnico — Guia de Instalação

**Projeto:** Sistema Web com Controle de Acesso e Testes de Software  
**Disciplina:** Verificação, Validação e Teste de Software  
**Instituição:** UniDomBosco  
**Versão:** 1.0.0  

---

## 📋 Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Instalação Passo a Passo](#instalação-passo-a-passo)
4. [Configuração de Ambiente](#configuração-de-ambiente)
5. [Banco de Dados](#banco-de-dados)
6. [Execução da Aplicação](#execução-da-aplicação)
7. [Testes Automatizados](#testes-automatizados)
8. [Verificação de Saúde](#verificação-de-saúde)
9. [Troubleshooting](#troubleshooting)
10. [Comandos Úteis](#comandos-úteis)

---

## 🔧 Pré-requisitos

### Sistema Operacional
- **Linux** (Ubuntu 20.04+ / Debian 10+)
- **macOS** (10.14+)
- **Windows** (com WSL2 ou Git Bash)

### Dependências do Sistema

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    git \
    curl \
    build-essential

# macOS (com Homebrew)
brew install python@3.11 git

# Verificar instalação
python3 --version
pip3 --version
git --version
```

### Versões Suportadas

| Componente | Versão Mínima | Versão Testada |
|-----------|---------------|----------------|
| Python | 3.9 | 3.11.x |
| pip | 21.0 | 23.x |
| pip-tools | - | 6.14.0 |
| Git | 2.20 | 2.40+ |

---

## 📁 Estrutura do Projeto

```
Trabalho_final/
├── app.py                      # Aplicação principal Flask
├── models.py                   # Modelos do banco de dados
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── ANALISE_COMPLETA.md        # Análise técnica detalhada
├── .gitignore                 # Arquivos ignorados pelo Git
├── .env.example               # Template de variáveis de ambiente
├── .venv/                     # Ambiente virtual (criado)
├── static/                    # Arquivos estáticos
│   ├── style.css             # Estilos CSS
│   └── uploads/              # Uploads de usuários
├── templates/                # Templates HTML Jinja2
│   ├── admin.html            # Painel administrativo
│   ├── cadastro.html         # Formulário de cadastro
│   ├── index.html            # Página inicial
│   ├── login.html            # Tela de login
│   ├── noticia_detail.html   # Detalhes da notícia
│   ├── noticia_form.html     # Formulário de notícia
│   └── usuarios.html         # Perfil do usuário
├── tests/                    # Testes automatizados
│   ├── conftest.py          # Configuração Pytest
│   ├── test_auth.py         # Testes de autenticação
│   ├── test_admin_access.py # Testes de autorização
│   └── test_functional.py   # Testes end-to-end
├── sql/                      # Scripts SQL
│   └── init.sql             # Inicialização do banco
├── instance/                # Banco de dados (gerado)
│   └── sistema.db           # SQLite database
└── logs/                    # Logs (gerado)
    └── app.log
```

---

## 🚀 Instalação Passo a Passo

### 1. Clonar o Repositório

```bash
# Clone o repositório
git clone https://github.com/SamuelVPS04/Trabalho_final.git
cd Trabalho_final

# Verifique se está no branch correto
git branch -a
git checkout main
```

### 2. Criar Ambiente Virtual Python

```bash
# Linux/macOS
python3.11 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
python3.11 -m venv .venv
.\.venv\Scripts\activate.bat
```

**Verificar ativação:**

```bash
which python              # Linux/macOS
where python             # Windows

# Deverá mostrar o caminho dentro de .venv/
```

### 3. Atualizar pip, setuptools e wheel

```bash
pip install --upgrade pip setuptools wheel

# Verificar versões
pip --version
python --version
```

### 4. Instalar Dependências

```bash
# Instalar requirements.txt
pip install -r requirements.txt

# Verificar instalação
pip list

# Deverá mostrar:
# Flask==2.3.3
# Flask-SQLAlchemy==3.0.5
# Flask-Login==0.6.2
# Werkzeug==2.3.7
# pytest==7.4.0
# etc.
```

### 5. Criar Arquivo .env

```bash
# Copiar template
cp .env.example .env

# Editar com suas configurações (opcional)
nano .env
```

**Conteúdo de `.env`:**

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# Database Configuration
DATABASE_URL=sqlite:///sistema.db

# Server Configuration
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Upload Configuration
MAX_UPLOAD_SIZE=16777216
```

### 6. Inicializar Banco de Dados

```bash
# A aplicação cria o banco automaticamente ao iniciar
# Mas você pode executar manualmente:

python3 << 'EOF'
from app import app, db
from models import User

with app.app_context():
    # Criar todas as tabelas
    db.create_all()
    
    # Criar admin padrão
    admin = User.query.filter_by(email='admin@exemplo.com').first()
    if not admin:
        admin = User(
            nome='Administrador',
            email='admin@exemplo.com',
            tipo='admin'
        )
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado com sucesso")
    else:
        print("⚠️  Admin já existe")

EOF
```

---

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente Importantes

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `FLASK_ENV` | `development` | Ambiente (development/production) |
| `FLASK_DEBUG` | `True` | Debug mode |
| `SECRET_KEY` | `dev-key` | Chave secreta para sessions |
| `DATABASE_URL` | `sqlite:///sistema.db` | URL do banco de dados |
| `FLASK_HOST` | `127.0.0.1` | Host do servidor |
| `FLASK_PORT` | `5000` | Porta do servidor |

### Configuração para Produção

```bash
# .env para produção
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Gerar SECRET_KEY segura
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

---

## 💾 Banco de Dados

### Estrutura do Banco

**Tabela: `users`**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(200) NOT NULL,
    tipo VARCHAR(20) DEFAULT 'comum',
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

**Tabela: `noticias`**

```sql
CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    data_noticia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    texto TEXT NOT NULL,
    imagem VARCHAR(500),
    ativo BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_noticias_ativo ON noticias(ativo);
CREATE INDEX idx_noticias_data ON noticias(data_noticia DESC);
```

### Executar Script SQL

```bash
# Para SQLite (desenvolvido com este banco)
sqlite3 sistema.db < sql/init.sql

# Para PostgreSQL (se usar)
psql -U usuario -d database < sql/init.sql

# Para MySQL
mysql -u usuario -p database < sql/init.sql
```

### Limpar Banco de Dados

```bash
# ⚠️ Cuidado: isto deleta todos os dados

# SQLite
rm instance/sistema.db

# Recriar banco vazio
python3 << 'EOF'
from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Banco de dados recriado")

EOF
```

---

## ▶️ Execução da Aplicação

### Iniciar Servidor de Desenvolvimento

```bash
# Ativar ambiente virtual primeiro
source .venv/bin/activate  # Linux/macOS

# Iniciar Flask
python app.py

# Ou usar flask run
flask run

# Ou com parâmetros customizados
flask run --host=0.0.0.0 --port=8000 --debug
```

**Saída esperada:**

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Acessar Aplicação

- **URL:** http://127.0.0.1:5000
- **Admin Email:** admin@exemplo.com
- **Admin Senha:** admin123

### Modo Produção com Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Executar
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Com mais configurações
gunicorn -w 4 \
         -b 0.0.0.0:5000 \
         --timeout 30 \
         --access-logfile - \
         --error-logfile - \
         app:app
```

---

## 🧪 Testes Automatizados

### Executar Testes Completos

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Rodar todos os testes
pytest

# Saída esperada
# ======================== 8 passed in 0.45s ========================
```

### Executar Testes com Verbosidade

```bash
# Modo verbose
pytest -v

# Modo muito verbose
pytest -vv

# Com output de print
pytest -s

# Combinado
pytest -vvs
```

### Executar Testes Específicos

```bash
# Só testes de autenticação
pytest tests/test_auth.py -v

# Só testes de autorização
pytest tests/test_admin_access.py -v

# Só testes funcional
pytest tests/test_functional.py -v

# Um teste específico
pytest tests/test_auth.py::test_login_valid_credentials -v
```

### Gerar Relatório de Cobertura

```bash
# Instalar coverage
pip install pytest-cov

# Gerar relatório
pytest --cov=. --cov-report=html

# Abrir relatório
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Estrutura dos Testes

```
tests/
├── conftest.py                  # Fixtures compartilhadas
├── test_auth.py                 # 4 testes de autenticação
├── test_admin_access.py         # 4 testes de autorização
└── test_functional.py           # 1 teste end-to-end
```

**Resumo de Testes:**

| Arquivo | Testes | Função |
|---------|--------|--------|
| `test_auth.py` | 4 | Login válido, senha errada, email inexistente, usuário desativado |
| `test_admin_access.py` | 4 | Não autenticado, usuário comum, admin, rota direta |
| `test_functional.py` | 1 | Fluxo completo: criar, visualizar e desativar notícia |


## 🛠️ Comandos Úteis

### Gerenciamento de Ambiente Virtual

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows PowerShell

# Desativar
deactivate

# Deletar ambiente virtual
rm -rf .venv

# Atualizar pip
pip install --upgrade pip

# Listar pacotes instalados
pip list

# Congelar dependências atuais
pip freeze > requirements.txt

# Verificar packages desatualizados
pip list --outdated
```

### Banco de Dados

```bash
# Conectar ao SQLite
sqlite3 instance/sistema.db

# Listar tabelas (dentro do sqlite3)
.tables

# Ver schema da tabela
.schema users
.schema noticias

# Sair do sqlite3
.quit

# Fazer backup do banco
cp instance/sistema.db instance/sistema.db.bak

# Restaurar backup
cp instance/sistema.db.bak instance/sistema.db
```

### Flask CLI

```bash
# Listar rotas
flask routes

# Ver shell interativo
flask shell

# Executar com host customizado
flask run --host=0.0.0.0 --port=8000

# Ver variáveis de ambiente
flask config
```

### Git

```bash
# Ver status
git status

# Ver branches
git branch -a

# Ver commits
git log --oneline

# Ver diferenças
git diff

# Adicionar mudanças
git add .

# Commit
git commit -m "mensagem"

# Push
git push origin main
```

### Limpeza e Manutenção

```bash
# Remover arquivos temporários
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Remover environment
rm -rf .venv

# Limpar logs
rm -rf logs/*

# Verificar espaço em disco
du -sh .
du -sh static/uploads/
```

---

## 📦 Dependências Detalhadas

### requirements.txt

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
psycopg2-binary==2.9.7
python-dotenv==1.0.0
Werkzeug==2.3.7
Pillow==10.0.0
pytest==7.4.0
```

### Versões Python Recomendadas

- Python 3.11.x (principal)
- Python 3.10.x (compatível)
- Python 3.9.x (compatível)

