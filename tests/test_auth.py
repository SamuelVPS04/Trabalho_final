from app import app as flask_app, db
from models import User


def login(client, email, senha):
    return client.post('/login', data={'email': email, 'senha': senha}, follow_redirects=True)


def test_login_valid_credentials(client):
    response = login(client, 'admin@exemplo.com', 'admin123')
    assert 'Bem-vindo' in response.get_data(as_text=True)
    assert 'Painel Administrativo' in response.get_data(as_text=True)


def test_login_invalid_password(client):
    response = login(client, 'admin@exemplo.com', 'senhaerrada')
    assert 'Senha incorreta' in response.get_data(as_text=True)
    assert 'Login' in response.get_data(as_text=True)


def test_login_nonexistent_email(client):
    response = login(client, 'naoexiste@exemplo.com', 'qualquer')
    assert 'E-mail não cadastrado' in response.get_data(as_text=True)


def test_login_deactivated_user(client):
    with flask_app.app_context():
        usuario = User(nome='Usuário Desativado', email='desativado@exemplo.com', tipo='comum', ativo=False)
        usuario.set_senha('senha123')
        db.session.add(usuario)
        db.session.commit()

    response = login(client, 'desativado@exemplo.com', 'senha123')
    assert 'Usuário desativado' in response.get_data(as_text=True)
