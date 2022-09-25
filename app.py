import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import schemas
import services
import models

app = fastapi.FastAPI()

@app.post("api/regeister")
async def regeister(user:schemas.UserRequset, db:orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.getUserByEmail(email=user.email, db=db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already registered") 
    
    # not yet
    user = models.userModel(email=user.email, name=user.name, phone=user.phone, password_hash=hash.bcrypt.hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
