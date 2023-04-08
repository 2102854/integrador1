# Projeto integrador 1
# Titulo do projeto
# Grupo 5
#
#

# Referencias
from flask import Flask, render_template
from sqlalchemy import Integer, String, Numeric, Date, Column, create_engine
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

#from typing import List
#from typing import Optional
#import sqlite3
#import datetime, os
#from flask_sqlalchemy import SQLAlchemy


# Mapeia o banco de dados
Base = declarative_base()
engine = create_engine('sqlite:///C:\\temp\\venv\\integrador.db', echo=True)
#engine = create_engine("sqlite:///integrador.db", echo=True)

#dir = os.path.dirname(os.path.abspath(__file__))
#db_file = "sqlite:///{}".format(os.path.join(dir,"integrador.db"))

# Configuração da aplicação
app = Flask(__name__)
#app.config['SECRET_KEY'] = '123'
#app.config['SQLALCHEMY_DATABASE_URI'] = db_file
#db = SQLAlchemy(app)

#############################
# Classes do banco de dados #
#############################

class Pais (Base):
    __tablename__ = "PAIS"

    pais_id = Column(Integer, primary_key=True)
    nome = Column(String(250))
    sigla = Column(String(3))

    def __repr__(self) -> str:
        return f"Pais(pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Estado (Base):
    __tablename__ = "ESTADO"

    estado_id = Column(Integer, primary_key=True)
    pais_id = Column(Integer)
    nome = Column(String(250))
    sigla = Column(String(3))

    def __repr__(self) -> str:
        return f"Estado(estado_id={self.estado_id!r}, pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Cidade (Base):
    __tablename__ = "CIDADE"

    cidade_id = Column(Integer, primary_key=True)
    estado_id = Column(Integer, nullable=False)
    nome = Column(String(250), nullable=False)
    distancia = Column(Numeric(10,2), nullable=False)
    valor_pedagio = Column(Numeric(10,2), nullable=False)
 
    def __repr__(self) -> str:
        return f"Cidade(cidade_id={self.cidade_id!r}, estado_id={self.estado_id!r}, nome={self.nome!r}, sigla={self.sigla!r}, distancia={self.distancia!r}, valor_pedagio={self.valor_pedagio!r} )"
    
    def __init__(self, nome):
        self.nome = nome 

class Endereco (Base):
    __tablename__ = "ENDERECO"

    endereco_id = Column(Integer, primary_key=True)
    cidade_id = Column(Integer, nullable=False)
    logradouro = Column(String(400), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(50), nullable=False)
 
    def __repr__(self) -> str:
        return f"Endereco(endereco_id={self.endereco_id!r},cidade_id={self.cidade_id!r}, logradouro={self.logradouro!r}, numero={self.numero!r}, complemento={self.complemento!r})"
    
    def __init__(self, logradouro):
        self.nome = logradouro 

class Veiculo (Base):
    __tablename__ = "VEICULO"

    veiculo_id = Column(Integer, primary_key=True)
    modelo = Column(String(250), nullable=False)
    placa = Column(String(20), nullable=False)
    capacidade = Column(Numeric(3), nullable=False)
    media_consumo = Column(Numeric(10,2), nullable=False)

    def __repr__(self) -> str:
        return f"Veiculo(veiculo_id={self.veiculo_id!r},modelo={self.modelo!r},placa={self.placa!r},capacidade={self.capacidade!r}, media_consumo={self.media_consumo!r})"
    
    def __init__(self, modelo):
        self.nome = modelo 
     
class Hospital (Base):
    __tablename__ = "HOSPITAL"

    hospital_id = Column(Integer, primary_key=True)
    endereco_id = Column(Integer, nullable=False)
    nome = Column(String(250), nullable=False)

    def __repr__(self) -> str:
        return f"Hospital(hospital_id={self.hospital_id!r}, nome={self.nome!r}, endereco_id={self.endereco_id!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Paciente (Base):
    __tablename__ = "PACIENTE"

    paciente_id = Column(Integer, primary_key=True)
    endereco_id = Column(Integer, nullable=False)
    nome = Column(String(250), nullable=False)
    data_nasc = Column(Date, nullable=False)
    tel1 = Column(Numeric(11), nullable=False)
    tel2 = Column(Numeric(11), nullable=True)

    def __repr__(self) -> str:
        return f"Paciente(paciente_id={self.paciente_id!r},endereco_id={self.endereco_id!r},nome={self.nome!r},data_nasc={self.data_nasc!r},tel1={self.tel1!r},tel2={self.tel2!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Responsavel (Base):
    __tablename__ = "TIPO_RESPONSAVEL"

    tipo_responsavel_id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Responsavel(tipo_Responsavel_id={self.tipo_responsavel_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Responsavel (Base):
    __tablename__ = "RESPONSAVEL"

    responsavel_id = Column(Integer, primary_key=True)
    tipo_responsavel_id = Column(Integer, nullable=False)
    nome = Column(String(250), nullable=False)
    numero_habilitacao = Column(String(50), nullable=False)
    carga_horaria = Column(Numeric(5, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Responsavel(responsavel_id={self.responsavel_id!r},tipo_responsavel={self.tipo_responsavel_id!r},nome={self.nome!r},numero_habilitacao={self.numero_habilitacao!r},carga_horaria={self.carga_horaria!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Doenca (Base):
    __tablename__ = "TIPO_DOENCA"

    tipo_doenca_id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Doenca(tipo_doenca_id={self.tipo_doenca_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Encaminhamento (Base):
    __tablename__ = "TIPO_ENCAMINHAMENTO"

    tipo_encaminhamento_id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Encaminhamento(tipo_encaminhamento_id={self.tipo_encaminhamento_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Remocao (Base):
    __tablename__ = "TIPO_REMOCAO"

    tipo_remocao_id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Remocao(tipo_remocao_id={self.tipo_remocao_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Agendamento (Base):
    __tablename__ = "AGENDAMENTO"

    agendamento_id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, nullable=False)
    tipo_encaminhamento_id = Column(Integer, nullable=False)
    tipo_doenca_id = Column(Integer, nullable=False)
    tipo_remocao_id = Column(Integer, nullable=False)
    hospital_id = Column(Integer, nullable=False)
    veiculo_id = Column(Integer, nullable=False)
    estado_geral_paciente = Column(String(500), nullable=False)
    data_remocao = Column(Date, nullable=False)
    saida_prevista = Column(Date, nullable=False)
    observacao = Column(String(500), nullable=False)
    custo_IFD = Column(Numeric(5, 2), nullable=False)
    custo_estadia = Column(Numeric(5, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Agendamento(agendamento_id={self.agendamento_id!r},paciente_id={self.paciente_id!r}),tipo_encaminhamento_id={self.tipo_encaminhamento_id!r}),tipo_doenca_id={self.tipo_doenca_id!r}),tipo_remocao_id={self.tipo_remocao_id!r}),hospital_id={self.hospital_id!r}),veiculo_id={self.veiculo_id!r}),estado_geral_paciente={self.estado_geral_paciente!r}),saida_prevista={self.saida_prevista!r}),observacao={self.observacao!r}),custo_IFD={self.paccusto_IFDiente_id!r}),custo_estadia={self.custo_estadia!r}),data_remocao={self.data_remocao!r})"
    
    def __init__(self, agendamento_id):
        self.agendamento_id = agendamento_id 

class Agendamento_Responsavel (Base):
    __tablename__ = "AGENDAMENTO_RESPONSAVEL"

    agendamento_responsavel_id = Column(Integer, primary_key=True)
    agendamento_id = Column(Integer, nullable=False)
    responsavel_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Agendamento_Responsavel(agendamento_responsavel_id={self.agendamento_responsavel_id!r},agendamento_id={self.agendamento_id!r}),responsavel_id={self.responsavel_id!r})"
    
    def __init__(self, agendamento_responsavel_id):
        self.agendamento_responsavel_id = agendamento_responsavel_id 

#página inicial
@app.route("/")
def index():
    return render_template('index.html')