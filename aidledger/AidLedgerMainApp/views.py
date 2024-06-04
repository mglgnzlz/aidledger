from django.shortcuts import render
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from .models import CustomUser
from .forms import CustomUserCreationForm,qrForm
from django.views import View
from web3 import Web3
from io import BytesIO
from base64 import b64encode
from base64 import b64decode
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image





######################################################init######################################################
# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connected
if not web3.is_connected():
    raise Exception("Could not connect to Ethereum network")
else:
    print(f"Connected to Ethereum network: {web3}")

# Load contract ABI
with open('../blockchain/build/contracts/AidLedger.json') as f:
    aid_ledger_json = json.load(f)
    contract_abi = aid_ledger_json['abi']
    contract_address = "0x0fCc37e0364d17d409DE83bB81E8eA55C6A1589d"
    print(f"Contract ABI: {contract_abi}")

contract = web3.eth.contract(address=contract_address, abi=contract_abi)
print(f"Contract: {contract}")

# Test the function call
try:
    relief_good = contract.functions.getReliefGood(1).call()
    print(relief_good)
except Exception as e:
    print(f"Error: {e}")
##########################################################################################################


######################################################GENERATE/SCAN QR CODES######################################################

def govGenerateQR(request):
    qr_code = request.session.get('qr_code', None)
    if 'qr_code' in request.session:
        del request.session['qr_code']

    relief_good_count = contract.functions.reliefGoodCount().call()
    relief_goods = []
    for i in range(1, relief_good_count + 1):
        relief_good = contract.functions.getReliefGood(i).call()
        relief_goods.append({
            'id': relief_good[0],
            'donor': relief_good[1],  # Assuming the address is already checksummed
            'typeOfGood': relief_good[2],
            'weight': relief_good[3],
            'status': relief_good[4],
            'recipient': relief_good[5]
        })

    relief_goods.reverse()  # Reverse the list if you want to display the latest first

    # Combine both qr_code and relief_goods into the context
    context = {
        'relief_goods': relief_goods,
        'qr_code': qr_code
    }
    return render(request, 'AidLedgerMainPage/govtDashboard.html', context)


# View to create a new relief good
def create_relief_good(request):
    if request.method == "POST":
        context = {}
        rfg_type = request.POST.get('rfgType')
        rfg_weight = request.POST.get('rfgWeight')
        username = request.session['username']
        
        donor_address = Web3.to_checksum_address(username)
        
        recipient_address = "0x0000000000000000000000000000000000000000"

        # print(f"User: {user}")
        print(f"Donor Address: {donor_address}")
        print(f"Recipient Address: {recipient_address}")
        
        # Interact with the smart contract to create a new relief good
        try:
            tx_hash = contract.functions.createReliefGood(
                donor_address,
                rfg_type,
                rfg_weight,
                "In transit",
                recipient_address
            ).transact({'from': donor_address})
            
            # Wait for the transaction to be mined
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Optionally, you can add code to handle the transaction receipt
            print(f"Transaction receipt: {receipt}")
            
            # Generate QR code based on the transaction receipt
            qr_data = f"Transaction Receipt: {receipt.transactionHash.hex()}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=3,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_data = buffer.getvalue()
            buffer.close()

            # Convert the image data to a base64 encoded string
            img_b64 = b64encode(img_data)

            # Create a data URL
            img_data_url = f'data:image/png;base64,{img_b64.decode()}'

            # Add the data URL to the context
            context['qr_code_data_url'] = img_data_url

            # If you still want to download the image
            response = HttpResponse(img_data, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
            return response

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'AidLedgerMainPage/govtDashboard.html', context)





def handlerScanQR (request):
    # Initialize an empty context dictionary
    context = {}
    if request.method == 'POST':
        form = qrForm(request.POST, request.FILES)
        if form.is_valid():
            qr_code_instance = form.save()
            qr_image_path = qr_code_instance.qr_image.path
            decoded_data = decode(Image.open(qr_image_path))
            if decoded_data:
                qr_code_data = decoded_data[0].data.decode('utf-8')
                context['qr_code_data'] = qr_code_data  # Add decoded data to context
            else:
                context['error'] = 'QR code could not be decoded'
    else:
        form = qrForm()
    context['form'] = form
    return render(request, 'AidLedgerMainPage/handlerDashboard.html', context)


def recipScanQR (request):
    
    
    context = {
        
    }
    
    return render(request, "AidLedgerMainPage/recipientDashboard.html", context)
###########################################################################################################




###########################AUTHENTICATION FUNCTIONS###########################


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
                    request.session['username'] = user.username

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
    
    
######################################################