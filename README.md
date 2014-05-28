swagger-flask-test
==================

A test project for python-flask integration with Swagger

- [Miguel's Flask Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Miguel's Flask-RESTful Tutorial](http://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful)

    curl -v -X POST --data 'application={"name": "foo"}'  http://localhost:5000/ums/v1/applications
    curl -X PUT --data '{"name": "Changed Name", "password":""}' --header "Content-Type:application/json" http://localhost:5000/ums/v1/applications/1