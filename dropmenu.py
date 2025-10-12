from models import db, Turma, Transporte

def turmas() -> list:
    turmas = Turma.query.all()
    dados = [{'id':x.id,'desc':x.desc} for x in turmas]
    
    return dados

def rotas() -> list:
    rotas = Transporte.query.all()
    dados = [{'id': x.id, 'desc': x.desc} for x in rotas]
    return dados
