"""
Runs the server
"""
from app.routes import app

# Config
app.config['SECRET_KEY'] = 'thisshouldbeasceret'

if __name__ == '__main__':
    print("LAUNCHING APP")
    app.run()
