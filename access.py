from functools import wraps
from flask import session, current_app, request
from blueprint_auth.auth import form_menu


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return 'Вам необходимо авторизоваться'

    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            user_role = session['user_group']
            if user_role:
                access = current_app.config['access_config']
                user_target = request.blueprint
                user_func = request.endpoint
                if user_role in access and user_target in access[user_role]:
                    return func(*args, **kwargs)
                elif user_role in access and user_func in access[user_role]:
                    return func(*args, **kwargs)
                else:
                    return form_menu('Недостаточно прав')
            else:
                return form_menu('У вас нет каких-либо прав в этой системе')
        else:
            return form_menu('Вы не авторизованы')

    return wrapper
