from flask import Flask
from models import db
from blueprints.faltas import faltas_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caipunas.db'

db.init_app(app)

app.register_blueprint(faltas_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)