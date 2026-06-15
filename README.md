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

Isso roda os testes de login, controle de acesso e fluxo funcional.

## Resultados obtidos

- Autenticação com email/senha e hash seguro.
- Controle de acesso para área administrativa.
- CRUD de usuários com desativação de contas.
- CRUD de notícias com marcação de ativo/inativo.
- Testes automatizados com Pytest para login, autorização e fluxo de notícia.

## Dificuldades encontradas

- Ajustar o ambiente para suportar teste end-to-end com navegador no container.
- Garantir que as rotas de administração bloqueiem corretamente usuários comuns e não autenticados.
- Manter o upload de imagens seguro e com nome de arquivo único.
