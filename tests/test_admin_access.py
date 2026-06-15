from app import app as flask_app
from models import User
from app import db


def login(client, email, senha):
    return client.post('/login', data={'email': email, 'senha': senha}, follow_redirects=True)


def test_unauthenticated_access_is_redirected(client):
    response = client.get('/admin', follow_redirects=True)
    html = response.get_data(as_text=True)
    assert 'Por favor, faça login' in html or 'Acesso ao Sistema' in html


def test_common_user_cannot_access_admin(client):
    with flask_app.app_context():
        usuario = User(nome='Usuário Comum', email='user@exemplo.com', tipo='comum')
        usuario.set_senha('senha123')
        db.session.add(usuario)
        db.session.commit()

    login(client, 'user@exemplo.com', 'senha123')
    response = client.get('/admin', follow_redirects=True)
    html = response.get_data(as_text=True)
    assert 'Acesso negado' in html
    assert 'Sistema de Notícias' in html or 'Painel Administrativo' not in html


def test_admin_user_can_access_admin(client):
    login(client, 'admin@exemplo.com', 'admin123')
    response = client.get('/admin')
    assert 'Painel Administrativo' in response.get_data(as_text=True)


def test_direct_admin_route_blocked_for_common_user(client):
    with flask_app.app_context():
        usuario = User(nome='Usuário Comum', email='user2@exemplo.com', tipo='comum')
        usuario.set_senha('senha123')
        db.session.add(usuario)
        db.session.commit()

    login(client, 'user2@exemplo.com', 'senha123')
    response = client.get('/admin/noticia/criar', follow_redirects=True)
    assert 'Acesso negado' in response.get_data(as_text=True)
