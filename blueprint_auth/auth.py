from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from work_with_db import select_dict
from sql_provider import SQLProvider
import os

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html', error=None)
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        _sql = provider.get('auth_internal.sql', login=login, password=password)
        user = select_dict(current_app.config['db_config'], _sql)
        if not user:
            _sql = provider.get('auth_external.sql', login=login, password=password)
            user = select_dict(current_app.config['db_config'], _sql)
        if user:
            session['user_id'] = user[0]['id']
            session['user_group'] = user[0]['group_name']
            return redirect(url_for('bp_auth.form_menu'))
        else:
            return render_template('auth.html', error='Неверные имя пользователя или пароль')


@blueprint_auth.route('/form_menu')
def form_menu(error=None):
    if 'user_id' in session.keys():
        if 'user_group' in session.keys():
            return render_template('form_menu.html', user_id=session['user_id'], group_name=session['user_group'],
                                   error=error)
        else:
            return render_template('form_menu.html', error=error)
    return render_template('form_menu.html', error='Вы не авторизованы')




@blueprint_auth.route('/', methods=['GET', 'POST'])
def sign_out():
    session.clear()
    return render_template('main_menu.html')
