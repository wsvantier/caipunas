from flask import Flask
from models import db
from dropmenu import turmas, rotas
from blueprints.faltas import faltas_bp
from blueprints.rm import rm_bp
from blueprints.lp import lp_bp
from blueprints.transporte import transporte_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caipunas.db'

db.init_app(app)

app.register_blueprint(faltas_bp)
app.register_blueprint(rm_bp)
app.register_blueprint(lp_bp)
app.register_blueprint(transporte_bp)

@app.context_processor
def inject_globals():
    return {
        'turmas': turmas(),
        'transportes': rotas()
    }
    
    

@app.template_filter('RA')
def format_ra(valor):
    return f"{valor:,}".replace(',', '.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)