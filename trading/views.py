from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .utilfuncs import queryPrice, feedback_context_fill, validate_password
from .models import Users, Portfolio, TransactionHistory
from .forms import QueryForm, PurchaseForm, LoginForm, RegisterForm
	
error_type = {
		"INVALID_SYMBOL": 1,
		"INSUFFICIENT_FUNDS": 2,
	}

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			password_conf = form.cleaned_data['password_conf']
			
			# check password validity
			error_msg = validate_password(password, password_conf)
			if error_msg is not None:
				context = feedback_context_fill(error_msg, "Register", "Error", "Register")
				return render(request, "trading/feedback.html", context)
			
			# check email validity
			email = form.cleaned_data['email_address']
			try:
				valid = validate_email(email)
			except ValidationError:
				context = feedback_context_fill("It seems that you provided an invalid email address. Please try again!", "Register", "Error", "Register")
				return render(request, "trading/feedback.html", context)
			
			# check if account already exists
			exists = Users.objects.filter(username=username)
			if len(exists) == 0:
				# create new User
				Users.objects.create(username=username, password=make_password(password), balance=4000, email_address=email)
				context = feedback_context_fill("Successfully registered! You may login now.", "Register", "Success", "Login", "Go to Login")
				return render(request, "trading/feedback.html", context)
			else:
				context = feedback_context_fill("It seems that this username already exists. Please try another one!", "Register", "Error", "Register")
				return render(request, "trading/feedback.html", context)
		else:
			context = feedback_context_fill("Oops, something went wrong. Please try again!", "Register", "Error", "Register")
			return render(request, "trading/feedback.html", context)
	else:
		auth.logout(request)
		form = RegisterForm()
		return render(request, "trading/register.html", {"form": form})

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = Users.objects.filter(username=username)
			if len(user) == 1 and check_password(password, user[0].password):
				request.session["username"] = username
				context = feedback_context_fill("Successfully logged in!", "Login", "Success", "Index", "Go to Homepage")
				return render(request, "trading/feedback.html", context)
			else:
				context = feedback_context_fill("Incorrect username or password! Please try again.", "Login", "Error", "Login")
				return render(request, "trading/feedback.html", context)
		else:
			context = feedback_context_fill("Incorrect username or password! Please try again.", "Login", "Error", "Login")
			return render(request, "trading/feedback.html", context)
	else:
		form = LoginForm()
		return render(request, "trading/login.html", {"form": form })
		
def logout(request):
	auth.logout(request)
	context = feedback_context_fill("Successfully logged out.", "Logged out", "", "Index", "Go back to Homepage")
	return render(request, "trading/feedback.html", context)
		
def index(request):
	if request.session.has_key('username'):
		id = Users.objects.filter(username=request.session["username"])[0].id
		context = {}
		# query user information
		user_overview = Users.objects.filter(id=id)
		context["balance"] = user_overview[0].balance
		
		# query portfolio information
		total_wealth = float(context["balance"])
		portfolio = Portfolio.objects.filter(user_id = id)
		for stock in portfolio:
			# update prices
			current_price = queryPrice(stock.stock_symbol)
			if current_price is not None:
				stock.current_value = current_price * float(stock.quantity)
				total_wealth += stock.current_value
				Portfolio.objects.filter(stock_symbol = stock.stock_symbol).update(current_value=stock.current_value)
			else:
				context = feedback_context_fill("Oops some error happened. Please try again!", "", "Error", "Index", "Go back to Homepage")
				return render(request, "trading/feedback.html")
		context["portfolio"] = portfolio
		context["total_wealth"] = total_wealth
		
		# query transaction history
		transactions = TransactionHistory.objects.filter(user_id = id).order_by("date")
		context["transactions"] = transactions
		
		return render(request, "trading/index.html", context)
	else:
		form = LoginForm()
		return render(request, "trading/login.html", {"form": form})
		
def query(request):
	if request.method == "POST":
		form = QueryForm(request.POST)
		if form.is_valid():
			stock_symbol = form.cleaned_data['stock_symbol'].upper()
			current_price = queryPrice(stock_symbol)
			# check if symbol exists
			if current_price is not None:
				return render(request, "trading/query_purchase_result.html", {"stock_symbol": stock_symbol, "current_price": current_price, "title": "Query"})
			else:
				return render(request, "trading/query_purchase_error.html", {"stock_symbol": stock_symbol, "title": "Query", "dest":"query", "error_type": error_type["INVALID_SYMBOL"]})
	else:
		context = {
			"form": QueryForm(),
			"msg": "Enter a symbol to query the price of a stock:",
			"title": "Query",
			"dest": "query",
		}
		return render(request, "trading/query_purchase.html", context)

def purchase(request):
	if request.method == "POST":
		form = PurchaseForm(request.POST)
		if form.is_valid():
			id = Users.objects.filter(username=request.session["username"])[0].id
			# get data from form
			stock_symbol = form.cleaned_data['stock_symbol'].upper()
			quantity = form.cleaned_data['quantity']
			current_price = queryPrice(stock_symbol)
			
			# check if symbol exists
			if current_price is None:
				context = {"stock_symbol": stock_symbol, "title": "Purchase", "dest":"purchase", "error_type": error_type["INVALID_SYMBOL"]}
				return render(request, "trading/query_purchase_error.html", context)
			
			# validate sufficient funds
			cash_needed = current_price * float(quantity)
			user_overview = Users.objects.filter(id=id)
			balance = user_overview[0].balance
			context = {"balance": balance, "stock_symbol": stock_symbol, "title": "Purchase", "dest": "purchase", "title": "Purchase",
				"current_price": current_price, "quantity": quantity, "cash_needed": cash_needed, "error_type": error_type["INSUFFICIENT_FUNDS"],
			}
			if cash_needed > float(balance):
				return render(request, "trading/query_purchase_error.html", context)
			else:
				# deduct money from balance
				new_balance = float(Users.objects.filter(id=id)[0].balance) - cash_needed
				Users.objects.filter(id=id).update(balance=new_balance)
				
				# add new stocks to portfolio
				exists_check = Portfolio.objects.filter(user_id=id, stock_symbol=stock_symbol)
				if len(exists_check) == 0:
					Portfolio.objects.create(user_id=id, stock_symbol=stock_symbol, quantity=quantity, current_value=cash_needed)
				else:
					prev_quantity = Portfolio.objects.filter(user_id=id, stock_symbol=stock_symbol)[0].quantity
					Portfolio.objects.filter(user_id=id, stock_symbol=stock_symbol).update(quantity=prev_quantity + int(quantity))
				
				# record transaction history
				TransactionHistory.objects.create(user_id=id, stock_symbol=stock_symbol, quantity=quantity, purchase_price=cash_needed, per_share_price=current_price)
				return render(request, "trading/query_purchase_result.html", context)
	else:
		context = {
			"form": PurchaseForm(),
			"msg": "Enter a symbol and quantity to purchase stocks:",
			"title": "Purchase",
			"dest": "purchase",
		}
		return render(request, "trading/query_purchase.html", context)