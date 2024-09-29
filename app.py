from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Função para verificar maioridade
@app.route('/maioridade', methods=['GET', 'POST'])
def verificar_maioridade():
    if request.method == 'POST':
        idade = int(request.form['idade'])
        if idade >= 18:
            resultado = f"Você tem {idade} anos, portanto é MAIOR de idade."
        else:
            resultado = f"Você tem {idade} anos, portanto é MENOR de idade."
        return render_template('maioridade.html', resultado=resultado)
    return render_template('maioridade.html')

# Função para cadastrar alunos
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_alunos():
    cadastro = {}
    if request.method == 'POST':
        nome = request.form['nome']
        idade = int(request.form['idade'])
        nota = float(request.form['nota'])
        cadastro[nome] = {'Idade': idade, 'Nota': nota}
        return render_template('cadastro.html', cadastro=cadastro)
    return render_template('cadastro.html')

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
    return render_template('login.html', mensagem=mensagem)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
