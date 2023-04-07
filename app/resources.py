from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from app import db
from app.models import News

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
def abort_if_news_not_found(id):
    if not News.query.filter_by(id=id).first():
        return abort(404, message=f"News {id} not found")


class NewsResource(Resource):
    def get(self, id):

        news = News.query.filter_by(id=id).first()
        abort_if_news_not_found(id)

        return jsonify(news.to_dict(only=("title", "body", "cover", "timestamp")))