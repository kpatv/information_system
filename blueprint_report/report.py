from flask import Blueprint, render_template, request, current_app
from work_with_db import select_dict, call_proc
from sql_provider import SQLProvider
from access import group_required, login_required
import os

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/work')
@login_required
@group_required
def work_with_reports():
    config = current_app.config['report_config']
    return render_template('report_menu.html', conf=config, key_list=config.keys())


@blueprint_report.route('/for_date/<proc>/<sql>', methods=['GET', 'POST'])
@login_required
@group_required
def create_report(proc, sql):
    if request.method == 'GET':
        return render_template('input_param.html')
    else:
        date_ = request.form.get('date')
        if not date_:
            return render_template('input_param.html', error='Недостаточно входных данных')
        else:
            year_ = int(date_[0:4])
            month_ = int(date_[5::])
            _sql = provider.get(sql, month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)
            if not res:
                temp = call_proc(current_app.config['db_config'], proc, year_, month_)
                _sql = provider.get(sql, month_=month_, year_=year_)
                res = select_dict(current_app.config['db_config'], _sql)
                if res:
                    return render_template('report.html', msg='Отчёт успешно создан', y=year_, m=month_)
                else:
                    return render_template('input_param.html',
                                           error='Невозможно создать отчёт по указанному периоду. Недостаточно данных')
            else:
                print(1)
                return render_template('report.html', msg='Отчёт уже существует', y=year_, m=month_)


@blueprint_report.route('/report_show/', methods=['GET', 'POST'])
@login_required
@group_required
def report_show():
    print(request.args)
    if 'year' in request.args.keys() and 'month' in request.args.keys():
        _sql = provider.get('all.sql', month_=request.args['month'], year_=request.args['year'])
        res = select_dict(current_app.config['db_config'], _sql)
        if res:
            return render_template('dynamic_rep.html', result=res, key_list=res[0].keys())
    if request.method == 'GET':
        return render_template('input_param.html')
    else:
        date_ = request.form.get('date')
        if not date_:
            return render_template('input_param.html', error='Недостаточно входных данных')
        else:
            year_ = int(date_[0:4])
            month_ = int(date_[5::])
            _sql = provider.get('all.sql', month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)

            if res:
                month_dict = {
                    1: "январь",
                    2: "февраль",
                    3: "март",
                    4: "апрель",
                    5: "май",
                    6: "июнь",
                    7: "июль",
                    8: "август",
                    9: "сентябрь",
                    10: "октябрь",
                    11: "ноябрь",
                    12: "декабрь"
                }
                res_keys = {
                    "Year": "Год",
                    "Month": "Месяц",
                    "Service ID": "ID услуги",
                    "Title": "Название услуги",
                    "Count of connections": "Количество подключений"
                }
                month_name = month_dict.get(month_)
                key_res = res_keys.values()
                key_res_1 = res_keys.keys()
                return render_template('dynamic_rep.html',
                                       rep_title=f"Отчет о количестве подключений конкретных услуг за {month_name} {year_} года",
                                       result=res, key_list=key_res, key_list_1=key_res_1)
            else:
                return render_template('input_param.html', error='Отчёт по данному периоду не существует')


@blueprint_report.route('/for_date2/<proc>/<sql>', methods=['GET', 'POST'])
@login_required
@group_required
def create_report2(proc, sql):
    if request.method == 'GET':
        return render_template('input_param2.html')
    else:
        date_ = request.form.get('date')
        start_index = request.form.get('start_index')
        end_index = request.form.get('end_index')
        if not date_ or not start_index or not end_index:
            return render_template('input_param2.html', error='Недостаточно входных данных')
        else:
            year_ = int(date_[0:4])
            month_ = int(date_[5::])

            _sql = provider.get(sql, month_=month_, year_=year_, start_index=start_index, end_index=end_index)
            res = select_dict(current_app.config['db_config'], _sql)
            if not res:
                temp = call_proc(current_app.config['db_config'], proc, year_, month_, start_index, end_index)
                _sql = provider.get(sql, month_=month_, year_=year_, start_index=start_index, end_index=end_index)
                res = select_dict(current_app.config['db_config'], _sql)
                if res:
                    return render_template('report2.html', msg='Отчёт успешно создан', y=year_, m=month_)
                else:
                    return render_template('input_param2.html',
                                           error='Невозможно создать отчёт по указанному периоду. Недостаточно данных')
            else:
                print(1)
                return render_template('report2.html', msg='Отчёт уже существует', y=year_, m=month_)


@blueprint_report.route('/report_show2/', methods=['GET', 'POST'])
@login_required
@group_required
def report_show2():
    print(request.args)
    if 'year' in request.args.keys() and 'month' in request.args.keys():
        _sql = provider.get('all2.sql', month_=request.args['month'], year_=request.args['year'])
        res = select_dict(current_app.config['db_config'], _sql)
        if res:
            return render_template('dynamic_rep.html', result=res, key_list=res[0].keys())
    if request.method == 'GET':
        return render_template('input_param2.html')
    else:
        date_ = request.form.get('date')
        start_index = request.form.get('start_index')
        end_index = request.form.get('end_index')
        if not date_:
            return render_template('input_param.html', error='Недостаточно входных данных')
        else:
            year_ = int(date_[0:4])
            month_ = int(date_[5::])
            _sql = provider.get('all2.sql', month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)
            if res:
                month_dict = {
                    1: "январь",
                    2: "февраль",
                    3: "март",
                    4: "апрель",
                    5: "май",
                    6: "июнь",
                    7: "июль",
                    8: "август",
                    9: "сентябрь",
                    10: "октябрь",
                    11: "ноябрь",
                    12: "декабрь"
                }
                res_keys = {
                    "Year": "Год",
                    "Month": "Месяц",
                    "client ID": "ID клиента",
                    "Name": "ФИО клиаента",
                }
                month_name = month_dict.get(month_)
                key_res = res_keys.values()
                key_res_1 = res_keys.keys()

                return render_template('dynamic_rep.html',
                                       rep_title=f"Отчет об изменениях баланса клиентов, номера которых находятся в диапазоне от {start_index} до {end_index} за {month_name} {year_} года",
                                       result=res, key_list=key_res, key_list_1=key_res_1)
            else:
                return render_template('input_param.html', error='Отчёт по данному периоду не существует')
