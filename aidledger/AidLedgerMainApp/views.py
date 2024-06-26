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
from django.views import View


# GENERATE QR / SCAN QR FUNCTIONS

class SignUpView(View):
    def get(self, request):
        eth_address = request.GET.get('ethAddress', '')
        return render(request, 'AidLedgerMainPage/signUp.html', {'ethAddress': eth_address})

    def post(self, request):
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            userType = data.get('userType')
            accountName = data.get('accountName')

            if not username:
                return JsonResponse({'error': 'Ethereum address is missing'}, status=400)
            if not userType:
                return JsonResponse({'error': 'User type is missing'}, status=400)
            if not accountName:
                return JsonResponse({'error': 'Account name is missing'}, status=400)

            # Create and save a new UserProfile instance
            CustomUser.objects.create(
                username=username,
                userType=userType,
                accountName=accountName
            )

            # Determine the redirect URL based on user type
            redirect_url = ''
            if userType == 'NGO/GOVT':
                redirect_url = '/govgenqr/'
            elif userType == 'HANDLER':
                redirect_url = '/handlerscanqr/'
            elif userType == 'RECIPIENT':
                redirect_url = '/recipscanqr/'

            # Return a JSON response indicating success and the redirect URL
            return JsonResponse({'message': 'Sign up successful!', 'redirect_url': redirect_url}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=400)


    
    
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
    try:
        data = json.loads(request.body)
        print("Received data:", data)

        REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers={'X-API-KEY': API_KEY}
        )
        
        response_data = response.json()
        print("Moralis response:", response_data)
        print("Status code:", response.status_code)
        
        if response.status_code == 201:
            eth_address = response_data.get('address')
            print("ETH address:", eth_address)
            try:
                user = CustomUser.objects.get(username__iexact=eth_address)
                print("User found:", user.username)
                if user.is_active:
                    login(request, user)
                    request.session['auth_info'] = data
                    request.session['verified_data'] = response_data

                    redirect_url = determine_redirect_url(user)
                    return JsonResponse({'user': user.username, 'redirect_url': redirect_url})
                else:
                    print("Account is disabled.")
                    return JsonResponse({'error': 'Account disabled'})
            except CustomUser.DoesNotExist:
                print("User does not exist, redirecting to signup.")
                return JsonResponse({'redirect_url': '/signup/'})
        else:
            print("Failed to verify message.")
            return JsonResponse(response_data)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': 'An unexpected error occurred'})

def determine_redirect_url(user):
    if user.userType == 'NGO/GOVT':
        return '/govgenqr/'
    elif user.userType == 'HANDLER':
        return '/handlerscanqr/'
    elif user.userType == 'RECIPIENT':
        return '/recipscanqr/'
    else:
        return '/'