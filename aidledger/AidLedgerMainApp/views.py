from django.shortcuts import render
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from .models import CustomUser
from .forms import CustomUserCreationForm


# GENERATE QR / SCAN QR FUNCTIONS

def signup(request):
    eth_address = request.GET.get('ethAddress', '')  # Retrieve MetaMask address from query parameters

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.ethAddress = request.POST.get('ethAddress')  # Assign MetaMask address from form data
            user.save()

            # Determine account type
            account_type = request.POST.get('userType')

            # Determine dashboard URL based on account type
            if account_type == 'NGO/GOVT':
                dashboard_url = '/govgenqr/'  # Replace with the URL for NGO/GOVT dashboard
            elif account_type == 'HANDLER':
                dashboard_url = '/handlerscanqr/'  # Replace with the URL for HANDLER dashboard
            elif account_type == 'RECIPIENT':
                dashboard_url = '/recipscanqr/'  # Replace with the URL for RECIPIENT dashboard
            
            return JsonResponse({'dashboard_url': dashboard_url})
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'ethAddress': eth_address,
    }
    return render(request, "AidLedgerMainPage/signUp.html", context)



    
    
def govGenerateQR (request):
    
    
    context = {
        
    }
    
    return render(request, "AidLedgerMainPage/govtDashboard.html", context)

def handlerScanQR (request):
    
    
    context = {
        
    }
    
    return render(request, "AidLedgerMainPage/handlerDashboard.html", context)


def recipScanQR (request):
    
    
    context = {
        
    }
    
    return render(request, "AidLedgerMainPage/recipientDashboard.html", context)


API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjJlOGIwYzM5LWQxMWQtNDNmNi05NGYwLTkzNmUxZjQ1NmM4NCIsIm9yZ0lkIjoiMzk0MjE3IiwidXNlcklkIjoiNDA1MDc3IiwidHlwZUlkIjoiMmVkMThhZDEtZGQyNC00NjQwLTg5NDUtNGM5MWQ3ODUzZWM0IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTY5OTE2NjIsImV4cCI6NDg3Mjc1MTY2Mn0.4kS9AoEPdRBZtODHjNFEtDg7dTFdItb_qAVAc_2589Y'
# this is a check to make sure the API key was set
# you have to set the API key only in line 9 above
# you don't have to change the next line
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit


def moralis_auth(request):
    return render(request, 'AidLedgerMainPage/login.html', {})

def my_profile(request):
    return render(request, 'AidLedgerMainPage/profile.html', {})

def request_message(request):
    data = json.loads(request.body)
    print(data)

    #setting request expiration time to 1 minute after the present->
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + 'Z'

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "defi.finance",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": expirationTime,
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})

    return JsonResponse(json.loads(x.text))


def verify_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = CustomUser.objects.get(username=eth_address)
        except CustomUser.DoesNotExist:
            # user = CustomUser(username=eth_address)
            # user.is_staff = False
            # user.is_superuser = False
            # user.save()
            return redirect('signup')
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))
