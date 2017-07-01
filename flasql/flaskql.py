import os
import sqlite3
from sickle import Sickle
from pymods import MODSReader, OAIReader
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'DCdebugSmall.xml'),
    SECRET_KEY='potato',
    USERNAME='admin',
    PASSWORD='default',
    OAI='http://merrick.library.miami.edu/oai/oai.php'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def parse_local_dc():
    records = OAIReader(app.config['DATABASE'])
    return records


def get_oai():
    oai_feed = Sickle(app.config['OAI'])
    records = oai_feed.ListRecords(metadataPrefix='oai_dc', set='scbooks', ignore_deleted=True)
    return records


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<elem>')
def local_elem_page(elem):
    dc_ns = '{http://purl.org/dc/elements/1.1/}'
    records = parse_local_dc()
    try:
        elem_list = [value for record in records for value in record.metadata.get_element(dc_ns + elem)]
    except TypeError:
        pass
    return render_template('titles.html', titles=elem_list)


@app.route('/oai/<elem>')
def oai_elem_page(elem):
    records = get_oai()
    try:
        elem_list = [value for record in records for value in record.metadata[elem]]
    except TypeError:
        pass
    return render_template('titles.html', titles=elem_list)
