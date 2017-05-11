from flask import Flask, render_template
from flask import session
from flask_material import Material
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
# from wtforms.validators import Required

app = Flask(__name__)
Material(app)

GAME_SESSIONS = {}
LAST_GAME = 0

# Routing
NAV_ROUTES = ["home", "about"] #, "new"]

# Colours
COLOURS = {
    'nav_colour': 'black',
    'nav_text_colour': 'white-text',
    'primary_colour': 'black',
    'primary_text_colour': 'white-text',
    'highlight_colour': 'grey'
}

# GLOBAL DATA
@app.context_processor
def template_global_variables():
    globs = {}
    globs.update(COLOURS)
    globs['navs'] = NAV_ROUTES
    return globs

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
