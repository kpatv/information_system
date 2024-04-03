import os
from flask import Blueprint, render_template, request, current_app
from work_with_db import select_dict
from sql_provider import SQLProvider
from access import login_required, group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder = 'templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
print(os.path.dirname(__file__))
print(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/first', methods = ['GET', 'POST'])
@group_required
@login_required
def query_index():
    if request.method == 'POST':
        client_age = request.form.get('client_age')

        _sql = provider.get('req1.sql', client_age=int(client_age))
        data = select_dict(current_app.config['db_config'], _sql)
        if data:
            client_title = 'Сведения о клиентах, моложе заданного возраста'
            return render_template('dynamic.html', client_title=client_title, data=data)
        else:
            return render_template('error.html')
    return render_template('input_param1_req.html')


@blueprint_query.route('/second ', methods = ['GET', 'POST'])
@group_required
@login_required
def query_index2():
    if request.method == 'POST':
        year = request.form.get('year')
        month = request.form.get('month')
        _sql = provider.get('req2.sql', year=year, month=month)
        data = select_dict(current_app.config['db_config'], _sql)
        if data:
            client_title = 'Cведения о клиентах, ни разу не изменивших баланс за выбранный период времени'
            return render_template('dynamic2.html', client_title=client_title, data=data)
        else:
            return render_template('error.html')
    return render_template('input_param2_req.html')


@blueprint_query.route('/third ', methods = ['GET', 'POST'])
@login_required
@group_required
def query_index3():
    if request.method == 'POST':
        year = request.form.get('year')
        _sql = provider.get('req3.sql', year=year)
        data = select_dict(current_app.config['db_config'], _sql)
        if data:
            client_title = 'Поиск клиентов по городам'
            return render_template('dynamic3.html', client_title=client_title, data=data)
        else:
            return render_template('error.html')
    return render_template('input_param3_req.html')





@blueprint_query.route('/catalog')
def catalog():
    _sql = provider.get('catalog.sql')
    data = select_dict(current_app.config['db_config'], _sql)
    if data:
        catalog_title = 'Каталог услуг, доступных для подклюения'
        return render_template('dynamic_catalog.html', catalog_title=catalog_title, data=data)
    else:
        return 'Ошибка'



