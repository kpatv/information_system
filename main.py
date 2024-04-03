import json
from flask import Flask, render_template, session
from blueprint_auth.auth import blueprint_auth
from blueprint_query.query import blueprint_query
from blueprint_report.report import blueprint_report
from blueprint_market.route import blueprint_market

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'you will never guess'

with open('db_config.json') as f:
    app.config['db_config'] = json.load(f)

with open('access.json') as f:
    app.config['access_config'] = json.load(f)

with open('reports.json') as f:
    app.config['report_config'] = json.load(f)

with open('cache.json') as f:
    app.config['cache_config'] = json.load(f)

app.register_blueprint(blueprint_auth, url_prefix='/')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')


@app.route('/')
def main_menu():
    return render_template('main_menu.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/req')
def req():
    return render_template('req.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
