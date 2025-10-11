from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Turma, Sed, Aluno
import pandas as pd
from datetime import datetime
from dropmenu import turmas, rotas

lp_bp = Blueprint('lp', __name__, url_prefix='/lp')

@lp_bp.route('/')
def home():
    dados = turmas()
    return render_template('lp.html', turmas=dados, transportes=rotas())

@lp_bp.route('/inserir', methods=['POST'])
def add_turma():
    codigo = request.form['codigoForm']
    turma = request.form['turmaForm']
    
    busca = Turma.query.filter_by(id = codigo).first()
    
    if not busca:
        nova_turma = Turma(id = codigo, desc = turma)
        db.session.add(nova_turma)
        db.session.commit()
        
    return redirect(url_for('lp.home'))

@lp_bp.route('/api/v1/dados')
def dados():
    
    query = Turma.query.all()
    dados = [{'id':x.id, 'desc':x.desc} for x in query]
    
    return jsonify(dados)


@lp_bp.route('/delete/<int:id>')
def excluir(id):
    busca = Turma.query.get(id)
    db.session.delete(busca)
    db.session.commit()
    
    return redirect(url_for('lp.home'))


@lp_bp.route('/turma/<int:id>')
def classe(id):
    
    busca = Turma.query.get(id)
    dados = Sed.query.filter_by(turma_id = id).all()
    return render_template('turma.html',dados=dados, turma=busca.desc, id=busca.id, turmas=turmas(), transportes=rotas())

@lp_bp.route('/upload/<int:id>', methods = ['POST'])
def upload(id):
    
    arq = request.files['arq']
    periodo = request.form['periodo']
    
    df = pd.read_csv(arq, sep = ';', skiprows = 2)
    dados = df[['Tipo de Ensino','Série','Nº','Nome do Aluno','RA','Dig. RA','Data de Nascimento','Data Início Matrícula','Data Fim Matrícula','Situação','Endereço do Aluno']]
    colunas = ['Logradouro','Numero','Bairro','Cidade','Estado']
    dados[colunas] = dados['Endereço do Aluno'].str.replace(',',' -').str.split(' - ', expand = True)
    dados.drop(columns=['Endereço do Aluno'], inplace = True)
    
    Sed.query.filter_by(turma_id=id).delete()

    
    for x in dados.values:
        sed = Sed(tipo=x[0],
                    serie=x[1],
                    num_chamada = x[2],
                    nome = x[3],
                    ra = x[4],
                    dig_ra = x[5],
                    dt_nasc = datetime.strptime(x[6],'%d/%m/%Y').date(),
                    inicio = datetime.strptime(x[7],'%d/%m/%Y').date(),
                    fim = datetime.strptime(x[8],'%d/%m/%Y').date(),
                    situacao = x[9],
                    logradouro = x[10],
                    num_residencia = x[11],
                    bairro = x[12],
                    cidade = x[13],
                    turma_id = id )
        
        if not Aluno.query.filter_by(ra=x[4]).first():
            if x[9] == 'ATIVO':
                aluno= Aluno(nome = x[3],
                            ra = x[4],
                            turno = periodo)
                db.session.add(aluno)
        else:
            aluno = Aluno.query.filter_by(ra=x[4]).first()
            aluno.turno = periodo
        db.session.add(sed)
        
    
    db.session.commit()
    return redirect(f'/lp/turma/{id}')