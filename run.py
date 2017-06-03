"""
Runs the server
"""
from app.routes import app

if __name__ == '__main__':
    print("LAUNCHING APP")
    app.run(threaded=True)
