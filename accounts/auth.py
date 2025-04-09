from ninja.security import HttpBearer
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuth()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            if user.is_active:
                return user
        except Exception:
            raise HttpError(401, "Token inválido")
