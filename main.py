from app import app, site_api

if __name__ == '__main__':

    app.register_blueprint(site_api.blueprint)
    app.run(host='0.0.0.0', port=80, debug=True)
