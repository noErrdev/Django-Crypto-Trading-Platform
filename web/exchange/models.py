from email.policy import default
from statistics import mode
from django.db import models
from django.conf import settings
# from django.conf import DEFAULT_CONTENT_TYPE_DEPRECATED_MSG

class Portfolio(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	cryptoName = models.CharField(max_length=50)
	amount = models.FloatField(default=0, null=True)
	equivalentAmount = models.FloatField(default=0, null=True, blank=True)
	marketType = models.CharField(max_length=10, default='spot') # spot/futures

	def __str__(self):
		return self.cryptoName

# details of terminated spot orders
class TradeHistory(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=4) # buy/sell
	pair = models.CharField(max_length=20)
	pairPrice = models.FloatField()
	orderType = models.CharField(max_length=15, default=None) # market/limit/stop-limit
	histAmount = models.JSONField(default=None)
	amount = models.CharField(max_length=100)
	price = models.FloatField()
	time = models.DateTimeField(auto_now=True)
	complete = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = 'Trade histories'

# only for open spot orders
class SpotOrders(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=4) # buy/sell
	pair = models.CharField(max_length=20)
	orderType = models.CharField(max_length=15) # market/limit/stop-limit
	amount = models.CharField(max_length=100) # e.g., 0.02 BTC 
	price = models.FloatField()
	triggerConditions = models.FloatField(blank=True, null=True) # only used for stop-limit
	createDate = models.DateTimeField(auto_now_add=True)

# details of all futures orders
class FuturesOrders(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=4) # short/long
	pair = models.CharField(max_length=20)
	amount = models.CharField(max_length=100) # e.g., 0.02 BTC
	entryPrice = models.FloatField()
	marketPrice = models.FloatField()
	liqPrice = models.FloatField()
	leverage = models.IntegerField()
	orderType = models.CharField(max_length=15) # market/limit/stop-limit
	marginType = models.CharField(max_length=10) # cross/isolated
	complete = models.BooleanField(default=False)
	pnl = models.FloatField(default=0)
	triggerConditions = models.FloatField(blank=True, null=True) # only used for stop-limit
	createDate = models.DateTimeField(auto_now_add=True)

# extra details for terminated futures orders including history amounts for statistical reports
class FuturesHistory(models.Model):
	orderDetails = models.OneToOneField(FuturesOrders, on_delete=models.DO_NOTHING)
	histAmount = models.JSONField(default=None)
	terminateDate = models.DateTimeField(auto_now_add=True)