from django.urls import path

from .consumers import TradeConsumer, historiesConsumer
from account.consumers import MarketConsumer

app_name = 'exchange_ws'
websocket_urlpatterns = [
    path('ws/trade/', TradeConsumer.as_asgi()),
    path('ws/trade/prices/', MarketConsumer.as_asgi()),
    path('ws/histories/', historiesConsumer.as_asgi())
]