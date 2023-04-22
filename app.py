# Projeto integrador 1
# Titulo do projeto
# Grupo 5

# Referencias
import locale
from flask import Flask, render_template, url_for, flash, redirect, request
from sqlalchemy import  Column, create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy.sql.operators import ilike_op

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

# Mapeia o banco de dados
Base = declarative_base()
engine = create_engine('sqlite:///C:\\temp\\venv\\integrador.db', echo=True)
session = Session(engine)
#engine = create_engine("sqlite:///integrador.db", echo=True)

# Configuração da aplicação
app = Flask(__name__)
app.debug = True

#############################
# Classes do banco de dados #
#############################

class Pais (Base):
    __tablename__ = "PAIS"

    pais_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250))
    sigla = Column(TEXT(3))

    def __repr__(self) -> str:
        return f"Pais(pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    def __init__(self, nome, sigla):
        self.nome = nome 
        self.sigla = sigla

class Estado (Base):
    __tablename__ = "ESTADO"

    estado_id = Column(INTEGER, primary_key=True)
    pais_id = Column(INTEGER)
    nome = Column(TEXT(250))
    sigla = Column(TEXT(3))

    def __repr__(self) -> str:
        return f"Estado(estado_id={self.estado_id!r}, pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    def __init__(self, pais_id, nome, sigla):
        self.pais_id = pais_id
        self.nome = nome
        self.sigla = sigla

class Cidade (Base):
    __tablename__ = "CIDADE"

    cidade_id = Column(INTEGER, primary_key=True)
    estado_id = Column(INTEGER, nullable=False)
    nome = Column(TEXT(250), nullable=False)
    distancia_km = Column(NUMERIC(10,2), nullable=False)
    valor_pedagio = Column(NUMERIC(10,2), nullable=False)
 
    def __repr__(self) -> str:
        return f"Cidade(cidade_id={self.cidade_id!r}, estado_id={self.estado_id!r}, nome={self.nome!r}, distancia_km={self.distancia_km!r}, valor_pedagio={self.valor_pedagio!r} )"
    
    def __init__(self, estado_id, nome, distancia_km, valor_pedagio):
        self.estado_id = estado_id
        self.nome = nome 
        self.distancia_km = distancia_km
        self.valor_pedagio = valor_pedagio

class Endereco (Base):
    __tablename__ = "ENDERECO"

    endereco_id = Column(INTEGER, primary_key=True)
    cidade_id = Column(INTEGER, nullable=False)
    logradouro = Column(TEXT(400), nullable=False)
    numero = Column(TEXT(20), nullable=False)
    complemento = Column(TEXT(50), nullable=False)
 
    def __repr__(self) -> str:
        return f"Endereco(endereco_id={self.endereco_id!r},cidade_id={self.cidade_id!r}, logradouro={self.logradouro!r}, numero={self.numero!r}, complemento={self.complemento!r})"
    
    def __init__(self, logradouro):
        self.nome = logradouro 

class Veiculo (Base):
    __tablename__ = "VEICULO"

    veiculo_id = Column(INTEGER, primary_key=True)
    modelo = Column(TEXT(250), nullable=False)
    placa = Column(TEXT(20), nullable=False)
    capacidade = Column(NUMERIC(3), nullable=False)
    media_consumo = Column(NUMERIC(10,2), nullable=False)

    def __repr__(self) -> str:
        return f"Veiculo(veiculo_id={self.veiculo_id!r},modelo={self.modelo!r},placa={self.placa!r},capacidade={self.capacidade!r}, media_consumo={self.media_consumo!r})"
    
    def __init__(self, modelo):
        self.nome = modelo 
     
class Hospital (Base):
    __tablename__ = "HOSPITAL"

    hospital_id = Column(INTEGER, primary_key=True)
    endereco_id = Column(INTEGER, nullable=False)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Hospital(hospital_id={self.hospital_id!r}, nome={self.nome!r}, endereco_id={self.endereco_id!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Paciente (Base):
    __tablename__ = "PACIENTE"

    paciente_id = Column(INTEGER, primary_key=True)
    cidade_id = Column(INTEGER, nullable=False)
    nome = Column(TEXT(250), nullable=False)
    data_nasc = Column(TEXT(10), nullable=False)
    tel_1 = Column(TEXT(11), nullable=False)
    tel_2 = Column(TEXT(11), nullable=True)
    logradouro = Column(TEXT(400), nullable=False)
    numero = Column(TEXT(20), nullable=False)
    complemento = Column(TEXT(50), nullable=False)
    cep = Column(TEXT(10), nullable=False)

    def __repr__(self) -> str:
        return f"Paciente(paciente_id={self.paciente_id!r},cidade_id={self.cidade_id!r},nome={self.nome!r},data_nasc={self.data_nasc!r},tel_1={self.tel_1!r},tel_2={self.tel_2!r},logradouro={self.logradouro!r}, numero={self.numero!r}, complemento={self.complemento!r}, cep={self.cep!r})"
    
    def __init__(self, cidade_id, nome, data_nasc, tel_1, tel_2, logradouro, numero, complemento, cep):
        self.cidade_id = cidade_id
        self.nome = nome 
        self.data_nasc = data_nasc
        self.tel_1 = tel_1
        self.tel_2 = tel_2
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cep = cep

class Tipo_Responsavel (Base):
    __tablename__ = "TIPO_RESPONSAVEL"

    tipo_responsavel_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Responsavel(tipo_Responsavel_id={self.tipo_responsavel_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Responsavel (Base):
    __tablename__ = "RESPONSAVEL"

    responsavel_id = Column(INTEGER, primary_key=True)
    tipo_responsavel_id = Column(INTEGER, nullable=False)
    nome = Column(TEXT(250), nullable=False)
    numero_habilitacao = Column(TEXT(50), nullable=False)
    carga_horaria = Column(NUMERIC(5, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Responsavel(responsavel_id={self.responsavel_id!r},tipo_responsavel={self.tipo_responsavel_id!r},nome={self.nome!r},numero_habilitacao={self.numero_habilitacao!r},carga_horaria={self.carga_horaria!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Doenca (Base):
    __tablename__ = "TIPO_DOENCA"

    tipo_doenca_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Doenca(tipo_doenca_id={self.tipo_doenca_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Encaminhamento (Base):
    __tablename__ = "TIPO_ENCAMINHAMENTO"

    tipo_encaminhamento_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Encaminhamento(tipo_encaminhamento_id={self.tipo_encaminhamento_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Remocao (Base):
    __tablename__ = "TIPO_REMOCAO"

    tipo_remocao_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Remocao(tipo_remocao_id={self.tipo_remocao_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Agendamento (Base):
    __tablename__ = "AGENDAMENTO"

    agendamento_id = Column(INTEGER, primary_key=True)
    paciente_id = Column(INTEGER, nullable=False)
    tipo_encaminhamento_id = Column(INTEGER, nullable=False)
    tipo_doenca_id = Column(INTEGER, nullable=False)
    tipo_remocao_id = Column(INTEGER, nullable=False)
    hospital_id = Column(INTEGER, nullable=False)
    veiculo_id = Column(INTEGER, nullable=False)
    estado_geral_paciente = Column(TEXT(500), nullable=False)
    data_remocao = Column(DATE, nullable=False)
    saida_prevista = Column(DATE, nullable=False)
    observacao = Column(TEXT(500), nullable=False)
    custo_IFD = Column(NUMERIC(5, 2), nullable=False)
    custo_estadia = Column(NUMERIC(5, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Agendamento(agendamento_id={self.agendamento_id!r},paciente_id={self.paciente_id!r}),tipo_encaminhamento_id={self.tipo_encaminhamento_id!r}),tipo_doenca_id={self.tipo_doenca_id!r}),tipo_remocao_id={self.tipo_remocao_id!r}),hospital_id={self.hospital_id!r}),veiculo_id={self.veiculo_id!r}),estado_geral_paciente={self.estado_geral_paciente!r}),saida_prevista={self.saida_prevista!r}),observacao={self.observacao!r}),custo_IFD={self.paccusto_IFDiente_id!r}),custo_estadia={self.custo_estadia!r}),data_remocao={self.data_remocao!r})"
    
    def __init__(self, agendamento_id):
        self.agendamento_id = agendamento_id 

class Agendamento_Responsavel (Base):
    __tablename__ = "AGENDAMENTO_RESPONSAVEL"

    agendamento_responsavel_id = Column(INTEGER, primary_key=True)
    agendamento_id = Column(INTEGER, nullable=False)
    responsavel_id = Column(INTEGER, nullable=False)

    def __repr__(self) -> str:
        return f"Agendamento_Responsavel(agendamento_responsavel_id={self.agendamento_responsavel_id!r},agendamento_id={self.agendamento_id!r}),responsavel_id={self.responsavel_id!r})"
    
    def __init__(self, agendamento_responsavel_id):
        self.agendamento_responsavel_id = agendamento_responsavel_id 

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
    sql = select(Pais)
    return render_template('paises.html',paises=session.scalars(sql))

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
    sql = session.query(Estado, Pais).join(Estado, Estado.pais_id == Pais.pais_id).all()
    return render_template('estados.html', results=sql)

#Abre a página de cidades
@app.route("/cidades")
def cidades():    
    sql = session.query(Cidade, Estado).join(Estado, Cidade.estado_id == Estado.estado_id).all()
    return render_template('cidades.html', results=sql)

#Abre a página de pacientes
@app.route("/pacientes")
def pacientes():
    #http://127.0.0.1:5000/pacientes?nome=rosa
    nome = request.args.get('nome', default = '', type = str)
    print(nome)
    if nome == '':    
        sql = session.query(Paciente, Cidade).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()        
    else:
        sql = session.query(Paciente, Cidade).filter(ilike_op(Paciente.nome,f'%{nome}%')).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()
    return render_template('pacientes.html', results=sql)

#Abre a página de cadastro de pacientes
@app.route('/pacientes/novo/', methods=('GET', 'POST'))
def pacientes_add():
    if request.method == 'POST':      
        
        novoPaciente = Paciente (
            request.form['cidade'], 
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
    