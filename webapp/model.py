from mongoengine import *

connect('simple_tasklist', host='db')


class Task(Document):
    name = StringField()
