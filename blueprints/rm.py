from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Rm

rm_bp = Blueprint('rm', __name__, url_prefix='/rm')

@rm_bp.route('/')
def home():
    return render_template('rm.html')

@rm_bp.route('/api/v1/dados')
def dados():
    pesquisa = Rm.query.all()
    dados = [{'rm':x.rm, 'nome':x.nome} for x in pesquisa]
    return jsonify(dados)

@rm_bp.route('/inserir', methods = ['POST'])
def add_rm():
    nome = request.form['nomeForm']

    novo_registro = Rm(nome = nome.upper())
    db.session.add(novo_registro)
    db.session.commit()

    return redirect(url_for('rm.home'))

@rm_bp.route('/excluir/<int:id>', methods = ['GET'])
def excluir(id):

    registro = Rm.query.get(id)
    db.session.delete(registro)
    db.session.commit()
    
    return redirect(url_for('rm.home'))
