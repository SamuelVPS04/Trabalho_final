from app import app as flask_app, db
from models import Noticia


def login(client, email, senha):
    return client.post('/login', data={'email': email, 'senha': senha}, follow_redirects=True)


def test_admin_can_create_and_toggle_noticia(client):
    login(client, 'admin@exemplo.com', 'admin123')

    response = client.post(
        '/admin/noticia/criar',
        data={
            'titulo': 'Notícia de Teste',
            'texto': 'Conteúdo da notícia para validação de testes de fluxo.'
        },
        follow_redirects=True
    )
    html = response.get_data(as_text=True)
    assert 'Notícia criada com sucesso' in html

    response = client.get('/')
    html = response.get_data(as_text=True)
    assert 'Notícia de Teste' in html
    assert 'Conteúdo da notícia' in html

    with flask_app.app_context():
        noticia = Noticia.query.filter_by(titulo='Notícia de Teste').first()
        assert noticia is not None
        noticia_id = noticia.id

    response = client.post(f'/admin/noticia/toggle/{noticia_id}', follow_redirects=True)
    assert 'Notícia desativada' in response.get_data(as_text=True)

    response = client.get('/')
    assert 'Notícia de Teste' not in response.get_data(as_text=True)
