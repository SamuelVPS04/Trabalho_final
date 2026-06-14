from app import app, db
from models import User

with app.app_context():
    # Verificar se já existe
    admin = User.query.filter_by(email='admin@exemplo.com').first()
    
    if admin:
        print(f"Admin já existe: {admin.email}")
        # Resetar a senha
        admin.set_senha('admin123')
        db.session.commit()
        print("Senha resetada para: admin123")
    else:
        # Criar novo admin
        admin = User(
            nome='Administrador',
            email='admin@exemplo.com',
            tipo='admin',
            ativo=True
        )
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin criado com sucesso!")
    
    print(f"Email: admin@exemplo.com")
    print(f"Senha: admin123")