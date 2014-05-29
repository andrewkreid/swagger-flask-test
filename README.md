swagger-flask-test
==================

A test project for python-flask integration with Swagger

- [Github page for flask-restful-swagger](https://github.com/rantav/flask-restful-swagger)
- [Swagger Spec v1.2](https://github.com/wordnik/swagger-spec/blob/master/versions/1.2.md)

== Prerequisites

At the time of writing, you had to use the following fork of flask-restful-swagger, as it contains a
newer version of swagger-ui that fixes a bug that prevented you posting JSON

[https://github.com/richtera/flask-restful-swagger](https://github.com/richtera/flask-restful-swagger)

== Calling The API with curl
```bash
    # Add a
    curl -v -X POST --data 'application={"name": "foo"}'  http://localhost:5000/ums/v1/applications

    curl -X PUT --data '{"name": "Changed Name", "password":""}' --header "Content-Type:application/json" http://localhost:5000/ums/v1/applications/1
```