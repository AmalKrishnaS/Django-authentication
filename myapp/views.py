from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home_page(request): 
    return render(request,"registration/home.html")
    
def signup_page(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            return HttpResponse('Passwords doesn\'t match')
        else:
            if User.objects.filter(username = username).first():
                HttpResponse(request, "This username is already taken")
                return redirect('home')
        
            myuser = User.objects.create_user(username, email, pass1)
            
            myuser.save()
        
            return redirect('login')
        
  
    return render(request, 'registration/signup.html')

def login_page(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        
        user = authenticate(request=request, username=username, password=pass1)
        
        if user is not None:
            request.session['username']=username
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Incorrect password or username")
        
    return render(request, 'registration/login.html')

def logout_page(request):
    logout(request)
    request.session.flush
    return redirect('login')