import sys

from routers.auth import get_current_user

sys.path.append("..")

from starlette.responses import RedirectResponse
from fastapi import Depends, status, APIRouter, Request, Form
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user": "Not authorized"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/password", response_class=HTMLResponse)
async def change_user_password(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("change-password.html", {"request": request, "user": user})


@router.post("/password", response_class=HTMLResponse)
async def change_user_password_commit(request: Request,
                                      username: str = Form(...),
                                      password1: str = Form(...),
                                      password2: str = Form(...),
                                      db: Session = Depends(get_db)):
    current_user = await get_current_user(request)
    if current_user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user = db.query(models.Users).filter(models.Users.username == username).first()

    if user is None or not bcrypt_context.verify(password1, user.hashed_password):
        msg = 'Please type correct current username & password'
        return templates.TemplateResponse("change-password.html",
                                          {"request": request, "msg": msg, "user": current_user})

    hashed_password2 = bcrypt_context.hash(password2)
    user.hashed_password = hashed_password2

    db.add(user)
    db.commit()

    msg = 'Password Change Successful'
    return templates.TemplateResponse("change-password.html", {"request": request, "msg": msg, "user": current_user})
