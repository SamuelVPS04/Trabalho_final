import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from models import db, User, Noticia

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_path = os.path.join(basedir, 'sistema.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{default_db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de upload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Inicializar extensões
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return f'/static/uploads/{filename}'
    return None

# ==================== ROTAS PÚBLICAS ====================

@app.route('/')
def index():
    noticias = Noticia.query.filter_by(ativo=True).order_by(Noticia.data_noticia.desc()).all()
    return render_template('index.html', noticias=noticias)

# ==================== AUTENTICAÇÃO ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_painel'))
        return redirect(url_for('usuario_perfil'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('E-mail não cadastrado!', 'danger')
        elif not user.check_senha(senha):
            flash('Senha incorreta!', 'danger')
        elif not user.ativo:
            flash('Usuário desativado! Contate o administrador.', 'danger')
        else:
            login_user(user)
            flash(f'Bem-vindo, {user.nome}!', 'success')
            if user.is_admin():
                return redirect(url_for('admin_painel'))
            return redirect(url_for('usuario_perfil'))
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios!', 'danger')
        elif senha != confirmar_senha:
            flash('As senhas não coincidem!', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
        else:
            novo_user = User(nome=nome, email=email, tipo='comum')
            novo_user.set_senha(senha)
            db.session.add(novo_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado!', 'info')
    return redirect(url_for('index'))

# ==================== USUÁRIO COMUM ====================

@app.route('/perfil')
@login_required
def usuario_perfil():
    return render_template('usuarios.html', user=current_user)

@app.route('/perfil/editar', methods=['POST'])
@login_required
def editar_perfil():
    if current_user.is_admin():
        return redirect(url_for('admin_painel'))
    
    novo_nome = request.form.get('nome')
    if novo_nome:
        current_user.nome = novo_nome
        db.session.commit()
        flash('Nome atualizado com sucesso!', 'success')
    
    return redirect(url_for('usuario_perfil'))

# ==================== ADMINISTRADOR ====================

@app.route('/noticia/<int:noticia_id>')
def noticia_detalhe(noticia_id):
    noticia = Noticia.query.get_or_404(noticia_id)
    if not noticia.ativo and (not current_user.is_authenticated or not current_user.is_admin()):
        abort(404)
    return render_template('noticia_detail.html', noticia=noticia)


@app.route('/admin')
@login_required
def admin_painel():
    if not current_user.is_admin():
        flash('Acesso negado! Área restrita para administradores.', 'danger')
        return redirect(url_for('index'))
    
    usuarios = User.query.all()
    noticias = Noticia.query.order_by(Noticia.data_noticia.desc()).all()
    return render_template('admin.html', usuarios=usuarios, noticias=noticias)

@app.route('/admin/usuario/criar', methods=['POST'])
@login_required
def admin_criar_usuario():
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('index'))
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    tipo = request.form.get('tipo', 'comum')
    
    if not nome or not email or not senha:
        flash('Nome, e-mail e senha são obrigatórios!', 'danger')
        return redirect(url_for('admin_painel'))
    
    if User.query.filter_by(email=email).first():
        flash('E-mail já cadastrado!', 'danger')
        return redirect(url_for('admin_painel'))
    
    novo_user = User(nome=nome, email=email, tipo=tipo)
    novo_user.set_senha(senha)
    db.session.add(novo_user)
    db.session.commit()
    
    flash(f'Usuário {nome} criado com sucesso!', 'success')
    return redirect(url_for('admin_painel'))

@app.route('/admin/usuario/editar/<int:user_id>', methods=['POST'])
@login_required
def admin_editar_usuario(user_id):
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    tipo = request.form.get('tipo')
    senha = request.form.get('senha')
    
    if nome:
        user.nome = nome
    if email and email != user.email:
        if User.query.filter_by(email=email).first():
            flash('E-mail já está em uso!', 'danger')
            return redirect(url_for('admin_painel'))
        user.email = email
    if tipo:
        user.tipo = tipo
    if senha:
        user.set_senha(senha)
    
    db.session.commit()
    flash(f'Usuário {user.nome} atualizado!', 'success')
    return redirect(url_for('admin_painel'))

@app.route('/admin/usuario/toggle/<int:user_id>', methods=['POST'])
@login_required
def admin_toggle_usuario(user_id):
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Você não pode desativar seu próprio usuário!', 'danger')
        return redirect(url_for('admin_painel'))
    
    user.ativo = not user.ativo
    status = 'ativado' if user.ativo else 'desativado'
    db.session.commit()
    
    flash(f'Usuário {user.nome} {status}!', 'success')
    return redirect(url_for('admin_painel'))

# Rota API para buscar dados de um usuário específico (usado pelo modal de edição)
@app.route('/admin/usuario/<int:user_id>', methods=['GET'])
@login_required
def admin_get_usuario(user_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'tipo': user.tipo,
        'ativo': user.ativo
    })

# ==================== CRUD NOTÍCIAS ====================

@app.route('/admin/noticia/criar', methods=['GET', 'POST'])
@login_required
def admin_criar_noticia():
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        imagem = request.files.get('imagem')
        
        if not titulo or not texto:
            flash('Título e texto são obrigatórios!', 'danger')
            return redirect(url_for('admin_criar_noticia'))
        
        imagem_path = save_image(imagem) if imagem and imagem.filename else None
        
        nova_noticia = Noticia(
            titulo=titulo,
            texto=texto,
            imagem=imagem_path,
            created_by=current_user.id
        )
        
        db.session.add(nova_noticia)
        db.session.commit()
        
        flash('Notícia criada com sucesso!', 'success')
        return redirect(url_for('admin_painel'))
    
    return render_template('noticia_form.html', noticia=None)

@app.route('/admin/noticia/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_editar_noticia(id):
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('index'))
    
    noticia = Noticia.query.get_or_404(id)
    
    if request.method == 'POST':
        noticia.titulo = request.form.get('titulo')
        noticia.texto = request.form.get('texto')
        
        imagem = request.files.get('imagem')
        if imagem and imagem.filename:
            imagem_path = save_image(imagem)
            if imagem_path:
                noticia.imagem = imagem_path
        
        db.session.commit()
        flash('Notícia atualizada!', 'success')
        return redirect(url_for('admin_painel'))
    
    return render_template('noticia_form.html', noticia=noticia)

@app.route('/admin/noticia/toggle/<int:id>', methods=['POST'])
@login_required
def admin_toggle_noticia(id):
    if not current_user.is_admin():
        flash('Acesso negado!', 'danger')
        return redirect(url_for('index'))
    
    noticia = Noticia.query.get_or_404(id)
    noticia.ativo = not noticia.ativo
    status = 'ativada' if noticia.ativo else 'desativada'
    db.session.commit()
    
    flash(f'Notícia {status}!', 'success')
    return redirect(url_for('admin_painel'))

# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Criar admin padrão se não existir
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
            print("\n=== USUÁRIO ADMIN CRIADO ===")
            print("Email: admin@exemplo.com")
            print("Senha: admin123")
            print("============================\n")
    
    app.run(debug=True)