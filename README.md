# Trabalho Final - Sistema de Notícias

## Descrição

Sistema web em Flask com controle de acesso, gerenciamento de usuários e CRUD de notícias. Usuários e notícias podem ser desativados sem exclusão física.

## Requisitos

- Python 3.11+
- Dependências em `requirements.txt`
- Banco SQLite por padrão via `app.py`

## Como executar

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Execute o app:

```bash
python app.py
```

O servidor será iniciado em `http://127.0.0.1:5000`.

## Usuário administrador padrão

- Email: `admin@exemplo.com`
- Senha: `admin123`

## Como executar testes

1. Ative o ambiente virtual.
2. Execute:

```bash
pytest
```
