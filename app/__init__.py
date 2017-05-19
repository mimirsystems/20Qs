"""
Runs the server
"""
from app.routes import app
from app.db import db

# Config
app.config['SECRET_KEY'] = 'thisshouldbeasceret'

if __name__ == '__main__':
    print("RUNNING MAIN")
    db.create_all()
    print("LAUNCHING APP")
    app.run()
