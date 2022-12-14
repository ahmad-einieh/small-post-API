import imp
import database
import models
import sqlalchemy.orm as orm
import schemas
import fastapi
import email_validator
import passlib.hash as hash
import jwt
import fastapi.security as security
from typing import List

public_key = "AHMADISTHEBEST2000AHMADESMAAILEINIEH"
outhToSchema = security.OAuth2PasswordBearer("/api/login")

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

async def create_user(user:schemas.UserRequset, db=orm.Session ):

    try:
        isValid = email_validator.validate_email(email=user.email)
        email = isValid.email
    except email_validator.EmailNotValidError:
        raise fastapi.HTTPException(status_code=400, detail="Invalid Email")

    hashed_password = hash.bcrypt.hash(user.password)
    userObject = models.userModel(
        email=email,
        name=user.name,
        phone=user.phone,
        password_hash=hashed_password
    )
    db.add(userObject)
    db.commit()
    db.refresh(userObject)
    return userObject

async def create_token(user:models.userModel):
    user_schema = schemas.UserResponse.from_orm(user)
    user_dict = user_schema.dict()
    del user_dict['created_At']

    token = jwt.encode(user_dict, public_key , algorithm="HS256") 
    return dict(access_token=token,token_type="bearer")


async def login(email:str,password:str,db=orm.Session):
    user = await getUserByEmail(email=email,db=db)
    if not user:
        return False
    if not hash.bcrypt.verify(password, user.password_hash):
        return False
    return user



async def current_user(db:orm.Session= fastapi.Depends(get_db),token:str=fastapi.Depends(outhToSchema)):
    try:
        payload = jwt.decode(token, public_key, algorithms=["HS256"])
        db_user = db.query((models.userModel)).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Information")
    
    return schemas.UserResponse.from_orm(db_user)

async def create_post(user:schemas.UserResponse, post:schemas.PostsRequest, db=orm.Session):
    postObject = models.postModel(
        **post.dict(),
        user_id=user.id
    )
    db.add(postObject)
    db.commit()
    db.refresh(postObject)
    return schemas.PostsResponse.from_orm(postObject)

async def get_posts_by_user(user:schemas.UserResponse, db=orm.Session):
    posts = db.query(models.postModel).filter_by(user_id=user.id)
    return list(map(schemas.PostsResponse.from_orm, posts))

async def get_posts_by_all(db=orm.Session):
    posts = db.query(models.postModel)
    return list(map(schemas.PostsResponse.from_orm, posts))


async def get_post_by_id(post_id:int, db=orm.Session):
    post = db.query(models.postModel).get(post_id)
    if not post:
        raise fastapi.HTTPException(status_code=404, detail="Post Not Found")
    #return schemas.PostsResponse.from_orm(post)
    return post

async def delete_post(post:models.postModel, db=orm.Session):
    db.delete(post)
    db.commit()

async def update_post(post:schemas.PostsRequest,db_post:models.postModel,db=orm.session):

    db_post.title = post.title
    db_post.content = post.content
    db_post.image = post.image

    db.commit()
    db.refresh(db_post)

    return schemas.PostsResponse.from_orm(db_post)
