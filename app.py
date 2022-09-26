import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import schemas
import services
from typing import List
from fastapi.middleware.cors import CORSMiddleware 

app = fastapi.FastAPI()
# SECOND PARAMETER LIST OF ACCEPTED URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #["url","url2"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/regeister")
async def regeister(user:schemas.UserRequset, db:orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.getUserByEmail(email=user.email, db=db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already registered") 


    db_user = await services.create_user(user=user, db=db)
    return await services.create_token(user=db_user) 
    
@app.post("/api/login")
async def login(form_data:security.OAuth2PasswordRequestForm=fastapi.Depends(),db:orm.Session=fastapi.Depends(services.get_db)):
    db_user = await services.login(email=form_data.username,password=form_data.password,db=db)
    if not db_user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")

    return await services.create_token(user=db_user)

@app.get("/api/user/current_user",response_model=schemas.UserResponse)
async def current_user(user:schemas.UserResponse=fastapi.Depends(services.current_user)):
    return user

@app.post("/api/post/create",response_model=schemas.PostsResponse)
async def create_post(post:schemas.PostsRequest, db:orm.Session=fastapi.Depends(services.get_db), user:schemas.UserResponse=fastapi.Depends(services.current_user)):
    return await services.create_post(user=user, post=post, db=db) 

@app.get("/api/post/get_posts_by_user",response_model=List[schemas.PostsResponse])
async def get_posts_by_user(user:schemas.UserResponse=fastapi.Depends(services.current_user), db:orm.Session=fastapi.Depends(services.get_db)):
    return await services.get_posts_by_user(user=user, db=db)

@app.get("/api/post/all_users",response_model=List[schemas.PostsResponse])
async def get_posts_by_all( db:orm.Session=fastapi.Depends(services.get_db)):
    return await services.get_posts_by_all( db=db)

@app.get("/api/post/get_post_by_id/{post_id}",response_model=schemas.PostsResponse)
async def get_post_by_id(post_id:int,db:orm.session = fastapi.Depends(services.get_db)):
    return await services.get_post_by_id(post_id=post_id, db=db)

@app.delete("/api/post/delete_post_by_id/{post_id}")
async def delete_post_by_id(post_id:int,db:orm.session = fastapi.Depends(services.get_db), user:schemas.UserResponse=fastapi.Depends(services.current_user)):
    post = await services.get_post_by_id(post_id=post_id, db=db)
    await services.delete_post(post=post, db=db)
    return "delete is done!"

@app.put("/api/post/update_post_by_id/{post_id}",response_model=schemas.PostsResponse)
async def update_post_by_id(post_id:int, post:schemas.PostsRequest, db:orm.session = fastapi.Depends(services.get_db), user:schemas.UserResponse=fastapi.Depends(services.current_user)):
    dp_post = await services.get_post_by_id(post_id=post_id, db=db)
    return await services.update_post(post=post,db_post=dp_post, db=db)

