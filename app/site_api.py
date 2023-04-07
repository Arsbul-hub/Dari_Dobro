import flask
from flask import jsonify, make_response

from app import db, app
from app.models import News

blueprint = flask.Blueprint(
    'site_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news')
def get_news():
    news = News.query.all()
    return jsonify(

                [item.to_dict(only=('title', 'body')) for item in news]

    )




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
