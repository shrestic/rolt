import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)
User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


def jwt_auth_middleware(inner):
    async def middleware(scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                user = await get_user(user_id)

                if isinstance(user, AnonymousUser):
                    logger.warning(
                        "[JWT] User ID %(user_id)s not found → Anonymous",
                        extra={"user_id": user_id},
                    )
                else:
                    logger.info(
                        "[JWT] Authenticated user %(username)s (ID: %(user_id)s)",
                        extra={"username": user.username, "user_id": user.id},
                    )

                scope["user"] = user

            except Exception:
                logger.exception("[JWT] Token decode failed")
                scope["user"] = AnonymousUser()
        else:
            logger.warning("[JWT] No token found in query string")
            scope["user"] = AnonymousUser()

        return await inner(scope, receive, send)

    return middleware
