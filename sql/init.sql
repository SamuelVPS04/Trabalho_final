-- Estrutura do banco de dados
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(200) NOT NULL,
    tipo VARCHAR(20) DEFAULT 'comum',
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS noticias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    data_noticia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    texto TEXT NOT NULL,
    imagem VARCHAR(500),
    ativo BOOLEAN DEFAULT TRUE,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_noticias_ativo ON noticias(ativo);
CREATE INDEX idx_noticias_data ON noticias(data_noticia DESC);

-- Insert de usuário administrador padrão
INSERT IGNORE INTO users (nome, email, senha_hash, tipo, ativo)
VALUES (
    'Administrador',
    'admin@exemplo.com',
    'pbkdf2:sha256:600000$84vtPKfbP8MLr4JV$42a193df1325817a0e0bf45f6b021975552811a9adc6440712b125439da5cacd',
    'admin',
    TRUE
);
