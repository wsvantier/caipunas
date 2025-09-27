from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Falta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(), nullable = False)
    dia = db.Column(db.Integer, nullable = False)
    mes = db.Column(db.String(), nullable = False)
    ano = db.Column(db.Integer, nullable = False)
    
    __table_args__ = (UniqueConstraint('nome','dia','mes','ano', name='nome_dia_mes_ano'),)