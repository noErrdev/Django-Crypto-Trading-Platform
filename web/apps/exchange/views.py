import json
import re
import urllib.parse

import channels.layers
import requests
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from requests.structures import CaseInsensitiveDict

from .common_functions import Give_equivalent
from .models import Portfolio, TradeHistory
from .trade import Trade


def home(request):
    return render(request, "exchange/index.html")


def search(request, value):

    headers = CaseInsensitiveDict()
    url = "https://arzdigital.com/wp-admin/admin-ajax.php"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    encoddedValue = urllib.parse.quote_plus(json.dumps({"s": value}))
    data = f"action=arzAjax&query=search&data={encoddedValue}"

    try:
        resp = requests.post(url, headers=headers, data=data).json().get("coins", "null")
    except:
        resp = "null"

    if resp != "null":
        for item in resp:
            item["image"] = f'https://cdn.arzdigital.com/uploads/assets/coins/icons/32x32/{item["slug"]}.png'
    return JsonResponse(resp, safe=False)


def signUp(request):
    return render(request, "registration/signup.html")


def markets(request):
    return render(request, "exchange/markets.html")


@login_required()
def trade(request, value):
    value = re.sub("'", '"', value)
    value = json.loads(value)

    tradeObject = Trade(request.user, "market", value["type"], value["pair"], value["amount"])
    result = tradeObject.result
    if result["state"] == 0:
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)("orderBook", {"type": "order.display", "content": result})
    return JsonResponse(result)


@login_required()
def portfolio(request):
    eq = Give_equivalent()
    resJson = dict()
    for index, item in enumerate(Portfolio.objects.filter(usr=request.user).iterator()):
        if item.cryptoName == "USDT":
            equivalentAmount = None
        else:
            equivalentAmount = eq.calc_equivalent(item.cryptoName, "USDT", item.amount)[1]
        resJson[index] = {
            "cryptoName": item.cryptoName,
            "amount": item.amount,
            "equivalentAmount": equivalentAmount,
            "marketType": item.marketType,
        }
    return JsonResponse(resJson)


@login_required()
def tradinghistory(request):
    resJson = dict()

    for index, item in enumerate(
        TradeHistory.objects.filter(usr=request.user, amount__gt=0).order_by("-time").iterator()
    ):
        resJson[index] = {
            "type": item.type,
            "pair": item.pair,
            "histAmount": item.histAmount,
            "amount": item.amount,
            "price": item.price,
            "time": item.time,
            "complete": item.complete,
            "orderType": item.orderType,
        }
    return JsonResponse(resJson)


def recentTrades(request):
    resJson = dict()
    for index, item in enumerate(TradeHistory.objects.filter(amount__gt=0).order_by("-time").iterator()):
        resJson[index] = {
            "type": item.type,
            "pair": item.pair,
            "pairPrice": item.price,
            "amount": item.amount,
        }
    return JsonResponse(resJson)


def echo(request):
    return render(request, "exchange/echo.html")
