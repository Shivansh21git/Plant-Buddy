from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserregistrationForm, DeviceForm
from .models import Device
from influxdb_client import InfluxDBClient
from django.contrib import messages

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
def device_data_view(request, device_id):
    # InfluxDB connection settings
    url = "http://localhost:8086"
    token = "ll68ar-kpu7RmwjXzlicjaHtx0N6vKFLANGHc-upvXmkIB4h7P9z9AbpljEJhlNBnr781ORNc3PoddTgAqS3EA=="
    org = "myorg"
    bucket = "plantbuddy"

    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -7d)
      |> filter(fn: (r) => r["_measurement"] == "npk_data")
      |> filter(fn: (r) => r["device_id"] == "{device_id}")
      |> last()
    '''

    result = query_api.query(org=org, query=query)

    data_points = {}
    for table in result:
        for record in table.records:
            field_name = record.get_field()
            value = record.get_value()
            data_points[field_name] = value

    return render(request, "core/device_data.html", {
        "device_id": device_id,
        "data_points": data_points
    })

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