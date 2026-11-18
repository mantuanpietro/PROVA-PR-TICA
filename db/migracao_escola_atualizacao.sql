USE escola_db;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO usuario (nome, email, senha) VALUES
('Marta Silva', 'marta@escola.com', 'scrypt:32768:8:1$nyRoDSGIsHd6Ws10$7149f9db371fe3b7ffc6a159c92e1549006b4fac39b4db1edff4d83a76da0c2ed0d3b1f4e79bd756b1a0bba5c09490ad60813866c77dfc18ea0a0dc4bf8ce345'),
('Rui Costa', 'rui@escola.com', 'scrypt:32768:8:1$tXOWcLRWc7phPbnz$02a04d52db7da96e6890d0402a11441146770eeb46f9602a309672921829280f1a06e411ee499be327fb5453b1c85a07592ff4cbfa6d419035ac96c1afba293b'),
('Ana Lopes', 'ana@escola.com', 'scrypt:32768:8:1$UOhXX5rm9PvPk6QA$066ed3ec7133b40799aad576c42296fd191b97b165c906e02d5d07ab70385c4aa25fbff093b50df998178f89d11d1965bd6dabbefc4f2d201e6aa8179d7f3fc4')
ON DUPLICATE KEY UPDATE email = VALUES(email);

ALTER TABLE aluno
    DROP FOREIGN KEY aluno_ibfk_1,
    ADD CONSTRAINT fk_aluno_responsavel
        FOREIGN KEY (id_responsavel)
        REFERENCES responsavel (id_responsavel)
        ON DELETE CASCADE;

ALTER TABLE aula
    DROP FOREIGN KEY aula_ibfk_1,
    ADD CONSTRAINT fk_aula_aluno
        FOREIGN KEY (id_aluno)
        REFERENCES aluno (id_aluno)
        ON DELETE CASCADE;
