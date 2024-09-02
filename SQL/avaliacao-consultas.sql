/*a.Consulta para listar todas as doenças e seus respectivos dados. A consulta deve retornar id da doença, seu
nome, número CID, e o tipo do patógeno. A sequência em que as colunas serão apresentadas deve manter
essa ordem e as linhas organizadas em ordem alfabética em relação ao nome da doença.*/

SELECT 
	d.id,
	d.nome_tecnico,
	d.cid,
	p.tipo
FROM doencas d
JOIN patogenos p ON p.id = d.patogeno_id
ORDER BY nome_tecnico;

/*b.Consulta para listar os sintomas de uma doença específica. A consulta deve retornar o nome do sintoma e
sua taxa de ocorrência, nessa ordem de colunas, e de forma que as linhas sejam ordenadas pela taxa de
ocorrência em que sintomas mais frequentes devem ser posicionados acima dos sintomas menos
frequentes (em caso de dois ou mais sintomas com a mesma taxa de ocorrência, deve-se seguir com a
ordenação pela ordem alfabética em relação ao nome do sintoma).*/

SELECT 
	s.nome,
	ds.ocorrencia
FROM doenca_sintoma ds
JOIN sintomas s ON s.id = ds.sintoma_id
ORDER BY
	CASE ds.ocorrencia
		WHEN 'muito comum' THEN 1
		WHEN 'comum' THEN 2
		WHEN 'pouco comum' THEN 3
		ELSE 4
	END,
s.nome ASC;

/*c.Consulta para listar todas as doenças e seus respectivos sintomas. A consulta deve retornar id da doença,
seu nome, e os seus sintomas (juntamente com a taxa de ocorrência). A sequência em que as colunas serão
apresentadas deve manter essa ordem. As linhas devem ser organizadas em ordem alfabética em relação
ao nome da doença. Cada doença deve ser apresentada em uma única linha e, para doenças com múltiplos
sintomas, eles devem ser disponibilizados em uma única coluna separados por vírgula. Os sintomas devem
ser ordenados do muito comum ao muito raro. Para cada sintoma, a sua taxa de ocorrência deve vir entre
parênteses, logo em seguida ao nome do sintoma (por exemplo, “Febre (muito comum), Diarreia (raro),
Dor no corpo (muito raro)”).*/

SELECT 
	d.id,
	d.nome_tecnico,
	GROUP_CONCAT(CONCAT(s.nome, ' (', ds.ocorrencia, ') ') SEPARATOR ', ') AS sintomas
FROM doenca_sintoma ds
JOIN doencas d ON d.id = ds.doenca_id
JOIN sintomas s ON s.id = ds.sintoma_id
GROUP BY d.id
ORDER BY d.nome_tecnico ASC;

/*d.Consulta para calcular o número de doenças cadastradas para cada tipo de patógeno. Devem ser
apresentados o tipo do patógeno (vírus, bactéria, fungo, ...) e a quantidade de doenças cadastradas no
sistema que são causadas pelo respectivo tipo de patógeno. As colunas devem seguir a ordem especificada
e as linhas devem ser organizadas em ordem decrescente em relação à quantidade de doenças, seguida
pela ordem alfabética em relação ao tipo do patógeno.*/

SELECT 
	p.tipo,
	count(d.nome_tecnico) AS doencas
FROM patogenos AS p
RIGHT JOIN doencas d ON d.patogeno_id = p.id
GROUP BY p.tipo
ORDER BY doencas DESC, tipo ASC;

/*e.Consulta para obter algumas estatísticas sobre os dados armazenados no sistema. A consulta deverá
apresentar o número de doenças cadastradas, o número de sintomas cadastrados, o número médio de
sintomas por doença, o menor número de sintomas de uma doença, o maior número de sintomas de uma
doença. As colunas devem ser apresentadas nessa ordem e as linhas devem ser organizadas em ordem
crescente considerando a mesma ordem das colunas.*/

SELECT
	(SELECT COUNT(*) AS numero_de_doencas FROM doencas) AS num_doencas,
	(SELECT COUNT(*) AS numero_de_sintomas FROM sintomas) AS num_sintomas,
	AVG(numero_de_sintomas_por_doenca) AS media,
	MIN(numero_de_sintomas_por_doenca) AS minimo,
	MAX(numero_de_sintomas_por_doenca) AS maximo
FROM (
	SELECT COUNT(sintoma_id) AS numero_de_sintomas_por_doenca 
	FROM doenca_sintoma 
	GROUP BY doenca_id
) AS consultas
ORDER BY num_doencas ASC, num_sintomas ASC, media ASC, minimo ASC, maximo ASC;

/*f.Consulta com estatísticas sobre os sintomas. A consulta deve apresentar o nome do sintoma, o número
total de doenças que apresenta o sintoma, o número de doenças em que o sintoma é muito comum,
comum, pouco comum, raro e muito raro. As colunas devem ser apresentadas nesta ordem e as linhas
devem ser organizadas, em ordem decrescente, em relação ao número total de doenças, em seguida pela
taxa de ocorrência (do muito comum ao muito raro) e, por fim, por ordem alfabética em relação ao nome
do sintoma.*/

SELECT 
	s.nome,
	COUNT(ds.doenca_id) AS num_doencas_total,
	SUM(ds.ocorrencia = 'muito comum') AS num_doencas_muito_comum,
	SUM(ds.ocorrencia = 'comum') AS num_doencas_comum,
	SUM(ds.ocorrencia = 'pouco comum') AS num_doencas_pouco_comum,
	SUM(ds.ocorrencia = 'raro') AS num_doencas_raro,
	SUM(ds.ocorrencia = 'muito raro') AS num_doencas_muito_raro
FROM doenca_sintoma ds 
JOIN sintomas AS s ON s.id = ds.sintoma_id 
GROUP BY sintoma_id
ORDER BY num_doencas_total DESC, num_doencas_muito_comum DESC, num_doencas_comum DESC, num_doencas_pouco_comum DESC, num_doencas_raro DESC, num_doencas_muito_raro DESC, nome;


/*g.Consulta para listar todas as doenças que possuem um determinado conjunto de sintomas. Devem ser
apresentados o id da doença e o seu nome (mantendo as colunas nesta ordem e as linhas organizadas em
ordem alfabética em relação ao nome da doença). Para essa questão, considere o seguinte conjunto de
sintomas “Febre” e “Diarreia”.*/

SELECT 
	d.id, 
	d.nome_tecnico
FROM doencas d
WHERE d.id IN (
	SELECT ds1.doenca_id 
	FROM doenca_sintoma ds1 
	JOIN sintomas s1 ON ds1.sintoma_id = s1.id 
	WHERE s1.nome = 'Febre'
)
AND d.id IN (
	SELECT ds2.doenca_id 
	FROM doenca_sintoma ds2 
	JOIN sintomas s2 ON ds2.sintoma_id = s2.id 
	WHERE s2.nome = 'Diarreia'
)
ORDER BY d.nome_tecnico;


/*h. Consulta para listar as doenças mais prováveis para uma lista de sintomas analisada. A consulta deve
retornar o id da doença e o seu nome. Para essa consulta, deve-se considerar um esquema de pontuações
baseados nos sintomas, calculado da seguinte forma:
	1. Cada sintoma é atribuído a uma taxa de ocorrência. Essas taxas de ocorrência são convertidas em
	pesos numéricos: muito comum = 5; comum = 4; pouco comum = 3; raro = 2; muito raro = 1.
	2. Cada doença inicia com uma pontuação igual a 0 (zero). Para cada sintoma que uma doença tem
	em comum em relação à lista de sintomas avaliada, a pontuação da doença é incrementada pelo
	peso correspondente à taxa de ocorrência do sintoma.
	3. Para cada sintoma presente na lista e que uma doença não tenha em sua relação de sintomas, a
	pontuação da doença é decrementada em 1 ponto.
	4. As doenças são ordenadas em ordem decrescente em relação ao total de pontos obtidos.

LISTA:

2-FEBRE
23-DIARRÉIA

*/

SELECT
	doenca_id,
	d.nome_tecnico AS nome_doenca,
	GROUP_CONCAT(DISTINCT CONCAT(consulta.nome, '(', consulta.pesos_numericos, ')') ORDER BY consulta.nome SEPARATOR ', ') AS sintomas,
	SUM(CASE WHEN nome = 'Febre' THEN pesos_numericos ELSE 0 END) +
	SUM(CASE WHEN nome = 'Diarréia' THEN pesos_numericos ELSE 0 END) -
	COUNT(CASE WHEN nome NOT IN ('Febre', 'Diarréia') THEN 1 ELSE NULL END) AS pontuacao_doenca
FROM (
	SELECT 
		ds.doenca_id,
		s.nome,
		d.nome_tecnico,
		CASE 
		   WHEN ds.ocorrencia = 'muito comum' 	THEN 5
		   WHEN ds.ocorrencia = 'comum' 			THEN 4
		   WHEN ds.ocorrencia = 'pouco comum' 	THEN 3
		   WHEN ds.ocorrencia = 'raro' 			THEN 2
		   WHEN ds.ocorrencia = 'muito raro' 	THEN 1
		END AS pesos_numericos
	FROM doenca_sintoma AS ds
	JOIN sintomas AS s ON s.id = ds.sintoma_id
	JOIN doencas AS d ON d.id = ds.doenca_id
) AS consulta
JOIN doencas AS d ON d.id = doenca_id
GROUP BY doenca_id, d.nome_tecnico
ORDER BY pontuacao_doenca DESC;

