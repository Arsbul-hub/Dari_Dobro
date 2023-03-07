from app import app, db
from app.models import User, News

if __name__ == '__main__':
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'New': News}

 
    app.run(host='0.0.0.0', port=80)
