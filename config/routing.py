from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import OriginValidator, AllowedHostsOriginValidator

from account import routing as account_routing
from exchange import routing as exchange_routing

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    account_routing.websocket_urlpatterns +
                    exchange_routing.websocket_urlpatterns
                )
            )
        )
    )
})