"""
Runs the server in debug mode
"""

from os import path, walk
from app.routes import app

def get_watches():
    watch_files = []
    for extra_dir in WATCH:
        for dirname, _, files in walk(extra_dir):
            watch_files += [path.join(dirname, file) for file in files]
    return watch_files

# Config
WATCH = ['app/templates', 'app/static']
app.config['PORT'] = 8000
app.config['DEBUG'] = True

if __name__ == '__main__':
    print("DEBUGGING")
    app.run(host='0.0.0.0', extra_files=get_watches())
