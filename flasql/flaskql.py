import os
import sqlite3
from sickle import Sickle
from pymods import MODSReader
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'MODSdebugSmall.xml'),
    SECRET_KEY='potato',
    USERNAME='admin',
    PASSWORD='default',
    OAI='http://merrick.library.miami.edu/oai/oai.php'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def parse_MODS():
    records = MODSReader(app.config['DATABASE'])
    return records

def get_oai():
    oai_feed = Sickle(app.config['OAI'])
    records = oai_feed.ListRecords(metadataPrefix='oai_dc', set='scbooks', ignore_deleted=True)
    return records

@app.route('/')
def index():
    return render_template('index.html')  # , elems=os.listdir('templates/'))

@app.route('/titles')
def titles():
    title_list = []
    for record in parse_MODS():
        for title in record.titles:
            title_list.append(title)
    return render_template('titles.html', titles=title_list)

@app.route('/creators')
def elem_page():
    elem_list = [name.text for record in parse_MODS() for name in record.get_creators]
    return render_template('titles.html', titles=elem_list)

# @app.route('/oai/<elem>')
# def oai_elem_page(elem):
#     try:
#         elem_list = [value for record in get_oai() for value in record.metadata['{}'.format(elem)]]
#         return render_template('titles.html', titles=elem_list)
#     except KeyError:
#         pass


@app.route('/oai/creator')
def oai_elem_page():
    records = get_oai()
    elem_list = []
    try:
        elem_list = [value for record in records for value in record.metadata['creator']]
        print(elem_list)
    except KeyError:
        pass
    return render_template('titles.html', titles=elem_list)
