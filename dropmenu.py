from models import db, Turma, Transporte

def turmas() -> list:
    turmas = Turma.query.all()
    dados = [x.desc for x in turmas]
    
    return dados