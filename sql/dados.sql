USE avaliacao;

INSERT INTO patogenos (id, nome_cientifico, tipo) VALUES
(1, 'Mycobacterium tuberculosis', 'Bactéria'),
(2, 'Influenza virus', 'Vírus'),
(3, 'Plasmodium spp.', 'Parasita'),
(4, 'Dengue virus', 'Vírus'),
(5, 'Hepatitis B virus', 'Vírus'),
(6, 'Treponema pallidum', 'Bactéria'),
(7, 'Candida albicans', 'Fungo'),
(8, 'Varicella-zoster virus', 'Vírus'),
(9, 'Leptospira spp.', 'Bactéria'),
(10, 'Toxoplasma gondii', 'Parasita'),
(11, 'Neisseria meningitidis', 'Bactéria'),
(12, 'Yellow fever virus', 'Vírus'),
(13, 'Zika virus', 'Vírus'),
(14, 'Chikungunya virus', 'Vírus'),
(15, 'Rubella virus', 'Vírus'),
(16, 'Measles virus', 'Vírus'),
(17, 'Clostridium tetani', 'Bactéria'),
(18, 'Mycobacterium leprae', 'Bactéria'),
(19, 'Vibrio cholerae', 'Bactéria'),
(20, 'Salmonella typhi', 'Bactéria'),
(21, 'Poliovirus', 'Vírus'),
(22, 'Rabies virus', 'Vírus'),
(23, 'Schistosoma spp.', 'Parasita'),
(24, 'Giardia lamblia', 'Parasita'),
(25, 'Entamoeba histolytica', 'Parasita'),
(26, 'Trichomonas vaginalis', 'Parasita'),
(27, 'Trypanosoma cruzi', 'Parasita'),
(28, 'Leishmania spp.', 'Parasita'),
(29, 'Clostridium tetani', 'Bactéria'),
(30, 'Hepatitis A virus', 'Vírus'),
(31, 'Hepatitis C virus', 'Vírus'),
(32, 'Herpes simplex virus', 'Vírus'),
(33, 'Variola virus', 'Vírus'),
(34, 'Epstein-Barr virus', 'Vírus'),
(35, 'Mumps virus', 'Vírus'),
(36, 'Clostridium tetani', 'Bactéria'),
(37, 'Hepatitis A virus','Vírus'),
(38, 'Hepatitis C virus','Vírus'),
(39, 'Herpes simplex virus','Vírus'),
(40, 'Variola virus','Vírus');

INSERT INTO doencas (id, cid, nome_tecnico, patogeno_id) VALUES
(1, 'A15-A19', 'Tuberculose', 1),
(2, 'J10-J11', 'Gripe', 2),
(3, 'B50-B54', 'Malária', 3),
(4, 'A90', 'Dengue', 4),
(5, 'B16', 'Hepatite B', 5),
(6, 'A50-A53', 'Sífilis', 6),
(7, 'B37', 'Candidíase', 7),
(8, 'B01', 'Varicela', 8),
(9, 'A27', 'Leptospirose', 9),
(10, 'B58', 'Toxoplasmose', 10),
(11, 'G00-G03', 'Meningite', 11),
(12, 'A95', 'Febre Amarela', 12),
(13, 'A92.5', 'Zika', 13),
(14, 'A92.0', 'Chikungunya', 14),
(15, 'B06', 'Rubéola', 15),
(16, 'B05', 'Sarampo', 16),
(17, 'A33-A35', 'Tétano', 17),
(18, 'A30', 'Hanseníase', 18),
(19, 'A00', 'Cólera', 19),
(20, 'A01.0', 'Tifoide', 20),
(21, 'A80', 'Poliomielite', 21),
(22, 'A82', 'Raiva', 22),
(23, 'B65', 'Esquistossomose', 23),
(24, 'A07.1', 'Giardíase', 24),
(25, 'A06', 'Amebíase', 25),
(26, 'A59', 'Tricomoníase', 26),
(27, 'B57', 'Doença de Chagas', 27),
(28, 'B55', 'Leishmaniose', 28),
(29, 'A33', 'Tétano Neonatal', 29),
(30, 'B15', 'Hepatite A', 30),
(31, 'B17.1', 'Hepatite C', 31),
(32, 'B00', 'Herpes Simples', 32),
(33, 'B03', 'Varíola', 33),
(34, 'B27', 'Mononucleose', 34),
(35, 'B26', 'Caxumba', 35),
(36, 'A33', 'Tétano Neonatal', 36),
(37, 'B15', 'Hepatite A', 37),
(38, 'B17.1', 'Hepatite C', 38),
(39, 'B00', 'Herpes Simples', 39),
(40, 'B03', 'Varíola', 40);

INSERT INTO doenca_nomes_populares (doenca_id, nome_popular) VALUES
(7, 'Sapinho'),
(8, 'Catapora'),
(18, 'Lepra'),
(23, 'Barriga d’água'),
(34, 'Doença do Beijo'),
(35, 'Papeira');

INSERT INTO sintomas (id, nome) VALUES 
(1, 'Tosse'),
(2, 'Febre'),
(3, 'Perda de peso'),
(4, 'Dor de cabeça'),
(5, 'Fadiga'),
(6, 'Calafrios'),
(7, 'Dor muscular'),
(8, 'Erupção cutânea'),
(9, 'Icterícia'),
(10, 'Úlceras'),
(11, 'Coceira'),
(12, 'Corrimento'),
(13, 'Dor ao urinar'),
(14, 'Ínguas'),
(15, 'Rigidez de nuca'),
(16, 'Espasmos musculares'),
(17, 'Desidratação'),
(18, 'Náusea'),
(19, 'Paralisia'),
(20, 'Feridas na pele'),
(21, 'Dor de garganta'),
(22, 'Inchaço das glândulas'),
(23, 'Diarréia'),
(24, 'Dor Abdominal'),
(25, 'Rigidez'),
(26, 'Manchas na pele'),
(27, 'Perda de sensibilidade'),
(28, 'Fraqueza muscular'),
(29, 'Vômito'),
(30, 'Inchaço no local da picada'),
(31, 'Feridas');

-- Tuberculose (1)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(1, 1, 'muito comum'), -- Tosse
(1, 2, 'comum'), -- Febre
(1, 3, 'comum'); -- Perda de peso

-- Gripe (2)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(2, 2, 'muito comum'), -- Febre
(2, 4, 'comum'), -- Dor de Cabeça
(2, 5, 'comum'); -- Fadiga

-- Malária (3)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(3, 2, 'muito comum'), -- Febre
(3, 6, 'muito comum'), -- Calafrios
(3, 4, 'comum'); -- Dor de Cabeça

-- Dengue (4)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(4, 2, 'muito comum'), -- Febre
(4, 7, 'comum'), -- Dor muscular
(4, 8, 'comum'); -- Erupção cutânea

-- Hepatite B (5)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(5, 9, 'comum'), -- Icterícia
(5, 5, 'comum'), -- Fadiga
(5, 24, 'comum'); -- Dor abdominal

-- Sífilis (6)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(6, 10, 'comum'), -- Úlceras
(6, 8, 'comum'), -- Erupção cutânea
(6, 2, 'pouco comum'); -- Febre

-- Candidíase (7)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(7, 11, 'muito comum'), -- Coceira
(7, 12, 'comum'), -- Corrimento
(7, 13, 'pouco comum'); -- Dor ao urinar

-- Varicela (8)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(8, 8, 'muito comum'), -- Erupção cutânea
(8, 2, 'comum'), -- Febre
(8, 11, 'comum'); -- Coceira

-- Leptospirose (9)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(9, 2, 'muito comum'), -- Febre
(9, 7, 'comum'), -- Dor muscular
(9, 9, 'pouco comum'); -- Icterícia

-- Toxoplasmose (10)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(10, 2, 'pouco comum'), -- Febre
(10, 7, 'pouco comum'), -- Dor muscular
(10, 14, 'pouco comum'); -- Ínguas

-- Meningite (11)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(11, 2, 'muito comum'), -- Febre
(11, 4, 'muito comum'), -- Dor de cabeça
(11, 15, 'comum'); -- Rigidez de nuca

-- Febre Amarela (12)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(12, 2, 'muito comum'), -- Febre
(12, 9, 'comum'), -- Icterícia
(12, 7, 'comum'); -- Dor muscular

-- Zika (13)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(13, 2, 'comum'), -- Febre
(13, 8, 'comum'), -- Erupção cutânea
(13, 7, 'comum'); -- Dor articular

-- Chikungunya (14)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(14, 2, 'muito comum'), -- Febre
(14, 7, 'muito comum'), -- Dor articular
(14, 8, 'comum'); -- Erupção cutânea

-- Rubéola (15)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(15, 8, 'muito comum'), -- Erupção cutânea
(15, 2, 'comum'), -- Febre
(15, 14, 'comum'); -- Ínguas

-- Sarampo (16)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(16, 8, 'muito comum'), -- Erupção cutânea
(16, 2, 'muito comum'), -- Febre
(16, 1, 'comum'); -- Tosse

-- Tétano (17)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(17, 16, 'muito comum'), -- Espasmos musculares
(17, 25, 'muito comum'), -- Rigidez
(17, 2, 'pouco comum'); -- Febre

-- Hanseníase (18)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(18, 26, 'muito comum'), -- Manchas na pele
(18, 27, 'comum'), -- Perda de sensibilidade
(18, 28, 'pouco comum'); -- Fraqueza muscular


-- Cólera (19)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(19, 23, 'muito comum'), -- Diarreia
(19, 29, 'comum'), -- Vômito
(19, 17, 'comum'); -- Desidratação

-- Tifoide (20)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(20, 2, 'muito comum'), -- Febre
(20, 24, 'comum'), -- Dor abdominal
(20, 8, 'pouco comum'); -- Erupção cutânea

-- Poliomielite (21)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(21, 19, 'muito comum'), -- Paralisia
(21, 2, 'comum'), -- Febre
(21, 7, 'comum'); -- Dor muscular

-- Raiva (22)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(22, 2, 'muito comum'), -- Febre
(22, 4, 'comum'), -- Dor de cabeça
(22, 16, 'comum'); -- Espasmos musculares

-- Esquistossomose (23)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(23, 2, 'comum'), -- Febre
(23, 24, 'comum'), -- Dor abdominal
(23, 23, 'pouco comum'); -- Diarreia

-- Giardíase (24)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(24, 23, 'muito comum'), -- Diarreia
(24, 24, 'comum'), -- Dor abdominal
(24, 18, 'comum'); -- Náusea

-- Amebíase (25)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(25, 23, 'muito comum'), -- Diarreia
(25, 24, 'comum'), -- Dor abdominal
(25, 2, 'pouco comum'); -- Febre

-- Tricomoníase (26)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(26, 12, 'muito comum'), -- Corrimento
(26, 11, 'comum'), -- Coceira
(26, 13, 'pouco comum'); -- Dor ao urinar

-- Doença de Chagas (27)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(27, 2, 'comum'), -- Febre
(27, 30, 'comum'), -- Inchaço no local da picada
(27, 24, 'pouco comum'); -- Dor abdominal

-- Leishmaniose (28)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(28, 20, 'muito comum'), -- Feridas na pele
(28, 2, 'comum'), -- Febre
(28, 3, 'comum'); -- Perda de peso

-- Tétano Neonatal (29)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(29, 16, 'muito comum'), -- Espasmos musculares
(29, 25, 'muito comum'), -- Rigidez
(29, 2, 'pouco comum'); -- Febre

-- Hepatite A (30)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(30, 9, 'comum'), -- Icterícia
(30, 5, 'comum'), -- Fadiga
(30, 24, 'comum'); -- Dor abdominal

-- Hepatite C (31)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(31, 9, 'comum'), -- Icterícia
(31, 5, 'comum'), -- Fadiga
(31, 24, 'comum'); -- Dor abdominal

-- Herpes Simples (32)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(32, 31, 'muito comum'), -- Feridas
(32, 11, 'comum'), -- Coceira
(32, 13, 'pouco comum'); -- Dor ao urinar

-- Varíola (33)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(33, 8, 'muito comum'), -- Erupção cutânea
(33, 2, 'muito comum'), -- Febre
(33, 7, 'comum'); -- Dor muscular

-- Mononucleose (34)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(34, 2, 'muito comum'), -- Febre
(34, 21, 'comum'), -- Dor de garganta
(34, 5, 'comum'); -- Fadiga

-- Caxumba (35)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(35, 22, 'muito comum'), -- Inchaço das glândulas
(35, 2, 'comum'), -- Febre
(35, 4, 'comum'); -- Dor de cabeça

-- Tétano Neonatal (36)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(36, 16, 'muito comum'), -- Espasmos musculares
(36, 25, 'muito comum'), -- Rigidez
(36, 2, 'pouco comum'); -- Febre

-- Hepatite A (37)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(37, 9, 'comum'), -- Icterícia
(37, 5, 'comum'), -- Fadiga
(37, 24, 'comum'); -- Dor abdominal

-- Hepatite C (38)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(38, 9, 'comum'), -- Icterícia
(38, 5, 'comum'), -- Fadiga
(38, 24, 'comum'); -- Dor abdominal

-- Herpes Simples (39)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(39, 31, 'muito comum'), -- Feridas
(39, 11, 'comum'), -- Coceira
(39, 13, 'pouco comum'); -- Dor dor ao urinar

-- varíola (40)
INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES
(40, 8, 'muito comum'); -- Erupção cutânea
