from app import app, db
from app.models import User, News

if __name__ == '__main__':
 
    app.run(host='0.0.0.0', port=80)
