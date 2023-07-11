
CREATE TABLE `departamento` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=1665 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `disciplina` (
  `cod` varchar(30) NOT NULL,
  `nome` varchar(150) NOT NULL,
  `cod_dept` int NOT NULL,
  PRIMARY KEY (`cod`),
  KEY `disciplina_fk_departamento` (`cod_dept`),
  CONSTRAINT `disciplina_fk_departamento` FOREIGN KEY (`cod_dept`) REFERENCES `departamento` (`cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tipo_avaliacao` (
  `cod` int NOT NULL,
  `descricao` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`cod`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tipo_estudante` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(15) NOT NULL,
  PRIMARY KEY (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `estudante` (
  `matricula` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) NOT NULL,
  `cod_curso` varchar(50) DEFAULT NULL,
  `email` varchar(30) NOT NULL,
  `senha` varchar(30) NOT NULL,
  `cod_tipo_estudante` int NOT NULL,
  `foto_perfil` mediumblob,
  PRIMARY KEY (`matricula`),
  KEY `estudante_fk_tipo_estudante` (`cod_tipo_estudante`),
  CONSTRAINT `estudante_fk_tipo_estudante` FOREIGN KEY (`cod_tipo_estudante`) REFERENCES `tipo_estudante` (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=223 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `professor` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) DEFAULT NULL,
  `cod_dept` int NOT NULL,
  PRIMARY KEY (`cod`),
  UNIQUE KEY `unico_nome_prof` (`nome`),
  KEY `professor_fk_departamento` (`cod_dept`),
  CONSTRAINT `professor_fk_departamento` FOREIGN KEY (`cod_dept`) REFERENCES `departamento` (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=149625 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `turma` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `numero_turma` int NOT NULL,
  `periodo` varchar(7) NOT NULL,
  `cod_professor` int NOT NULL,
  `cod_disciplina` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`cod`),
  UNIQUE KEY `unicidade` (`numero_turma`,`periodo`,`cod_disciplina`),
  KEY `turma_fk_professor` (`cod_professor`),
  KEY `turma_fk_disciplina` (`cod_disciplina`),
  CONSTRAINT `turma_fk_disciplina` FOREIGN KEY (`cod_disciplina`) REFERENCES `disciplina` (`cod`),
  CONSTRAINT `turma_fk_professor` FOREIGN KEY (`cod_professor`) REFERENCES `professor` (`cod`)
) ENGINE=InnoDB AUTO_INCREMENT=90559 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `avaliacao` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `comentario` text NOT NULL,
  `nota` int NOT NULL,
  `matricula_estudante` int NOT NULL,
  `cod_professor` int DEFAULT NULL,
  `cod_turma` int DEFAULT NULL,
  `tipo` int DEFAULT NULL,
  PRIMARY KEY (`cod`),
  KEY `avaliacao_fk_professor` (`cod_professor`),
  KEY `avaliacao_fk_tipo_avaliacao` (`tipo`),
  KEY `avaliacao_fk_estudante` (`matricula_estudante`),
  KEY `avaliacao_fk_turma` (`cod_turma`),
  CONSTRAINT `avaliacao_fk_estudante` FOREIGN KEY (`matricula_estudante`) REFERENCES `estudante` (`matricula`) ON DELETE CASCADE,
  CONSTRAINT `avaliacao_fk_professor` FOREIGN KEY (`cod_professor`) REFERENCES `professor` (`cod`),
  CONSTRAINT `avaliacao_fk_tipo_avaliacao` FOREIGN KEY (`tipo`) REFERENCES `tipo_avaliacao` (`cod`),
  CONSTRAINT `avaliacao_fk_turma` FOREIGN KEY (`cod_turma`) REFERENCES `turma` (`cod`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `denuncia` (
  `cod` int NOT NULL AUTO_INCREMENT,
  `cod_avaliacao` int NOT NULL,
  `cod_estudante` int NOT NULL,
  PRIMARY KEY (`cod`),
  UNIQUE KEY `denuncia_unica` (`cod_estudante`,`cod_avaliacao`),
  KEY `denuncia_fk_avaliacao` (`cod_avaliacao`),
  CONSTRAINT `denuncia_fk_avaliacao` FOREIGN KEY (`cod_avaliacao`) REFERENCES `avaliacao` (`cod`) ON DELETE CASCADE,
  CONSTRAINT `denuncia_fk_estudante` FOREIGN KEY (`cod_estudante`) REFERENCES `estudante` (`matricula`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;











CREATE or replace VIEW vw_turma_lookup
AS(
	SELECT t.cod as cod_turma, t.numero_turma, t.periodo, t.cod_disciplina, d.nome as nome_disciplina, p.nome as nome_prof, dept.nome as nome_dept
    FROM turma t
    JOIN professor p ON p.cod = t.cod_professor
    JOIN disciplina d on d.cod = t.cod_disciplina
    JOIN departamento dept ON d.cod_dept = dept.cod
);

CREATE OR REPLACE VIEW vw_denuncia_comentario
AS SELECT  distinct a.cod, a.comentario, e.nome, (
	SELECT count(*)
    FROM avaliacao av
    JOIN denuncia d ON d.cod_avaliacao = av.cod
    where a.cod = av.cod
    group by av.cod
) as qtd_denuncias


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `proc_nota_professor`(IN cod_professor INTEGER, OUT nota float)
BEGIN
	SELECT CASE
		WHEN AVG(a.nota) IS NULL THEN 0
        ELSE avg(a.nota)
        end
    into nota
    from professor p
    left join avaliacao a ON a.cod_professor = p.cod
    where p.cod = cod_professor;
END$$

DELIMITER ;
;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `proc_nota_turma`(IN cod_turma INTEGER, OUT nota FLOAT)
BEGIN
	SELECT CASE
		WHEN AVG(a.nota) IS NULL THEN 0
        ELSE avg(a.nota)
        end
    into nota
    from turma t
    left join avaliacao a ON a.cod_turma = t.cod
    where t.cod = cod_turma;

END$$

DELIMITER ;
;
