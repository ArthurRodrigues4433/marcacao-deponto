from main import app
from flask import render_template,request,redirect,flash,session
from datetime import datetime
import json

# Essa é a rota principal do aplicativo
# Ela renderiza a página inicial do site
@app.route('/')
def homepage():
    return render_template("homepage.html")

# Essa rota renderiza a página de login do funcionário
# Ela é acessada quando o usuário visita a URL '/login'
@app.route('/areaFuncionario')
def area_funcionario():
    usuario_logado_id = session.get('email')

    with open('clientes.json', 'r') as cliente_json:
        dados = json.load(cliente_json)

        funcionario = next(
            (item for item in dados if item['email'] == usuario_logado_id),
            None
        )

        nome_funcionario = funcionario['nome'] if dados else "Funcionário"

   
    return render_template('areadofunci.html', name=nome_funcionario)


# Rota que recebe o clique do botão
@app.route('/marcar_ponto', methods=['POST'])
def marcar_ponto():
    # Obtém o horário atualagora = datetime.now()
    agora = datetime.now()
    data = agora.strftime('%Y/%m/%d')
    hora = agora.strftime('%H:%M:%S')

    # Salva num arquivo (opcional)
    with open('pontos.json', 'a') as f:
        f.write(f'Ponto marcado em: {data} {hora}\n')

    # Passa o valor para o template
    return render_template('areadofunci.html', horario_marcado=hora)



# Essa rota renderiza a página de login do cliente
# Ela é acessada quando o usuário visita a URL '/logincliente'
@app.route('/logincliente')
def login_cliente():
    return render_template("logincliente.html")


# Essa rota processa o login do cliente
# Ela é acessada quando o usuário envia o formulário de login do cliente
@app.route('/loginFuncionario', methods=['POST'])
def login_funcionario():
    email = request.form.get('emailFuncionario')
    senha = request.form.get('senhaFuncionario')
    with open('clientes.json', 'r') as cliente_json:
        listaDeFuncionarios = json.load(cliente_json)
        cont = 0
        for usuario in listaDeFuncionarios:
            cont += 1

            if email == usuario['email'] and senha == usuario['senha']:
                session['email'] = usuario['email']
                return redirect('/areaFuncionario')
            if cont >= len(listaDeFuncionarios):
                return redirect('/')
                  

# Essa rota renderiza a página de cadastro do cliente
# Ela é acessada quando o usuário visita a URL '/cadastro'
@app.route('/cadastro')
def cadastro():

    return render_template("cadastro.html")


# Essa rota processa o cadastro do funcionário
# Ela é acessada quando o usuário envia o formulário de cadastro do funcionário
@app.route('/cadastroFuncionario', methods=['POST'])
def cadastro_funcionario():
    nome  = request.form.get('nome_funcionario')
    email = request.form.get('emailfuncionario')
    senha = request.form.get('senhafuncionario')
    data = request.form.get('dataNascimento')

    with open('clientes.json', 'r') as cliente_json:
        listaDeFuncionarios = json.load(cliente_json)
        for usuario in listaDeFuncionarios:
            if usuario['email'] == email:
                return redirect('/')

    user = [
        {
            "nome": nome,
            "email": email,
            "senha": senha,
            "data": data

        }
    ]

    novalista = listaDeFuncionarios + user

    with open('clientes.json', 'w') as cliente_json:
        json.dump(novalista, cliente_json, indent=4)

    return redirect('/')