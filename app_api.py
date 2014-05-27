#!/usr/bin/env python

"""
Sample REST API for testing Swagger integration.
"""

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_restful import Api, Resource, reqparse
from application_mock import get_applications, get_application, put_application, delete_application, create_application
import json

app = Flask(__name__)
api = Api(app)


class ApplicationListAPI(Resource):
    """ API implementation for listing Applications and creating new ones"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('application', type=str, required='true', help='Need Application JSON')


    def get(self):
        status, applications = get_applications()
        if status != 200:
            abort(status)
        else:
            return applications

    def post(self):

        args = self.reqparse.parse_args()
        status, application = create_application(json.loads(args['application']))
        if status != 200:
            abort(status)
        else:
            return application


class ApplicationAPI(Resource):
    """API Implementation for the Application Resource"""

    def get(self, app_id):
        pass

    def put(self, app_id):
        pass

    def delete(self, app_id):
        pass

api.add_resource(ApplicationListAPI, '/ums/v1/applications')
api.add_resource(ApplicationAPI, '/ums/v1/applications/<int:app_id>')

if __name__ == '__main__':
    create_application({"name": "Initial Application"})
    app.run(host="0.0.0.0", debug=True)