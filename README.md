swagger-flask-test
==================

A test project for python-flask integration with Swagger

- [Github page for flask-restful-swagger](https://github.com/rantav/flask-restful-swagger)
- [Swagger Spec v1.2](https://github.com/wordnik/swagger-spec/blob/master/versions/1.2.md)

Prerequisites
-------------

At the time of writing, you had to use the following fork of flask-restful-swagger, as it contains a
newer version of swagger-ui that fixes a bug that prevented you POSTing JSON with the right Content-Type:

- [https://github.com/richtera/flask-restful-swagger](https://github.com/richtera/flask-restful-swagger)

Quick Build'n'Run Instructions
------------------------------

```bash
sudo pip install flask-restful

# Install a fork of flask-restful-swagger that fixes some important bugs
git clone https://github.com/richtera/flask-restful-swagger.git
cd flask-restful-swagger
python ./setup.py build
sudo python ./setup.py install

# Check out and run the test
cd ..
git clone git@github.com:andrewkreid/swagger-flask-test.git
cd swagger-flask-test
python ./app_api.py

```

You should now be able to browse to http://localhost:5000/api/spec.html


Calling The API with curl
-------------------------

```bash
# Getting a list of Applications
curl http://localhost:5000/ums/v1/applications

# Getting an Application by ID
curl http://localhost:5000/ums/v1/applications/1

# Adding a new Application
curl -X POST --data 'application={"name": "foo"}'  http://localhost:5000/ums/v1/applications

# Modifying an existing Application
curl -X PUT --data '{"name": "Changed Name", "password":""}' --header "Content-Type:application/json" http://localhost:5000/ums/v1/applications/1
```

