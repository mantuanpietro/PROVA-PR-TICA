import mysql.connector
from werkzeug.security import check_password_hash

CHAVE = "chave_escola"

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senai",
        database="escola_db"
    )

def autenticar_usuario(email, senha):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT nome, email, senha FROM usuario WHERE email = %s''',
            (email,)
        )
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario['senha'], senha):
            return usuario
        return None
    finally:
        cursor.close()
        conexao.close()

def listar_responsaveis(termo):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = '''SELECT id_responsavel, nome, telefone, 
        CAST(AES_DECRYPT(cpf, %s) AS CHAR) AS cpf 
        FROM responsavel
        WHERE nome LIKE %s '''
    cursor.execute(sql, (CHAVE, '%' + termo + '%'))
    lista = cursor.fetchall()
    conexao.close()
    return lista

def buscar_responsavel(id_responsavel):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = '''SELECT id_responsavel, nome, telefone,
             CAST(AES_DECRYPT(cpf, %s) AS CHAR) AS cpf
             FROM responsavel
             WHERE id_responsavel = %s'''
    cursor.execute(sql, (CHAVE, id_responsavel))
    responsavel = cursor.fetchone()
    conexao.close()
    return responsavel

def cadastrar_responsavel(nome, cpf, telefone):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = '''INSERT INTO responsavel (nome, cpf, telefone)
                 VALUES (%s, AES_ENCRYPT(%s, %s), %s)'''
        cursor.execute(sql, (nome, cpf, CHAVE, telefone))
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()

def atualizar_responsavel(id_responsavel, nome, cpf, telefone):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = '''UPDATE responsavel
              SET nome = %s, cpf = AES_ENCRYPT(%s, %s), telefone = %s
              WHERE id_responsavel = %s'''
    cursor.execute(sql, (nome, cpf, CHAVE, telefone, id_responsavel))
    conexao.commit()
    conexao.close()

def excluir_responsavel(id_responsavel):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            'DELETE FROM responsavel WHERE id_responsavel = %s',
            (id_responsavel,)
        )
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()

def listar_aulas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = '''SELECT au.id_aula, au.data_hora, al.nome AS aluno, al.instrumento, r.nome AS responsavel, r.telefone, CAST(AES_DECRYPT(r.cpf, %s) AS CHAR) AS cpf 
        FROM aula au
        JOIN aluno al ON al.id_aluno = au.id_aluno
        JOIN responsavel r ON r.id_responsavel = al.id_responsavel
        ORDER BY YEAR(au.data_hora), au.data_hora'''
    cursor.execute(sql,(CHAVE,))
    lista = cursor.fetchall()
    conexao.close()
    return lista

def buscar_aula(id_aula):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = '''SELECT id_aula, data_hora FROM aula WHERE id_aula = %s'''
    cursor.execute(sql, (id_aula,))
    aula = cursor.fetchone()
    conexao.close()
    return aula

def atualizar_data_aula(id_aula, data_hora):
    conexao =conectar()
    cursor = conexao.cursor()
    sql = '''UPDATE aula SET data_hora = %s WHERE id_aula = %s'''
    cursor.execute(sql, (data_hora, id_aula))
    conexao.commit()
    conexao.close()

def cadastrar_aluno(nome, instrumento, id_responsavel):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = '''INSERT INTO aluno (nome, instrumento, id_responsavel)
             VALUES (%s, %s, %s)'''
    cursor.execute(sql, (nome, instrumento, id_responsavel))
    conexao.commit()
    conexao.close()