from app import app, blueprint, db_session

if __name__ == '__main__':
    # db_session.global_init("app.db")

    app.run(host='0.0.0.0', port=80, debug=True)
