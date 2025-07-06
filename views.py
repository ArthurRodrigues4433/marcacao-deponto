from main import app
from flask import render_template,request,redirect,flash,session
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

    return render_template("areadofunci.html")


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