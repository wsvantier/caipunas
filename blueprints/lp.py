from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Turma
from dropmenu import turmas

lp_bp = Blueprint('lp', __name__, url_prefix='/lp')

@lp_bp.route('/')
def home():
    dados = turmas()
    return render_template('lp.html', turmas=dados)

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