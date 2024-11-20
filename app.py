from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import string

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para usar a sessão
app.secret_key = 'some_secret_key'  # Necessário para usar flash

# Dicionário global para o sistema bancário
usuarios = {}

# Questão 1: Sistema Bancário
@app.route('/banco', methods=['GET', 'POST'])
def sistema_bancario():
    mensagem = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        operacao = request.form['operacao']
        valor = float(request.form['valor']) if request.form.get('valor') else 0

        if usuario not in usuarios:
            usuarios[usuario] = 0  # Criando conta para o usuário automaticamente

        if operacao == 'depositar':
            usuarios[usuario] += valor
            mensagem = f"Depósito de R$ {valor:.2f} realizado com sucesso!"
        elif operacao == 'sacar':
            if usuarios[usuario] >= valor:
                usuarios[usuario] -= valor
                mensagem = f"Saque de R$ {valor:.2f} realizado com sucesso!"
            else:
                mensagem = "Saldo insuficiente para saque."
        elif operacao == 'saldo':
            mensagem = f"Saldo de {usuario}: R$ {usuarios[usuario]:.2f}"

    return render_template('me-questão-03/sistema_bancario.html', mensagem=mensagem, usuarios=usuarios)

# Questão 2: Gerador de Senhas Aleatórias
@app.route('/gerar_senha', methods=['GET', 'POST'])
def gerar_senha():
    senha_gerada = ""
    if request.method == 'POST':
        tamanho = int(request.form['tamanho'])
        incluir_maiusculas = 'maiusculas' in request.form
        incluir_minusculas = 'minusculas' in request.form
        incluir_numeros = 'numeros' in request.form
        incluir_especiais = 'especiais' in request.form

        caracteres = ""
        if incluir_maiusculas:
            caracteres += string.ascii_uppercase
        if incluir_minusculas:
            caracteres += string.ascii_lowercase
        if incluir_numeros:
            caracteres += string.digits
        if incluir_especiais:
            caracteres += string.punctuation

        if caracteres:
            senha_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho))

    return render_template('me-questão-05/gerador_senha.html', senha=senha_gerada)

# Função para verificar maioridade
@app.route('/maioridade', methods=['GET', 'POST'])
def verificar_maioridade():
    if request.method == 'POST':
        idade = int(request.form['idade'])
        if idade >= 18:
            resultado = f"Você tem {idade} anos, portanto é MAIOR de idade."
        else:
            resultado = f"Você tem {idade} anos, portanto é MENOR de idade."
        return render_template('questão-03/maioridade.html', resultado=resultado)
    return render_template('questão-03/maioridade.html')

# Página inicial para perguntar quantos alunos serão cadastrados
@app.route('/quantos_alunos', methods=['GET', 'POST'])
def quantos_alunos():
    if request.method == 'POST':
        numero_alunos = int(request.form['numero_alunos'])
        return redirect(url_for('cadastro_alunos', num_alunos=numero_alunos))
    return render_template('questão-11/quantos_alunos.html')

# Função para cadastrar alunos
@app.route('/cadastro/<int:num_alunos>', methods=['GET', 'POST'])
def cadastro_alunos(num_alunos):
    cadastro = {}
    if request.method == 'POST':
        for i in range(num_alunos):
            nome = request.form[f'nome {i}']
            idade = int(request.form[f'idade {i}'])
            nota = float(request.form[f'nota {i}'])
            cadastro[nome] = {'Idade': idade, 'Nota': nota}

        # Salvando os cadastros na sessão
        session['cadastro'] = cadastro
        return redirect(url_for('exibir_cadastro'))
    return render_template('questão-11/cadastro_form.html', num_alunos=num_alunos)

# Função para exibir cadastros
@app.route('/cadastro/exibir', methods=['GET'])
def exibir_cadastro():
    # Pegando os cadastros da sessão
    cadastro = session.get('cadastro', {})
    return render_template('questão-11/exibir_cadastro.html', cadastro=cadastro)

# Funções para sistema de login
# Variável global para armazenar a senha
senha = ""
# Página inicial com opções
@app.route('/login')
def login_sistema():
    return render_template('questão-20/login.html')

# Página para cadastrar senha
@app.route('/cadastrar_senha', methods=['GET', 'POST'])
def pagina_cadastrar_senha():
    global senha
    mensagem = ""
    if request.method == 'POST':
        senha_escolhida = request.form['senha_escolhida']
        senha_confirmada = request.form['senha_confirmada']
        if senha_escolhida == senha_confirmada:
            senha = senha_escolhida
            mensagem = "Senha cadastrada com sucesso!"
        else:
            mensagem = "Senhas não coincidem!"
        return render_template('questão-20/cadastrar_senha.html', mensagem=mensagem)
    return render_template('questão-20/cadastrar_senha.html')

# Página para fazer login
@app.route('/fazer_login', methods=['GET', 'POST'])
def pagina_fazer_login():
    global senha
    mensagem = ""
    if request.method == 'POST':
        if senha == "":
            mensagem = "(!) Nenhuma senha foi cadastrada...\n\n Clique em voltar para cadastrar uma senha primeiro."
        else:
            possivel_senha = request.form['senha_login']
            if senha == possivel_senha:
                mensagem = "Login autenticado com SUCESSO!"
            else:
                mensagem = "Senha inválida!"
        return render_template('questão-20/fazer_login.html', mensagem=mensagem)
    return render_template('questão-20/fazer_login.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
