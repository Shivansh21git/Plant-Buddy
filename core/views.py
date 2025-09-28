from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserregistrationForm, DeviceForm
from .models import Device, DeviceData
from django.contrib import messages
from django.conf import settings
from dotenv import load_dotenv
from django.http import JsonResponse
import os
load_dotenv()



def home_view(request):
    return render(request, 'core/base.html')

def register_view(request):
    if request.method == 'POST':
         form = UserregistrationForm(request.POST)
         if form.is_valid():
              form.save()
              messages.success(request, "Registration successful. Please login.")
              return redirect('login')
         else: 
             messages.error(request, "Please correct the below error")
    else:
         form = UserregistrationForm()
    return render(request, 'core/register.html',{'form':form})


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user
            device.save()
            return redirect('dashboard')  # Refresh dashboard after adding device
    else:
        form = DeviceForm()

    devices = request.user.devices.all()
    return render(request, 'core/dashboard.html', {
        'devices': devices,
        'form': form
    })

@login_required
def device_data_json(request, device_id):
    device = get_object_or_404(Device, device_id=device_id, user=request.user)
    latest_data = DeviceData.objects.filter(device=device).order_by("-timestamp").first()

    if latest_data:
        return JsonResponse({
            "nitrogen": latest_data.nitrogen,
            "phosphorus": latest_data.phosphorus,
            "potassium": latest_data.potassium,
            "temperature": latest_data.temperature,
            "humidity": latest_data.humidity,
            "timestamp": latest_data.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse({}, status=404)
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Invalid credentials")
#     return render(request, 'core/login.html', {'form': AuthenticationForm()})