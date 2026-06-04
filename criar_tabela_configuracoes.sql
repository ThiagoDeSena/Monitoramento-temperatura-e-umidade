-- Criar tabela para armazenar setpoint e histerese (apenas último valor)
CREATE TABLE IF NOT EXISTS configuracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setpoint FLOAT NULL DEFAULT NULL,
    histerese FLOAT NULL DEFAULT NULL,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inserir registro inicial (se não existir)
INSERT IGNORE INTO configuracoes (id, setpoint, histerese) VALUES (1, NULL, NULL);

-- Criar índice para acesso rápido
CREATE INDEX idx_data ON configuracoes(data_atualizacao);
