DROP DATABASE IF EXISTS avaliacao;
CREATE DATABASE IF NOT EXISTS avaliacao;
USE avaliacao;

CREATE TABLE IF NOT EXISTS patogenos (
	id INT AUTO_INCREMENT PRIMARY KEY,  
	nome_cientifico VARCHAR(128) NOT NULL, 
	tipo VARCHAR(64) NOT NULL          
);

CREATE TABLE IF NOT EXISTS doencas(
	id INT AUTO_INCREMENT PRIMARY KEY,
	cid VARCHAR(16),
	nome_tecnico VARCHAR(128) NOT NULL,
	patogeno_id INT NOT NULL,
	FOREIGN KEY (patogeno_id) REFERENCES patogenos(id)
);

CREATE TABLE IF NOT EXISTS doenca_nomes_populares (
	doenca_id INT,
	nome_popular VARCHAR(128) NOT NULL,
	PRIMARY KEY (doenca_id, nome_popular),
	FOREIGN KEY (doenca_id) REFERENCES doencas(id)
);

CREATE TABLE IF NOT EXISTS sintomas(
	id INT AUTO_INCREMENT PRIMARY KEY,
	nome VARCHAR(64) NOT NULL 
);

CREATE TABLE IF NOT EXISTS doenca_sintoma(
	doenca_id INT,
	sintoma_id INT,
	ocorrencia VARCHAR(16) NOT NULL,
	PRIMARY KEY (doenca_id, sintoma_id),
	FOREIGN KEY (doenca_id) REFERENCES doencas(id),
	FOREIGN KEY (sintoma_id) REFERENCES sintomas(id)
);

SHOW TABLES;