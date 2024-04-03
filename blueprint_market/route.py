from flask import Blueprint, render_template, request, session, current_app, url_for
from werkzeug.utils import redirect
from sql_provider import SQLProvider
from work_with_db import select_dict, fetch_from_cache, save_order_with_list, clean_cache
import os
from access import group_required


blueprint_market = Blueprint('bp_market', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
def order_index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']

    if request.method == 'GET':

        sql = provider.get('product_list.sql')
        items = fetch_from_cache('all_items_cached', cache_config)(select_dict)(db_config, sql)

        sql = provider.get('get_client.sql', cl_id=session['user_id'])
        serv = fetch_from_cache(session['user_id'], cache_config)(select_dict)(db_config, sql)
        print(session['user_id'])
        if serv is None:
            serv = []
        serv = [i['ser_id'] for i in serv]
        print(serv)

        basket_items = session.get('basket', [])
        print(basket_items)
        for item in range(len(items)):
            cur = items[item]
            if cur['ser_id'] in basket_items and cur['ser_id'] in serv:
                items[item]['connection_status'] = 0
            elif cur['ser_id'] in basket_items or cur['ser_id'] in serv:
                items[item]['connection_status'] = 1
            else:
                items[item]['connection_status'] = 0

        return render_template('product_list.html', items=items)

    else:
        session.permanent = True
        s_id = request.form.get('s_id')
        if 'basket' in session:
            if s_id in session['basket']:
                session['basket'].remove(s_id)
            else:
                session['basket'].append(s_id)
        else:
            session['basket'] = [s_id]

        return redirect(url_for('bp_market.order_index'))


@blueprint_market.route('/save_order', methods=['GET','POST'])
def save_order():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']

    user_id = session.get('user_id')
    current_basket = session.get('basket', [])

    sql = provider.get('get_client.sql', cl_id=session['user_id'])
    serv = fetch_from_cache(session['user_id'], cache_config)(select_dict)(db_config, sql)
    if serv is None:
        serv = []
    serv = [i['ser_id'] for i in serv]

    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket, serv)

    if order_id:
        if 'basket' in session:
            session.pop('basket')
        clean_cache(session['user_id'], cache_config)
        return render_template('order_created.html')
    else:
        return 'Что-то пошло не так'



@blueprint_market.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.order_index'))
