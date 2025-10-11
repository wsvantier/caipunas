from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import db, Transporte, Sed, Aluno

transporte_bp = Blueprint('transporte', __name__, url_prefix='/transporte')

@transporte_bp.route('/')
def home():
    return render_template('transporte.html')

@transporte_bp.route('/inserir', methods = ['POST'])
def inserir():
    linha = request.form['linhaForm']
    desc = request.form['descForm']

    nova_linha = Transporte(id=linha, desc=desc)
    db.session.add(nova_linha)
    db.session.commit()

    return redirect(url_for('transporte.home'))


@transporte_bp.route('/api/v1/dados')
def dados():
    query = Transporte.query.all()
    dados = [ {'id':x.id, 'desc':x.desc} for x in query ]
    return jsonify(dados)


@transporte_bp.route('/delete/<int:id>')
def excluir(id):
    busca = Transporte.query.get(id)

    db.session.delete(busca)
    db.session.commit()

    return redirect(url_for('transporte.home'))

@transporte_bp.route('/rotas')
def rotas():
    
    alunos = Sed.query.filter_by(situacao = 'ATIVO').order_by(Sed.nome)
    alunos = (
    db.session.query(
        Sed.nome,
        Sed.ra,
        Sed.dig_ra,
        Sed.logradouro,
        Sed.num_residencia,
        Aluno.turno
    )
    .join(Aluno, Sed.ra == Aluno.ra)
    .filter(Sed.situacao == 'ATIVO').order_by(Sed.nome)
    .all()
)


    return render_template('rotas.html', alunos=alunos)