from flask import Flask, render_template, request, Response, redirect, url_for
import mysql.connector as mc
import json
from io import BytesIO
import base64

bd = mc.connect(
    database = 'seu_banco',
    user = 'root',
    password = 'senha'
)

def select(query):
    cursor = bd.cursor(dictionary=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

def data_manipulation(comando):
    cursor = bd.cursor()
    cursor.execute(comando)
    bd.commit()
    cursor.close()
    
    

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/professores', methods=['POST','GET'])
def professores():
    query = f"SELECT p.nome as nome_professor, p.cod as cod_professor, d.nome as nome_departamento FROM PROFESSOR p JOIN departamento d on p.cod_dept = d.cod "

    if request.method == 'POST':
        where = request.form["busca"]
        query += f"where p.nome LIKE '%{where}%' "

    # query += "LIMIT 1,10"
    professores = select(query)

    return render_template('professores.html', professores=professores)


@app.route('/professor/<cod_professor>')
def professor(cod_professor):

    comando = f"call proc_nota_professor({cod_professor},@nota)"
    data_manipulation(comando)

    query = f"SELECT p.nome as nome_professor, p.cod as cod_professor, d.nome as nome_departamento, @nota as nota FROM PROFESSOR p JOIN departamento d on p.cod_dept = d.cod WHERE p.cod = {cod_professor}"
    professor = select(query)[0]

    query = f"SELECT a.cod as cod_comentario, e.nome as nome_estudante, e.matricula as matricula,a.comentario as conteudo,a.tipo as tipo_avaliacao, a.nota as nota FROM avaliacao a join estudante e on e.matricula = a.matricula_estudante WHERE a.cod_professor = {cod_professor} and a.tipo = 1"
    
    comentarios = select(query)

    return render_template('professor.html',comentarios=comentarios,professor=professor)

@app.route('/avalia_professor', methods=['POST','GET'])
def avalia_professor():
    cod_professor = request.form["cod_professor"]
    nota = len(request.form["nota"])
    comentario = request.form["comentario"]
    matricula = request.form["matricula"]
    tipo = 1
    
    comando = f"INSERT INTO avaliacao(cod_professor,nota,comentario,matricula_estudante,tipo) VALUES({cod_professor},{nota},'{comentario}',{matricula},{tipo})"

    data_manipulation(comando)

    return professor(cod_professor)

@app.route('/delete_avaliacao/<cod_avaliacao>/<tipo_avaliacao>/<cod_tp>')
def delete_avaliacao(cod_avaliacao,tipo_avaliacao,cod_tp):
    comando = f"DELETE from avaliacao where cod = {cod_avaliacao}"
    data_manipulation(comando)
    tipo_avaliacao = int(tipo_avaliacao)

    if tipo_avaliacao == 1:
        return professor(cod_tp)
    elif tipo_avaliacao == 2:
        return turma(cod_tp)
    else:
        return pg_denuncias()

    

@app.route('/tela_atualiaza_avaliacao/<cod_avaliacao>')
def tela_atualiza_avaliacao(cod_avaliacao):
    query = f"SELECT * FROM AVALIACAO WHERE COD = {cod_avaliacao}"
    avaliacao = select(query)[0]

    return render_template('atualiza_avaliacao.html',avaliacao=avaliacao)

@app.route('/atualiza_avaliacao', methods=['POST','GET'])
def atualiza_avaliacao():
    nota = len(request.form["nota"])
    tipo = request.form["tipo_avaliacao"]
    comentario = request.form["comentario"]
    cod_avaliacao = request.form["cod_avaliacao"]
    
    comando = f"UPDATE avaliacao SET comentario = '{comentario}', nota = {nota} WHERE cod = {cod_avaliacao}"

    data_manipulation(comando)

    if int(tipo)== 1:
        query = f"SELECT cod_professor FROM AVALIACAO WHERE COD = {cod_avaliacao}"
        cod_professor = select(query)[0]["cod_professor"]
    
        return professor(cod_professor=cod_professor)
    else:
        query = f"SELECT cod_turma FROM avaliacao where cod = {cod_avaliacao}"
        cod_turma = select(query)[0]["cod_turma"]

        return turma(cod_turma=cod_turma)
    
@app.route('/denuncia_comentario/<cod_avaliacao>/<matricula>')
def denuncia_comentario(cod_avaliacao,matricula):
    comando = f"INSERT INTO denuncia(cod_avaliacao,cod_estudante) VALUES({cod_avaliacao},{matricula})"
    try:
        data_manipulation(comando)
    except Exception as e:
        pass

    query = f"SELECT tipo,cod_turma,cod_professor FROM AVALIACAO WHERE {cod_avaliacao} = cod"
    resultado = select(query)[0]

    tipo_avaliacao = int(resultado["tipo"])

    if tipo_avaliacao == 1:
        cod_professor = resultado["cod_professor"]
        return professor(cod_professor)
    else:
        cod_turma = resultado["cod_turma"]
        return turma(cod_turma)
    




@app.route('/turmas', methods=['POST','GET'])
def turmas():
    query = f"SELECT * FROM VW_TURMA_LOOKUP "

    if request.method == 'POST':
        where = request.form["busca"]
        query += f"where nome_disciplina LIKE '%{where}%' "

    # query += "LIMIT 1,10"
    
    lista_turmas = select(query)
    
    return render_template('turmas.html', lista_turmas = lista_turmas)



@app.route('/turma/<cod_turma>')
def turma(cod_turma):
    cod_turma = int(cod_turma)

    comando = f"CALL proc_nota_turma({cod_turma},@nota)"
    data_manipulation(comando)

    query = f"SELECT nome_disciplina,nome_prof,periodo,numero_turma,nome_dept,cod_turma,@nota as nota FROM VW_TURMA_LOOKUP WHERE COD_turma = {cod_turma}"
    att_turma = select(query)[0]
    
    query = f"SELECT a.cod as cod_comentario, e.nome as nome_estudante, e.matricula as matricula,a.comentario as conteudo, a.tipo as tipo_avaliacao, a.nota as nota  FROM avaliacao a join estudante e on e.matricula = a.matricula_estudante WHERE cod_turma = {cod_turma} and a.tipo = 2"
    comentarios = select(query)
    
    return render_template('turma.html',turma=att_turma,comentarios=comentarios)

@app.route('/pg_atualiza_turma/<cod_turma>')
def pg_atualiza_turma(cod_turma):
    query = f"SELECT * FROM TURMA WHERE cod={cod_turma}"
    turma = select(query)[0]

    query = f"SELECT * FROM PROFESSOR"
    lista_professores = select(query)

    return render_template('atualiza_turma.html',turma=turma,lista_professores=lista_professores)

@app.route('/atualiza_turma', methods=['POST','GET'])
def atualiza_turma():
    cod_turma = request.form["cod_turma"]
    professor = request.form["professor"]
    numero_turma = request.form["numero_turma"]
    periodo = request.form["periodo"]

    comando = f"UPDATE TURMA SET cod_professor = {professor}, numero_turma={numero_turma}, periodo='{periodo}' WHERE cod = {cod_turma}"

    data_manipulation(comando)

    return redirect(url_for('turmas'))


@app.route('/avalia_turma', methods=['POST','GET'])
def avalia_turma():
    cod_turma = request.form["cod_turma"]
    nota = len(request.form["nota"])
    comentario = request.form["comentario"]
    matricula = request.form["matricula"]
    tipo = 2

    comando = f"INSERT INTO avaliacao(matricula_estudante,nota,comentario,tipo,cod_turma) VALUES({matricula},{nota},'{comentario}',{tipo},{cod_turma})"

    data_manipulation(comando)

    return turma(cod_turma)


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/cria_perfil', methods=['GET','POST'])
def cria_perfil():
    cursor = bd.cursor()
    nome =  request.form["nome"]
    matricula =  request.form["matricula"]
    curso = request.form["curso"]
    email = request.form["email"]
    senha = request.form["senha"]
    tipo_estudante = 1

    foto = request.files["foto"].read()
    
    comando = """INSERT INTO estudante(nome,matricula,cod_curso,email,senha,cod_tipo_estudante,foto_perfil) VALUES(%s,%s,%s,%s,%s,%s,%s)"""

    values = (nome,matricula,curso,email,senha,tipo_estudante,foto)
    
    cursor.execute(comando,values)
    bd.commit()
    cursor.close()

    return render_template('index.html')

@app.route('/deleta_perfil/<matricula>')
def deleta_perfil(matricula):
    comando = f"DELETE FROM estudante WHERE matricula = {matricula}"
    data_manipulation(comando)

    return index()

@app.route('/pg_atualiza_perfil/<matricula>')
def pg_atualiza_perfil(matricula):
    return render_template('atualiza_perfil.html', matricula=matricula)


@app.route('/atualiza_perfil', methods=['POST','GET'])
def atualiza_perfil():
    nome = request.form["nome"]
    curso = request.form["curso"]
    email = request.form["email"]
    senha = request.form["senha"]
    matricula = request.form["matricula"]
    comando = f"UPDATE ESTUDANTE SET nome='{nome}' , cod_curso='{curso}', email='{email}', senha='{senha}' WHERE matricula = {matricula}"

    data_manipulation(comando)

    return index()


@app.route('/pg_login')
def pg_login():
    return render_template('login.html')


@app.route('/login', methods = ['GET','POST'])
def login():
    matricula = request.form["matricula"]
    senha = request.form["senha"]
    cursor = bd.cursor(dictionary=True)

    comando = f"SELECT matricula FROM estudante WHERE matricula = {matricula} AND senha = '{senha}'"
    cursor.execute(comando)
    retorno = cursor.fetchone()

    if retorno != None:
        return meu_perfil(matricula)
    else:
        return index()

    


@app.route('/meu_perfil/<matricula>')
def meu_perfil(matricula):
    query = f"SELECT * FROM ESTUDANTE e JOIN tipo_estudante te ON te.cod = e.cod_tipo_estudante WHERE MATRICULA = {matricula}"
    estudante = select(query)[0]
    # print(query)
    # foto = estudante["foto_perfil"]
    # foto = base64.b64encode(foto).decode('utf-8')
    # foto = Response(foto,mimetype='image/jpg')
    

    return render_template('meu_perfil.html', estudante=estudante)


@app.route('/pg_cria_turma')
def pg_cria_turma():
    query = "SELECT * from professor"
    lista_professores = select(query)

    query = "SELECT * from disciplina"
    lista_disciplinas = select(query)

    return render_template('cria_turma.html',lista_disciplinas=lista_disciplinas,lista_professores=lista_professores)

@app.route('/cria_turma', methods=['POST','GET'])
def cria_turma():
    cod_disciplina = request.form["disciplina"]
    cod_professor = request.form["professor"]
    periodo = request.form["periodo"]
    numero_turma = request.form["numero_turma"]

    comando = f"INSERT INTO turma(cod_disciplina,cod_professor,periodo,numero_turma) VALUES('{cod_disciplina}',{cod_professor},'{periodo}',{numero_turma})"
    data_manipulation(comando)

    return redirect(url_for('turmas'))

@app.route('/deleta_turma/<cod_turma>')
def deleta_turma(cod_turma):
    comando = f"DELETE FROM TURMA WHERE cod = {cod_turma}"
    data_manipulation(comando)

    return redirect(url_for('turmas'))


@app.route('/pg_denuncias')
def pg_denuncias():
    query = "SELECT * FROM vw_denuncia_comentario"

    lista_denuncias = select(query)

    return render_template('denuncias.html',lista_denuncias=lista_denuncias)



if __name__ == "__main__":
    app.run(debug=True)
