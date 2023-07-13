INSERT INTO TIPO_ESTUDANTE(cod,descricao) VALUES(1,'COMUM');
INSERT INTO TIPO_ESTUDANTE(cod,descricao) VALUES(2,'ADMINISTRADOR');

INSERT INTO tipo_avaliacao(cod,descricao) values(1,'professor');
INSERT INTO tipo_avaliacao(cod,descricao) values(2,'turma');

INSERT INTO ESTUDANTE(nome,cod_curso,email,senha,cod_tipo_estudante) VALUES('Admin','Computação','admin@gmail.com','senha',2);
INSERT INTO ESTUDANTE(nome,cod_curso,email,senha,cod_tipo_estudante) VALUES('Pedro','Computação','pedro@gmail.com','senha',1);
INSERT INTO ESTUDANTE(nome,cod_curso,email,senha,cod_tipo_estudante) VALUES('Lucas','Computação','lucas@gmail.com','senha',1);

INSERT INTO departamento(cod,nome) VALUES(158,'DECANATO EXTENSÃO - BRASÍLIA');
INSERT INTO departamento(cod,nome) VALUES(351,'DEPARTAMENTO DE AUDIOVISUAIS E PUBLICIDADE/DAP - BRASÍLIA');
INSERT INTO departamento(cod,nome) VALUES(345,'DEPARTAMENTO DE COMUNICAÇÃO ORGANIZACIONAL/COM - BRASÍLIA');

INSERT INTO disciplina(cod,nome,cod_dept) VALUES('APC0013','POPULAÇÃO E MEIO AMBIENTE',345);
INSERT INTO disciplina(cod,nome,cod_dept) VALUES('BDS0015','INDICADORES DE DESENVOLVIMENTO SUSTENTÁVEL',345);
INSERT INTO disciplina(cod,nome,cod_dept) VALUES('RDSS0019','PRÁTICA DE PESQUISA 1',351);

INSERT INTO professor(nome,cod_dept) VALUES('JESSICA PEREIRA GARCIA',345);
INSERT INTO professor(nome,cod_dept) VALUES('DIEGO PEREIRA LINDOSO',345);
INSERT INTO professor(nome,cod_dept) VALUES('FREDERIC ADELIN GEORGES MERTENS',351);

INSERT INTO turma(numero_turma,periodo,cod_professor,cod_disciplina) VALUES(1,'2023.1',149625,'APC0013');
INSERT INTO turma(numero_turma,periodo,cod_professor,cod_disciplina) VALUES(1,'2023.1',149626,'BDS0015');
INSERT INTO turma(numero_turma,periodo,cod_professor,cod_disciplina) VALUES(1,'2023.1',149627,'RDSS0019');


INSERT INTO avaliacao(cod_professor,nota,comentario,matricula_estudante,tipo) VALUES(149625,4,'Otimo professor explica bem',223,1);
INSERT INTO avaliacao(cod_professor,nota,comentario,matricula_estudante,tipo) VALUES(149625,3,'Professor razoavel',224,1);
INSERT INTO avaliacao(matricula_estudante,nota,comentario,tipo,cod_turma) VALUES(223,5,'Da pra aprender',2,90559);


INSERT INTO denuncia(cod_avaliacao,cod_estudante) VALUES(48,223);
INSERT INTO denuncia(cod_avaliacao,cod_estudante) VALUES(48,224);
INSERT INTO denuncia(cod_avaliacao,cod_estudante) VALUES(49,223);

