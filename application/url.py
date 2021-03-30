from flask import make_response
from flask_restful import Resource, reqparse, abort, fields, marshal_with

from datetime import datetime

from .models import db, UrlModel

from .util import create_shortcode, is_valid_shortcode, correct_url

"""Create a parser to get data from POST request"""
parser = reqparse.RequestParser()
parser.add_argument('url')
parser.add_argument('shortcode')

"""Compile stat fields to easily return stats."""
stats_fields = {
    'created': fields.DateTime(dt_format='iso8601'),
    'lastRedirect': fields.DateTime(dt_format='iso8601'),
    'redirectCount': fields.Integer
}

def update_db(obj_to_update):
    """Update stats on object."""
    obj_to_update.lastRedirect = datetime.now()
    obj_to_update.redirectCount += 1
    db.session.commit()

def add_to_db(obj_to_add):
    """Add object to db"""
    object_url = correct_url(obj_to_add['url'])
    urlObject = UrlModel(shortcode=obj_to_add['shortcode'], url=object_url)
    db.session.add(urlObject)
    db.session.commit()

class Shorten(Resource):
    """Check data and add to db if data is valid."""
    def post(self):
        args = parser.parse_args()
        if args['url']:
            if not args['shortcode']:
                args['shortcode'] = create_shortcode()
                add_to_db(args)
                return {"shortcode": args['shortcode']}, 201
            elif is_valid_shortcode(args['shortcode']):
                urlObject = UrlModel.query.filter_by(shortcode=args['shortcode']).first()
                if urlObject:
                    abort(409, message = "Shortcode already in use")
                else:
                    add_to_db(args)
                    return {"shortcode": args['shortcode']}, 201
            else:
                abort(412, message = "The provided shortcode is invalid")
        else:
            abort(400, message = "Url not present")

class ReturnURL(Resource):
    """Return URL for GET requests with a shortcode that is in the db."""
    def get(self, shortcode):
        urlObject = UrlModel.query.filter_by(shortcode=shortcode).first()
        if urlObject:
            update_db(urlObject)
            resp = make_response()
            resp.status_code = 302
            resp.headers['Location'] = urlObject.url
            resp.autocorrect_location_header = False
            return resp
        else:
            abort(404, message = "Shortcode not found")

class ReturnStats(Resource):
    """Return stats for GET requests with a shortcode that is in the db."""
    @marshal_with(stats_fields)
    def get(self, shortcode):
        urlObject = UrlModel.query.filter_by(shortcode=shortcode).first()
        if urlObject:
            return urlObject
        else:
            abort(404, message = "Shortcode not found")


