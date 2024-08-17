from flask import Blueprint, render_template, session, request
import uuid

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def index():
    if 'username' not in session:
        return render_template('username.html')
    return render_template('index.html')

@user_bp.route('/set_username', methods=['POST'])
def set_username():
    session['username'] = request.form['username']
    session['id'] = str(uuid.uuid4())
    return render_template('index.html')
