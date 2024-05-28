from django.shortcuts import render

# GENERATE QR / SCAN QR FUNCTIONS
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
    
    return render(request, "AidLedgerMainPage/recipentDashboard.html", context)



