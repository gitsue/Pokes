from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'poke/index.html')

def register(request):
	if request.method =="POST":
		result = User.objects.register(request.POST)
	if result["registered"]:
		request.session["user_name"] = result["user"].alias
		return redirect('/success')
	else:
		print_messages(request, result["errors"])
		return redirect('/')

def print_messages(request, message_list):
	for message in message_list:
		messages.add_message(request, messages.INFO, message)

def login(request):
	if request.method == "POST":
		user = User.objects.login(request.POST)

	if user:
		request.session['user_name'] = user.alias
		return redirect('/success')

def success(request):
	if "user_name" not in request.session:
		return redirect("/")
	print request.session["user_name"]
	context = {
		"users": User.objects.exclude(alias=request.session["user_name"]),
		"this_user": User.objects.get(alias=request.session["user_name"])
	}
	return render(request, 'poke/pokes.html', context)

def logout(request):
	request.session.clear()
	return redirect("/")


def poke(request):
	pass


