from flask import Blueprint, render_template

rm_bp = Blueprint('rm', __name__, url_prefix='/rm')

@rm_bp.route('/')
def home():
    return render_template('rm.html')