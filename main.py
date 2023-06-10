from app import application, blueprint, db_session

if __name__ == '__main__':
    # db_session.global_init("application.db")

    application.run(host='0.0.0.0')
