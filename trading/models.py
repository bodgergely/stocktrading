from django.db import models

class Users(models.Model):
	username = models.CharField(max_length=100)
	email_address = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	balance = models.DecimalField(decimal_places=2, max_digits=12)
	date_joined = models.DateField(auto_now=True)
	
class Portfolio(models.Model):
	user_id = models.IntegerField()
	stock_symbol = models.CharField(max_length=20)
	quantity = models.IntegerField()
	current_value = models.DecimalField(decimal_places=2, max_digits=12)
	
class TransactionHistory(models.Model):
	user_id = models.IntegerField()
	stock_symbol = models.CharField(max_length=20)
	quantity = models.IntegerField()
	purchase_price = models.DecimalField(decimal_places=2, max_digits=12)
	per_share_price = models.DecimalField(decimal_places=2, max_digits=12)
	date = models.DateField(auto_now=True)
