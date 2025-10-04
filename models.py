from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Falta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String, nullable = False)
    dia = db.Column(db.Integer, nullable = False)
    mes = db.Column(db.String, nullable = False)
    ano = db.Column(db.Integer, nullable = False)
    
    __table_args__ = (UniqueConstraint('nome','dia','mes','ano', name='nome_dia_mes_ano'),)


class Rm(db.Model):
    rm = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String, nullable = False)

class Sed(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    tipo = db.Column(db.String, nullable = False)
    serie = db.Column(db.String, nullable = False)
    num_chamada = db.Column(db.Integer, nullable = False)
    nome = db.Column(db.String, nullable = False)
    ra = db.Column(db.Integer, nullable = False)
    dig-ra = db.Column(db.Integer, nullable = False) 
    dt-nasc = db.Column(db.Date, nullable = False)
    inicio = db.Column(db.Date, nullable = False)
    fim = db.Column(db.Date, nullable = False)
    logradouro = db.Column(db.String, nullable = False)
    num_residencia = db.Column(db.String, nullable = False)
    bairro = db.Column(db.String, nullable = False)
    cidade = db.Column(db.String, nullable = False)
    
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String, nullable = False)
    turno = db.Column(db.Enum(['MANHA','TARDE']), nullable = False)
    transporte_id = db.Column(db.Integer, db.ForeignKey('Transporte.id'), nullable = True)
    
    tranporte = db.relationship('Transporte', back_populates='aluno')
    
class Transporte(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    desc = db.Column(db.String, nullable = False)
    
    alunos = db.relationship('Alunos', back_populates='transporte')