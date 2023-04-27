# Projeto integrador 1
# Titulo do projeto
# Grupo 5

# Referencias
import locale
from models import Pais, Estado, Cidade, Endereco, Veiculo, Hospital, Paciente, Tipo_Responsavel, Responsavel, Tipo_Doenca, Tipo_Encaminhamento, Tipo_Remocao, Agendamento, Agendamento_Responsavel
from flask import Flask, render_template, url_for, flash, redirect, request
from flask import jsonify
from sqlalchemy import create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op


# Cria o dicionário da Classe para retorno json
def dict_helper(objlist):
    result = [item.obj_to_dict() for item in objlist]
    return result

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

# Mapeia o banco de dados
#Base = declarative_base()
engine = create_engine('sqlite:///C:\\temp\\venv\\integrador.db', echo=True)
session = Session(engine)
#engine = create_engine("sqlite:///integrador.db", echo=True)

# Configuração da aplicação
app = Flask(__name__)
app.debug = True

#página inicial
@app.route("/")
def index():

    #Conta o número de Hospitais cadastrados
    num_hospitais = session.query(func.count(Hospital.hospital_id)).scalar()
    num_pacientes = session.query(func.count(Paciente.paciente_id)).scalar()
    num_agendamentos = session.query(func.count(Agendamento.agendamento_id)).scalar()

    #Carrega a lista de hospitais 
    #No máximo 4 nomes
    sql = select(Hospital).order_by(Hospital.hospital_id.desc())
    hospitais = session.scalars(sql)

    lt_hospitais = []
    num_hos = 0

    for hospital in hospitais:
        num_hos = num_hos + 1
        
        lt_hospitais.append(hospital.nome)
        if num_hos > 3:
            break

    if num_hos < 4:
        for x in range(4 - num_hos):
            lt_hospitais.append("..")    

    #Carrega a lista de pacientes 
    #No máximo 4 nomes

    sql = select(Paciente).order_by(Paciente.paciente_id.desc())
    pacientes = session.scalars(sql)   
    
    lt_pacientes = []
    num_pac = 0
    
    for paciente in pacientes:
        num_pac = num_pac + 1
        
        lt_pacientes.append(paciente.nome)
        if num_pac > 3:
            break

    if num_pac < 4:
        for x in range(4 - num_pac):
            lt_pacientes.append("..")

    return render_template('index.html', hospitais=num_hospitais, pacientes=num_pacientes, agendamentos=num_agendamentos, lt_hospitais=lt_hospitais, lt_pacientes=lt_pacientes)

#Abre a página de países
@app.route("/paises")
def paises():
    nome = request.args.get('nome', default = '', type = str)
    if nome == '':    
        paises = session.query(Pais).all()        
    else:
        paises = session.query(Pais).filter(ilike_op(Pais.nome,f'%{nome}%')).all()
    return render_template('paises.html',paises=paises)

#Abre a página de cadastro de países
@app.route('/paises/novo/', methods=('GET', 'POST'))
def pais_add():
    if request.method == 'POST':

        novoPais = Pais(request.form['nome'], request.form['sigla'])
        session.add(novoPais)        
        session.commit()        
        return redirect(url_for('paises'))    
    
    else:
        return render_template('form_cad_pais.html')
    
#Abre a página de edição de países    
@app.route('/paises/editar/<pais_id>', methods=('GET', 'POST'))
def pais_edit(pais_id):
    
    if request.method == 'POST':
        # Executa a alteração do país
        sql = select(Pais).where(Pais.pais_id == pais_id)
        result = session.scalars(sql).one()
        result.nome = request.form['nome']
        result.sigla = request.form['sigla']        
        session.commit() 

        # Volta para a página de países
        return redirect(url_for('paises'))
    else:

        # Pesquisa pelo Id do pais
        sql = select(Pais).where(Pais.pais_id == pais_id)
        result = session.scalars(sql).one()
        return render_template('form_edt_pais.html',pais_id=pais_id, nome=result.nome, sigla=result.sigla )
    
#Abre a página de estados
@app.route("/estados")
def estados():    
    nome = request.args.get('nome', default = '', type = str)
    if nome == '':    
        sql = session.query(Estado, Pais).join(Estado, Estado.pais_id == Pais.pais_id).all()        
    else:
        sql = session.query(Estado, Pais).filter(ilike_op(Estado.nome,f'%{nome}%')).join(Estado, Estado.pais_id == Pais.pais_id).all()
    return render_template('estados.html', results=sql)

#Abre a página de cidades
@app.route("/cidades")
def cidades():    
    #sql = session.query(Cidade, Estado).join(Estado, Cidade.estado_id == Estado.estado_id).all()
    nome = request.args.get('nome', default = '', type = str)
    if nome == '':    
        sql = session.query(Cidade, Estado).join(Estado, Cidade.estado_id == Estado.estado_id).all()       
    else:
        sql = session.query(Cidade, Estado).filter(ilike_op(Cidade.nome,f'%{nome}%')).join(Estado, Cidade.estado_id == Estado.estado_id).all()  
    return render_template('cidades.html', results=sql)

#Abre a página de pacientes
@app.route("/pacientes")
def pacientes():
    #http://127.0.0.1:5000/pacientes?nome=rosa
    nome = request.args.get('nome', default = '', type = str)
    if nome == '':    
        sql = session.query(Paciente, Cidade).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()        
    else:
        sql = session.query(Paciente, Cidade).filter(ilike_op(Paciente.nome,f'%{nome}%')).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()
    return render_template('pacientes.html', results=sql)

#https://medium.com/@mhd0416/flask-sqlalchemy-object-to-json-84c515d3c11c
# Retorna a lista de pacientes em formato json
@app.route("/pacientes/lst")
def getPacientes():
    sql = session.query(Paciente).all()
    p = dict_helper(sql) 
    return jsonify(pacientes = p)

#Abre a página de cadastro de pacientes
@app.route('/pacientes/novo/', methods=('GET', 'POST'))
def pacientes_add():
    if request.method == 'POST':      
        
        novoPaciente = Paciente (
            request.form['cidade'],
            request.form['hygia'],
            request.form['nome'].upper(), 
            request.form['data_nasc'], 
            request.form['tel_1'], 
            request.form['tel_2'], 
            request.form['logradouro'].upper(), 
            request.form['numero'], 
            request.form['complemento'].upper(), 
            request.form['cep']
        )
        session.add(novoPaciente)        
        session.commit()        
        return redirect(url_for('pacientes'))    
    
    else:
        cidades = session.query(Cidade).all()
        return render_template('form_cad_paciente.html', cidades=cidades)
    
#Abre a página de edição de pacientes
@app.route('/pacientes/editar/<paciente_id>', methods=('GET', 'POST'))
def pacientes_edit(paciente_id):
    if request.method == 'POST':      
        sql = select(Paciente).where(Paciente.paciente_id == paciente_id)
        paciente = session.scalars(sql).one()

        paciente.cidade_id = request.form['cidade']
        paciente.hygia = request.form['hygia']
        paciente.nome = request.form['nome'].upper()
        paciente.data_nasc = request.form['data_nasc'] 
        paciente.tel_1 = request.form['tel_1']
        paciente.tel_2 = request.form['tel_2'] 
        paciente.logradouro = request.form['logradouro'].upper() 
        paciente.numero = request.form['numero']
        paciente.complemento = request.form['complemento'].upper()
        paciente.cep = request.form['cep']     
        session.commit()

        return redirect(url_for('pacientes'))    
    
    else:
        cidades = session.query(Cidade).all()
        sql = select(Paciente).where(Paciente.paciente_id == paciente_id)
        paciente = session.scalars(sql).one()
        return render_template('form_edit_paciente.html', cidades=cidades, paciente = paciente)
    
    #Abre a página de pacientes
@app.route("/agendamentos")
def agendamentos():
    nome = request.args.get('nome', default = '', type = str)
    #if nome == '':    
    sql = session.query(Agendamento, Paciente ).join(Paciente, Agendamento.paciente_id == Paciente.paciente_id).all()        
    #else:
    #    sql = session.query(Paciente, Cidade).filter(ilike_op(Paciente.nome,f'%{nome}%')).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()
    return render_template('agendamentos.html', results=sql)

#Abre a página de agendamento de pacientes
@app.route('/agendamentos/novo/', methods=('GET', 'POST'))
def agendamentos_add():
    if request.method == 'POST':      
        
        novoPaciente = Paciente (
            request.form['cidade'],
            request.form['hygia'],
            request.form['nome'].upper(), 
            request.form['data_nasc'], 
            request.form['tel_1'], 
            request.form['tel_2'], 
            request.form['logradouro'].upper(), 
            request.form['numero'], 
            request.form['complemento'].upper(), 
            request.form['cep']
        )
        session.add(novoPaciente)        
        session.commit()        
        return redirect(url_for('pacientes'))    
    
    else:
        cidades = session.query(Cidade).all()
        return render_template('form_cad_agendamento.html', cidades=cidades)
    

#https://bootstrap-table.com/