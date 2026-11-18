from datetime import datetime, timedelta
from  flask import Flask, render_template, request, redirect, session
import database

app = Flask(__name__)
app.secret_key = 'escola'
app.permanent_session_lifetime = timedelta(minutes=5)

def logado():
    return 'nome' in session

@app.route('/', methods=['GET','POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = database.autenticar_usuario(
            request.form['email'],
            request.form['senha']
        )
        if usuario:
            session.permanent = True
            session['nome'] = usuario['nome']
            return redirect('/home')
        erro = 'Email ou senha inválidos. Tente novamente.'
    return render_template('login.html', erro=erro)

@app.route('/home')
def home():
    if not logado():
        return redirect('/')
    return render_template('home.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/responsaveis')
def responsaveis():
    if not logado():
        return redirect('/')
    termo = request.args.get('termo','')
    lista = database.listar_responsaveis(termo)
    return render_template('responsaveis.html',
                           responsaveis = lista, termo = termo)

@app.route('/responsaveis/editar/<int:id_responsavel>', methods = ['GET','POST'])
def editar_responsavel(id_responsavel):
    if not logado():
        return redirect('/')
    if request.method == 'POST':
        database.atualizar_responsavel(id_responsavel, request.form['nome'], request.form['cpf'], request.form['telefone'])
        return redirect('/responsaveis')
    responsavel = database.buscar_responsavel(id_responsavel)
    if responsavel is None:
        return redirect('/responsaveis')
    return render_template('editar_responsavel.html', responsavel = responsavel)

@app.route('/responsaveis/novo', methods=['GET', 'POST'])
def novo_responsavel():
    if not logado():
        return redirect('/')
    if request.method == 'POST':
        database.cadastrar_responsavel(
            request.form['nome'],
            request.form['cpf'],
            request.form['telefone']
        )
        return redirect('/responsaveis')
    return render_template('novo_responsavel.html')

@app.route('/responsaveis/excluir/<int:id_responsavel>', methods=['POST'])
def excluir_responsavel(id_responsavel):
    if not logado():
        return redirect('/')
    database.excluir_responsavel(id_responsavel)
    return redirect('/responsaveis')
    
@app.route('/aluno/novo', methods=['GET', 'POST'])
def novo_aluno():
    if not logado():
        return redirect('/')
    mensagem = None
    if request.method == 'POST':
        database.cadastrar_aluno(
            request.form['nome'],
            request.form['instrumento'],
            request.form['id_responsavel']
        )
        mensagem = 'Aluno cadastrado com sucesso.'
    lista = database.listar_responsaveis('')
    return render_template(
        'novo_aluno.html',
        responsaveis=lista,
        mensagem=mensagem
    )

@app.route('/aulas')
def aulas():
    if not logado():
        return redirect('/')
    lista = database.listar_aulas()
    return render_template('aulas.html', aulas=lista)

@app.route('/aulas/editar/<int:id_aula>', methods = ['GET', 'POST'])
def editar_aula(id_aula):
    if not logado():
        return redirect('/')
    if request.method == 'POST':
        data_hora = datetime.strptime(request.form['data_hora'], '%Y-%m-%dT%H:%M')
        database.atualizar_data_aula(id_aula, data_hora)
        return redirect('/aulas')
    aula = database.buscar_aula(id_aula)
    return render_template('editar_aula.html', aula=aula)

app.run(debug=True)