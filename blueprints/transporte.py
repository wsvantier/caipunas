from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import db, Transporte, Sed, Aluno

transporte_bp = Blueprint('transporte', __name__, url_prefix='/transporte')

@transporte_bp.route('/')
def home():
    alunos = (
    db.session.query(
        Aluno.id,
        Sed.nome,
        Sed.logradouro,
        Sed.num_residencia,
        Aluno.turno,
        Aluno.transporte_id
    )
    .join(Aluno, Sed.ra == Aluno.ra)
    .filter(Sed.situacao == 'ATIVO')
    .order_by(Aluno.turno, Sed.nome)
    .all()

    )
    return render_template('transporte.html', alunos=alunos)

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

@transporte_bp.route('/rotas/<int:id>')
def rotas(id):
    
    rota = Transporte.query.get(id)
    
    manha = (
    db.session.query(
        Sed.nome,
        Sed.ra,
        Sed.dig_ra,
        Sed.logradouro,
        Sed.num_residencia,
        Aluno.turno,
        Aluno.transporte_id
    )
    .join(Aluno, Sed.ra == Aluno.ra)
    .filter(
        (Sed.situacao == 'ATIVO') &
        (Aluno.transporte_id == id) &
        (Aluno.turno == 'MANHA')
    ).order_by(Sed.nome)
    .all()
)

    tarde = (
        db.session.query(
            Sed.nome,
            Sed.ra,
            Sed.dig_ra,
            Sed.logradouro,
            Sed.num_residencia,
            Aluno.turno,
            Aluno.transporte_id
        )
        .join(Aluno, Sed.ra == Aluno.ra)
        .filter(
            (Sed.situacao == 'ATIVO') &
            (Aluno.transporte_id == id) &
            (Aluno.turno == 'TARDE') 
        ).order_by(Sed.nome)
        .all()
    )

    return render_template('rotas.html', manha=manha, tarde=tarde, rota=rota.desc)

@transporte_bp.route('/update', methods=['POST'])
def update_rota():
    alunos = Aluno.query.all()
    for aluno in alunos:
        rota_id = request.form.get(f'rota_{aluno.id}')
        if rota_id:
            aluno.transporte_id = rota_id
    db.session.commit()
    return redirect(url_for('transporte.home'))
    