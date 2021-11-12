from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
class TradeHistory(models.Model):
	# usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
	usr = models.ForeignKey(User, on_delete=models.CASCADE)
	id = models.AutoField(primary_key=True)
	type = models.CharField(max_length=4)
	pair = models.CharField(max_length=10, default=None)
	pairPrice = models.FloatField()
	amount = models.FloatField(default=0)
	price = models.FloatField()
	time = models.DateTimeField(auto_now=True)


class Portfolio(models.Model):
	# usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
	usr = models.ForeignKey(User, on_delete=models.CASCADE)
	cryptoName = models.CharField(max_length=10, default=None, primary_key=True)
	amount = models.FloatField(default=0, null=True)
	equivalentAmount = models.FloatField(default=0, null=True)



