import mongoengine


mongoengine.register_connection(
    "marserv",
    "marserv",
    host="localhost",
    port=27017
)
