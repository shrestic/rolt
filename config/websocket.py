from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

import rolt.chat.routing
from rolt.core.middleware import jwt_auth_middleware

websocket_application = ProtocolTypeRouter(
    {
        "websocket": jwt_auth_middleware(
            URLRouter(rolt.chat.routing.websocket_urlpatterns),
        ),
    },
)
