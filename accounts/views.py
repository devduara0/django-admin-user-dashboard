from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User



def register(request):
  if request.method == 'POST':
   
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

   
    if password == password2:
     
      if User.objects.filter(username=username).exists():
        messages.error(request, 'Jina la mtumiaji lime chukuliwa')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'Barua pepe ime chukuliwa')
          return redirect('register')
        else:
          
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)

          user.save()
          messages.success(request, 'Ume sajiliwa na unaweza ku ingia "log in"')
          return redirect('login')
    else:
      messages.error(request, 'Nywila zina tofautiana')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')
