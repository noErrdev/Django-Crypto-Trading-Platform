var socket = new WebSocket('ws://' + window.location.host + '/ws/');
socket.onopen = function () {
    socket.send(JSON.stringify({"page":0}));
};

socket.onmessage = function(e) {
    var message = e.data;
    data = JSON.parse(message)
    fillData(data)
};

socket.onclose = function(e) {
    console.error('Socket closed unexpectedly');
};

console.clear()

function fillData(data) {
    Object.keys(data).forEach(function(item, index) {
        obj = data[index]
        document.getElementById(index + '_tr').setAttribute('data-href',`/account/trade/${obj["symbol"]}-USDT`)
        document.getElementById(index + '_image').src = `${obj["img"]}`
        document.getElementById(index + '_name').innerText = `${obj["symbol"]} (${obj["name"]})`
        document.getElementById(index + '_current_price').innerText = obj['price']
        var change = document.getElementById(index + '_price_change_percentage_24h')
        change.innerText = obj['24c'] + ' %'
        document.getElementById(index + '_total_volume').innerText = obj['vol']
        document.getElementById(index + '_marketCap').innerText = obj['mc']
        document.getElementById(index + '_market_cap_rank').innerText = obj['rank']
        document.getElementById(index + '_high').innerText = obj['24h']
        document.getElementById(index + '_low').innerText = obj['24l']

        if (parseInt(obj['24c']) > 0) {
            change.classList.remove('red')
            change.classList.add('green')
        }
        else if (parseInt(obj['24c']) < 0){
            change.classList.remove('green')
            change.classList.add('red')
        }
        else {   
            change.classList.remove('red')
            change.classList.remove('green')
        }
    })
}

function initial() {
    const numberOfCoins = 20;

    var parent = document.getElementById("cryptos")
    var before = document.getElementById("before1")

    var counter = 0
    while (counter < numberOfCoins) {

        var tr = document.createElement("tr")

        var market_cap_rank = document.createElement("td")
        var coin = document.createElement("td")
        var marketCap = document.createElement("td")
        var image = document.createElement("img")
        var current_price = document.createElement("td")
        var price_change_percentage_24h = document.createElement("td")
        var total_volume = document.createElement("td")
        var high = document.createElement("td")
        var low = document.createElement("td")
        var name = document.createElement("div")

        market_cap_rank.id = counter + '_market_cap_rank'
        coin.id = counter + '_coin'
        marketCap.id = counter + '_marketCap'
        current_price.id = counter + '_current_price'
        price_change_percentage_24h.id = counter + '_price_change_percentage_24h'
        total_volume.id = counter + '_total_volume'
        image.id = counter + '_image'
        name.id = counter + '_name'
        high.id = counter + '_high'
        low.id = counter + '_low'
        tr.id = counter + '_tr'

        coin.appendChild(image)
        coin.appendChild(name)
        tr.appendChild(market_cap_rank)
        tr.appendChild(coin)
        tr.appendChild(current_price)
        tr.appendChild(price_change_percentage_24h)
        tr.appendChild(high)
        tr.appendChild(low)
        tr.appendChild(total_volume)
        tr.appendChild(marketCap)

        parent.insertBefore(tr, before)

        counter ++;
    }
}

function pagination(page) {

    var prev = document.getElementById('paginationPrev')
    var now = document.getElementById('paginationText')
    var next = document.getElementById('paginationNext')
    now.innerText = page + 1 + '/' + 30

    prev.onclick = function(event) {
        if (page > 0) {
            socket.close()
            page --

            socket = new WebSocket('ws://' + window.location.host + '/ws/');

            socket.onopen = function () {
                socket.send(JSON.stringify({"page":page}));
            };

            socket.onmessage = function(e) {
                var message = e.data;
                data = JSON.parse(message)
                fillData(data)
            };

            socket.onclose = function(e) {
                console.error('Socket closed unexpectedly');
            };

            now.innerText = page + 1 + '/' + 30
        }
    }

    next.onclick = function(event) {
        if (page <= 30) {
            socket.close()
            page ++

            socket = new WebSocket('ws://' + window.location.host + '/ws/');

            socket.onopen = function () {
                socket.send(JSON.stringify({"page":page}));
            };

            socket.onmessage = function(e) {
                var message = e.data;
                data = JSON.parse(message)
                fillData(data)
            };

            socket.onclose = function(e) {
                console.error('Socket closed unexpectedly');
            };

            now.innerText = page + 1 + '/' + 30
        }
    }
}
var page = 0
initial()
pagination(page)