import database
import models
import sqlalchemy.orm as orm

def create_db():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

#create_db()

async def getUserByEmail(email:str, db=orm.Session ):
    return db.query(models.userModel).filter(models.userModel.email == email).first()