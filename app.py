import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import schemas
import services
import models

app = fastapi.FastAPI()

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
