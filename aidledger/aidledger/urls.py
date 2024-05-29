
from django.contrib import admin
from django.urls import include,path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("aidl/", include("AidLedgerMainApp.urls")),
    path('auth/', include('django.contrib.auth.urls')),
    
]
