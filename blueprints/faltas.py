from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import calendar
from datetime import datetime
from models import db,Falta
from dropmenu import turmas

faltas_bp = Blueprint('faltas', __name__, url_prefix='/faltas')


@faltas_bp.route('/')
def home(): 
    hoje = datetime.now()
    dia = hoje.day
    mes = hoje.month
    ano = hoje.year

    cal = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdayscalendar(ano,mes)

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro','Outubro','Novembro','Dezembro']
    meses_futuros= [x for x in meses if meses.index(x) >= mes-1]
   
    salas = turmas()
    return render_template('faltas.html', semanas = semanas, mes = meses[datetime.now().month-1], ano = ano, meses = meses_futuros, dia = dia, turmas=salas)


@faltas_bp.route('/inserir', methods = ['POST'])
def inserir_falta():
    if request.method == 'POST':
        nomeForm = request.form['nomeForm']
        diaForm = request.form['diaForm']
        mesForm = request.form['mesSelect']

        nova_falta = Falta(nome=nomeForm, dia=diaForm, mes=mesForm, ano=datetime.now().year )
        db.session.add(nova_falta)
        db.session.commit()

        return redirect(url_for('faltas.home'))
    

@faltas_bp.route('/api/v1/faltas_mes')
def faltas_mes():
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro','Outubro','Novembro','Dezembro']
    mes_atual = meses[datetime.now().month-1]
    ano_atual = datetime.now().year

    query = Falta.query.filter_by(ano=ano_atual, mes=mes_atual)
    dados = [{'id':x.id, 'nome':x.nome, 'dia':x.dia , 'ano':x.ano, 'mes':x.mes } for x in query]

    return jsonify(dados)

@faltas_bp.route('/excluir/<int:id>')
def excluir_falta(id):

    query = Falta.query.get(id)
    db.session.delete(query)
    db.session.commit()

    return redirect(url_for('faltas.home'))