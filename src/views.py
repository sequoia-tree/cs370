from flask import render_template

from app import app
from models import (
    CURRENT_WK,
    FILES,
    INSTRUCTOR,
    META_TYPES,
    RESOURCE_TYPES,
    RESOURCES_TO_RENDER,
    STAFF,
    WEEKS,
)
from semester import META, TIME_UNTIL_RELEASED
from utils import *

def rename(name):
    def rename_decorator(function):
        function.__name__ = name
        return function
    return rename_decorator

def make_template(route, renderer, template_function, *template_args):
    @app.route(f'/{route}.html')
    @rename(renderer)
    def render():
        return template_function(*template_args)

@app.route('/')
def render_index():
    return render_template('index.html',
                           TIME_UNTIL_RELEASED=TIME_UNTIL_RELEASED,
                           CURRENT_WK=CURRENT_WK,
                           WEEKS=WEEKS,
                           META_TYPES=META_TYPES,
                           RESOURCE_TYPES=RESOURCE_TYPES,
                           RESOURCES_TO_RENDER=RESOURCES_TO_RENDER,
                           INSTRUCTOR=INSTRUCTOR,
                           **META)

@app.route('/staff')
def render_staff():
    return render_template('staff.html', **STAFF)

for week in WEEKS:
    for type in RESOURCE_TYPES:
        if RESOURCES_TO_RENDER[week][type]:
            make_template(
                week.route(type), week.renderer(type),
                lambda week, type: render_template(week.template(type), week=week, type=type, **META),
                week, type
            )

for file in FILES:
    make_template(
        file, f'render_{file}',
        lambda file: render_template(f'{file}.html', file=file, **META),
        file
    )
