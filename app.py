from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para usar a sessão

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
senha = ""

@app.route('/login', methods=['GET', 'POST'])
def login_sistema():
    global senha
    mensagem = ""
    if request.method == 'POST':
        opcao = request.form['opcao']
        if opcao == "1":
            senha_escolhida = request.form['senha_escolhida']
            senha_confirmada = request.form['senha_confirmada']
            if senha_escolhida == senha_confirmada:
                senha = senha_escolhida
                mensagem = "Senha cadastrada com sucesso!"
            else:
                mensagem = "Senhas não coincidem!"
        elif opcao == "2":
            possivel_senha = request.form['senha_login']
            if senha == possivel_senha:
                mensagem = "Sucesso ao fazer login!"
            else:
                mensagem = "Senha inválida!"
    return render_template('questão-20/login.html', mensagem=mensagem)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
