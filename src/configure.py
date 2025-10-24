import sys

from includes.db import Db
from includes.schema import Schema

class Configure:

    def __init__(self):

        if not Db.Connect(True, True):
            sys.exit('ERROR - Could not establish connection to database')

        if not Schema.CreateDatabase():
            sys.exit('ERROR - Could not create database')

        if not Schema.CreateTables():
            sys.exit('ERROR - Could not create tables')

        if not Schema.CreateIndexes():
            sys.exit('ERROR - Could not create indexes')

        print('INFO - Service configured successfully')

try:
    Configure()

except Exception as e:
    sys.exit(e)