#!/usr/bin/env python

"""
Mock data store for Application objects. An Application Object looks like:

{
  "id" : int,
  "name" : string,
  "password" : string
}
"""

import random

application_map = {}
app_id_counter = 1


def random_password():
    """Mock random password generator. Not for prod, obviously..."""
    alphabet = 'abcdedfghijklmnopqrstuvwxyz'
    return ''.join(random.sample(alphabet, 10))


def get_applications():
    global application_map
    return 200, sorted(application_map.values(), key=lambda x: x["id"])


def get_application(app_id):
    global application_map
    if app_id in application_map:
        return 200, application_map[app_id]
    else:
        return 404, "Application Not Found"


def put_application(app):
    global application_map
    if "id" not in app:
        raise ValueError("Application does not have an ID field")

    app_id = app["id"]
    if app_id not in application_map:
        # No such Application
        return 404, "Applcation not found."

    application_map[app_id]["name"] = app["name"]
    application_map[app_id]["password"] = app["password"]
    return 200, application_map[app_id]


def delete_application(app_id):
    if app_id in application_map:
        del application_map[app_id]
        return 200, "DELETED"
    return 404, "Not Found"


def create_application(app):
    global application_map
    global app_id_counter

    new_app = {"id": app_id_counter}
    app_id_counter += 1
    new_app["name"] = app["name"]
    if "password" in app and len(app["password"]) > 0:
        new_app["password"] = app["password"]
    else:
        new_app["password"] = random_password()
    application_map[new_app["id"]] = new_app

    return 200, new_app

if __name__ == "__main__":
    create_application({"name": "app1"})
    create_application({"name": "app2", "password": "passwd2"})
    create_application({"name": "app3"})

    print get_applications()
    print "\n"
    print get_application(1)
    print get_application(666)

    print put_application({"id": 2, "name": "app2", "password": "fungus"})
    print get_applications()

    print delete_application(1)
    print get_applications()

    print delete_application(55)
