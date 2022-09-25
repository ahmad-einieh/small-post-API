import imp
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

db_url = "sqlite:///./database.db"
engine = sqlalchemy.create_engine(db_url, connect_args={"check_same_thread": False})

sessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = dec.declarative_base()