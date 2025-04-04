from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from .models import CustomUser
from provas.routers import router as provas_router


api = NinjaAPI()

class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    role: str

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        from ninja_jwt.authentication import JWTAuth
        jwt_auth = JWTAuth()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            if user.is_active:
                return user
        except Exception:
            raise HttpError(401, "Token inválido")

@api.post("/auth/registro")
def registrar(request, payload: RegisterSchema):
    if payload.role not in [CustomUser.Role.ADMIN, CustomUser.Role.PARTICIPANTE]:
        raise HttpError(400, "Tipo de usuário inválido")
    
    user = CustomUser.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        role=payload.role
    )
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "username": user.username,
            "role": user.role
        }
    }

@api.post("/auth/login")
def login(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Credenciais inválidas")
    
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "username": user.username,
            "role": user.role
        }
    }

@api.get("/admin/dashboard", auth=AuthBearer())
def dashboard_admin(request):
    if not request.auth.is_admin():
        raise HttpError(403, "Acesso restrito a administradores")
    return {"message": f"Bem-vindo Admin {request.auth.username}"}

@api.get("/participante/dashboard", auth=AuthBearer())
def dashboard_participante(request):
    return {"message": f"Olá {request.auth.username}"}

api.add_router("/provas/", provas_router)

from ninja import NinjaAPI
from provas.routers import router as provas_router


