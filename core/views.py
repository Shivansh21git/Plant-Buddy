from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserregistrationForm
from .models import Device


def home_view(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
         form = UserregistrationForm(request.POST)
         if form.is_valid():
              form.save()
              return redirect('login')
    else:
         form = UserregistrationForm()
    return render(request, 'core/register.html',{'form':form})


@login_required
def dashboard_view(request):
     devices = request.user.devices.all()
     return render(request, 'core/dashboard.html', {'devices': devices})

         

# Create your views here.
