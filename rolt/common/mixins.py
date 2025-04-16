from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class JwtAuthMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
