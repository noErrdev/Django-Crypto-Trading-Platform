var main_url = window.location.origin;
var usdtValue = 0;
var pairValue = 0;
var uValue = document.getElementById('uValue');
var pValue = document.getElementById('pValue');
uValue.value = 0;
pValue.value = 0;
var globPair = 'BTC'
var createdHistory = [];

function getPortfolio(pair) {

    globPair = pair
    var usdtAmount = document.getElementById('usdtAmount');
    var pairAmount = document.getElementById('pairAmount');

    usdtAmount.innerText = '0 USDT'
    pairAmount.innerText = `0 ${pair}`

    const url = `${main_url}/portfolio/`
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { console.log('time out'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            res = this.response;
            Object.keys(res).forEach(function(item, index) {

                if (res[item]['cryptoName'] == pair && pair != 'USDT') {
                    pairAmount.innerText = `${res[item]['amount'].toFixed(5)} ${pair} = ${res[item]['equivalentAmount'].toFixed(5)} USDT`
                    pairValue = res[item]['amount']
                }
                if (res[item]['cryptoName'] == 'USDT') {
                    usdtAmount.innerText = `${res[item]['amount'].toFixed(5)} USDT`
                    usdtValue = res[item]['amount']
                }
            })
        }
        else {
            console.log(this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        console.log('error')
    }
}

function trade(type, pair) {
    var amount = 0;
    if (type == 'buy') {
        amount = uValue.value;
    }
    else {
        amount = pValue.value;
    }
    var reqJson = {
        'pair' : `${pair}|USDT`,
        'type' : type,
        'amount' : amount,
    }

    const url = `${main_url}/trade/${JSON.stringify(reqJson)}`
    console.log(url);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { createAlert('info', 'Connection failed!'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            res = this.response;
            if (res['state'] == 0) {

                createAlert('success', 'Order filled!')
            }
            else {
                
                createAlert('danger', 'Insufficient balance!')
            }
            getPortfolio(globPair);
            getHistory()
        }
        else if (this.status != 200){
            createAlert('danger', this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        createAlert('danger', 'There is a problem, try again!')
    }
}

function removeHistory() {
    createdHistory.forEach(function(item, index) {
        item.remove();
    })
    createdHistory = []
}

function getHistory() {

    removeHistory()
    const url = `${main_url}/tradinghistory`
    console.log(url);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { console.log('time out'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            res = this.response;
            var parent = document.getElementById("open-orders")
            var before = document.getElementById("before")
            Object.keys(res).forEach(function(item, index) {

                var newNode = document.createElement("ul")
                newNode.classList.add("d-flex", "justify-content-between", "market-order-item", "ul")

                var time = document.createElement("li")
                var pair = document.createElement("li")
                var type = document.createElement("li")
                var price = document.createElement("li")
                var amount = document.createElement("li")
                var total = document.createElement("li")

                time.innerText = res[index]['time']
                type.innerText = res[index]['type']
                pair.innerText = res[index]['pair']
                price.innerText = res[index]['pairPrice'].toFixed(5)
                amount.innerText = res[index]['amount'].toFixed(5)
                total.innerText = res[index]['price'].toFixed(5)

                if (res[index]['type'] == 'buy') {
                    type.classList.add('green')
                }
                else {
                    type.classList.add('red')
                }

                newNode.appendChild(time)
                newNode.appendChild(pair)
                newNode.appendChild(type)
                newNode.appendChild(price)
                newNode.appendChild(amount)
                newNode.appendChild(total)

                createdHistory.push(newNode)

                parent.insertBefore(newNode, before)
            })
        }
        else {
            console.log(this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        console.log('error')
    }
}

function calcAmount(change, object) {
    if (change == 'usdt') {
        uValue.value = usdtValue * parseFloat(object.innerText.replace('%', '')) / 100
    }
    else {
        pValue.value = pairValue * parseFloat(object.innerText.replace('%', '')) / 100
    }
}

function percentage() {
    var pair = document.getElementById('pairPercentage');
    var usdt = document.getElementById('usdtPercentage');

    pair.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            pair.childNodes[index].addEventListener("click", function() {calcAmount('pair', pair.childNodes[index]);});
        }
    })

    usdt.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            usdt.childNodes[index].addEventListener("click", function() {calcAmount('usdt', usdt.childNodes[index]);});
        }
    })
}

function validate(evt) {

    var theEvent = evt || window.event;

    // Handle paste
    if (theEvent.type === 'paste') {
      key = event.clipboardData.getData('text/plain');
    } else {
    // Handle key press
      var key = theEvent.keyCode || theEvent.which;
      key = String.fromCharCode(key);
    }
    var regex = /[0-9.]|\./;
    if( !regex.test(key) ) {
    theEvent.returnValue = false;
        if(theEvent.preventDefault) {
            theEvent.preventDefault();
        }
    }
}

function closeAlert(){
    var alertBox = this.parentNode;
    alertBox.classList.remove('bounceInRight');
    alertBox.classList.add('bounceOutRight', 'd-none');    
}

function createAlert(type, message) {
    var logos = ['fa-info', 'fa-check', 'fa-exclamation-triangle']

    var parent = document.getElementById('alert');
    var mainDiv = document.createElement("div")

    mainDiv.classList.add('alert', 'animated', `alert-${type}`, 'bounceInRight')
    
    var secondDiv = document.createElement("div")    
    secondDiv.classList.add('icon', 'pull-left')

    var firstI = document.createElement("i")  

    if (type == 'info') {

        firstI.classList.add('fa', logos[0], 'fa-2x')
    }
    else if (type == 'success') {

        firstI.classList.add('fa', logos[1], 'fa-2x')
    }
    else if (type == 'danger') {

        firstI.classList.add('fa', logos[2], 'fa-2x')
    }


    secondDiv.appendChild(firstI)

    var lastDiv = document.createElement("div")    
    lastDiv.classList.add('copy')
    var title = document.createElement("h4")
    title.innerText = type    
    var text = document.createElement("p")    
    text.innerText = message    
    lastDiv.appendChild(title)
    lastDiv.appendChild(text)

    var close = document.createElement("a") 
    close.addEventListener('click', closeAlert)   
    close.classList.add('close')
    var closeI = document.createElement("i")    
    closeI.classList.add('fa', 'fa-times')
    close.appendChild(closeI)

    mainDiv.appendChild(secondDiv)
    mainDiv.appendChild(lastDiv)
    mainDiv.appendChild(close)

    parent.appendChild(mainDiv)
}

percentage();
getHistory()