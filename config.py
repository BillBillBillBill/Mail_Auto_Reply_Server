import mongoengine


def using_db(alias="marserv", name="marserv"):
    mongoengine.register_connection(
        alias,
        name,
        host="localhost",
        port=27017
    )
