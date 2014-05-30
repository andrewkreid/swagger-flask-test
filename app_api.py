#!/usr/bin/env python

"""
Sample REST API for testing Swagger integration.
"""

from flask import Flask, abort, request
from flask_restful import Api, Resource, fields, marshal_with
from application_mock import get_applications, get_application, put_application, delete_application, create_application
from flask_restful_swagger import swagger
import logging
import socket

app = Flask(__name__)

# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api = swagger.docs(Api(app),
                   produces=["application/json"],
                   basePath="http://%s:5000" % socket.getfqdn(),
                   resourcePath="/",
                   apiVersion='0.9',
                   api_spec_url="/api/spec")


@swagger.model
class Link:
    """Model for Links provided in the API"""
    resource_fields = {
        "href": fields.Url,       # Currently no way to set a description on mode fields :(
        "type": fields.String,
        "method": fields.String,
        "rel": fields.String,
        "title": fields.String
    }


@swagger.model
@swagger.nested(
    next_results=Link.__name__,
    previous_results=Link.__name__
)
class PaginationInfo:
    """Model for pagination of results"""
    resource_fields = {
        "next_results": fields.Nested(Link.resource_fields),
        "previous_results": fields.Nested(Link.resource_fields),
        "count": fields.Integer,
        "number_of_results": fields.Integer,
        "offset": fields.Integer
    }


@swagger.model
class ApplicationModel:
    """An Application """
    resource_fields = {
        "app_id": fields.Integer,
        "name": fields.String,
        "password": fields.String
    }


@swagger.model
@swagger.nested(
    applications=ApplicationModel.__name__,
    pagination=PaginationInfo.__name__
)
class ApplicationListModel:
    """A List Of Applications"""
    resource_fields = {
        'applications': fields.List(fields.Nested(ApplicationModel.resource_fields)),
        'pagination': fields.Nested(PaginationInfo.resource_fields)
    }


class ApplicationListAPI(Resource):
    """ API implementation for listing Applications and creating new ones"""

    def __init__(self):
        pass

    @swagger.operation(
        summary="Get a list of Applications",
        responseClass=ApplicationListModel.__name__,
        nickname="getApplicationList"
    )
    def get(self):
        status, applications = get_applications()
        if status != 200:
            abort(status)
        else:
            pagination_fragment = {
                "count": len(applications),
                "next_results": "",
                "previous_results": "",
                "number_of_results": len(applications),
                "offset": 0
            }
            return {"applications": applications, "pagination": pagination_fragment}, 200, {
                'Access-Control-Allow-Origin': '*'}

    @swagger.operation(
        notes=
        """
        Create a new Application resource by POST'ing Application JSON. <br><br>
        You MUST NOT include the app_id parameter (it will be assigned by the server).
        <pre>
        some preformatted text
        </pre>

        """,
        summary="Create a new application",
        responseClass=ApplicationModel.__name__,
        nickname="create",
        consumes=[
            "application/json"
        ],
        parameters=[
            {
                "name": "body",
                "description": "Application m",
                "dataType": ApplicationModel.__name__,
                "required": True,
                "allowMultiple": False,
                "paramType": "body",
            }
        ],
        responseMessages=[

        ]
    )
    def post(self):
        if not request.json:
            abort(400)
        logging.error("JSON: " + repr(request.json))
        status, application = create_application(request.json)
        if status != 200:
            abort(status)
        else:
            return application, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self, **args):
        return {'Allow': 'GET,PUT,POST,DELETE'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'}


class ApplicationAPI(Resource):
    """API Implementation for the Application Resource"""

    @swagger.operation(
        notes="Get an Application by ID",
        summary="Get a single Application by ID",
        nickname="get",
        responseClass=ApplicationModel.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Application Not Found"
            }
        ]
    )
    @marshal_with(ApplicationModel.resource_fields)
    def get(self, app_id):
        status, application = get_application(app_id)
        if status != 200:
            abort(status)
        else:
            return application

    @swagger.operation(
        summary="Modify an existing Application",
        nickname="modifyApplication",
        parameters=[
            {
                "name": "body",
                "description": "Application m",
                "dataType": ApplicationModel.__name__,
                "required": True,
                "allowMultiple": False,
                "paramType": "body",
            }
        ]
    )
    def put(self, app_id):
        new_app = request.json
        status, application = put_application(app_id, new_app)
        if status != 200:
            abort(status)
        return application

    @swagger.operation(
        method="DELETE",
        summary="Delete an Application by ID",
        responseMessages=[
            {
                "code": 404,
                "message": "Application Not Found"
            }
        ]
    )
    def delete(self, app_id):
        logging.error("DELETE %d" % app_id)
        status, message = delete_application(app_id)
        if status != 200:
            abort(status)
        return message


api.add_resource(ApplicationListAPI, '/ums/v1/applications')
api.add_resource(ApplicationAPI, '/ums/v1/applications/<int:app_id>')

if __name__ == '__main__':
    create_application({"name": "Initial Application"})
    app.run(host="0.0.0.0", debug=True)