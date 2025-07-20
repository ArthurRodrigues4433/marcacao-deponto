from main import app
from flask import render_template,request,redirect,flash,session,url_for
from collections import defaultdict
from datetime import datetime, timedelta
import json



# Essa é a rota principal do aplicativo
# Ela renderiza a página inicial do site
@app.route('/')
def homepage():
    return render_template("homepage.html")



# Essa rota renderiza a página de frequência do funcionário
# Ela é acessada quando o usuário visita a URL '/frequencia'
@app.route('/frequencia')
def frequencia():
    usuario_logado_id = session.get('email')
    
    if not usuario_logado_id:
        return redirect(url_for('login_cliente'))

    # Nome do funcionário
    with open('clientes.json', 'r') as cliente_json:
        dados = json.load(cliente_json)

        funcionario = next(
            (item for item in dados if item['email'] == usuario_logado_id),
            None
        )

        nome_funcionario = funcionario['nome'] if funcionario else "Funcionário"
    
    # Carrega pontos
    try:
        with open('pontos.json', 'r', encoding='utf-8') as f:
            dados_ponto = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados_ponto = {}

    registros = dados_ponto.get(usuario_logado_id, [])
    data_hoje = datetime.now().strftime('%Y/%m/%d')

    registros_hoje = [r for r in registros if r["data"] == data_hoje]

    return render_template(
        'frequencia.html',
        name=nome_funcionario,
        pontos_dia=registros_hoje
    )



# Essa rota renderiza a página de login do funcionário
# Ela é acessada quando o usuário visita a URL '/login'
@app.route('/areaFuncionario')
def area_funcionario():
    usuario_logado_id = session.get('email')

    # Nome do funcionário
    with open('clientes.json', 'r', encoding='utf-8') as cliente_json:
        dados = json.load(cliente_json)

        funcionario = next(
            (item for item in dados if item['email'] == usuario_logado_id),
            None
        )

        nome_funcionario = funcionario['nome'] if funcionario else "Funcionário"

    # Carrega os pontos
    try:
        with open('pontos.json', 'r', encoding='utf-8') as f:
            dados_ponto = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados_ponto = {}

    registros = dados_ponto.get(usuario_logado_id, [])
    agora = datetime.now()
    data_hoje = agora.strftime('%Y/%m/%d')

    # Verifica se deve iniciar um novo ciclo de registros
    if registros:
        ultimo_ponto = registros[-1]
        data_ultimo = datetime.strptime(f"{ultimo_ponto['data']} {ultimo_ponto['hora']}", "%Y/%m/%d %H:%M:%S")
        diff_horas = (agora - data_ultimo).total_seconds() / 3600

        # Se passar 11h descanso, considera novo ciclo (zera a exibição do dia)
        if diff_horas >= 11:
            registros_hoje = []
        else:
            registros_hoje = [r for r in registros if r["data"] == data_hoje]
    else:
        registros_hoje = []

    return render_template(
        'areadofunci.html',
        name=nome_funcionario,
        pontos_dia=registros_hoje
    )



# Essa rota processa o registro de ponto do funcionário
# ela verifica se o usuário está logado e registra o ponto, reinicia o ciclo quando passa as 11 horas depois do ultimo ponto
@app.route('/marcar_ponto', methods=['POST'])
def marcar_ponto():
    usuario_logado_id = session.get('email')
    if not usuario_logado_id:
        return redirect(url_for('login'))

    agora = datetime.now()
    data = agora.strftime('%Y/%m/%d')
    hora = agora.strftime('%H:%M:%S')

    try:
        with open('pontos.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}

    if usuario_logado_id not in dados:
        dados[usuario_logado_id] = []

    registros = dados[usuario_logado_id]

    # Verifica o último ponto
    if registros:
        ultimo_ponto = registros[-1]
        data_ultimo = datetime.strptime(f"{ultimo_ponto['data']} {ultimo_ponto['hora']}", "%Y/%m/%d %H:%M:%S")
        diff_horas = (agora - data_ultimo).total_seconds() / 3600

        # Se passou mais de 11 horas, inicia um novo "dia"
        if diff_horas >= 11:
            registros = []
            dados[usuario_logado_id] = registros

    # Pega registros do dia atual
    registros_hoje = [r for r in registros if r["data"] == data]

    tipos_ordem = ["entrada", "saida_intervalo", "volta_intervalo", "saida_final"]

    if len(registros_hoje) >= 4:
        tipo = "limite_atingido"
    else:
        tipo = tipos_ordem[len(registros_hoje)]
        novo_registro = {"data": data, "hora": hora, "tipo": tipo}
        registros.append(novo_registro)

        try:
            with open('pontos.json', 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except Exception as e:
            return f"Erro ao salvar o ponto: {str(e)}"

    return redirect(url_for('area_funcionario'))



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