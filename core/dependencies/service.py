from databases import database

def _create_database():
    return database.Base.metadata.create_all(bind=database.engine)