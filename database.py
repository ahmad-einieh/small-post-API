import imp
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

#db_url = "postgresql://postgres:123456@localhost:5432/postgres" # this for postgresql database
#db_url = "mysql://root:123456@localhost:3306/fastapi" # this for mysql database # this for mysql database
#engine = sqlalchemy.create_engine(db_url) #this engin for postgresql and mysql databases 

#this for sqlite database
db_url = "sqlite:///./database.db" 
engine = sqlalchemy.create_engine(db_url, connect_args={"check_same_thread": False})

sessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = dec.declarative_base()