import settings
from includes.db import Db
from includes.models import Base

class Schema:

    def CreateDatabase():

        query = f"CREATE DATABASE {settings.DB_NAME}"

        return Db.ExecuteQuery(query, None, True, True, True)

    def CreateExtensions():
        
        return Db.ExecuteQuery("CREATE EXTENSION IF NOT EXISTS vector", None, False, False, True)
    
    def CreateSchema():

        return Db.ExecuteQuery("CREATE SCHEMA IF NOT EXISTS batman", None, False, True, True)

    def CreateTables():
        
        return Base.metadata.create_all(Db.GetEngine(True))

    def CreateIndexes():

        return Db.ExecuteQuery("CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);", None, False, False, True)