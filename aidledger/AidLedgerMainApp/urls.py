from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [
    path('govgenqr/', views.govGenerateQR, name='govGenerateQR'),
    path('create_relief_good/', views.create_relief_good, name='create_relief_good'),
    path('handlerscanqr/', views.handlerScanQR, name='handlerScanQR'),
    path('recipscanqr/', views.recipScanQR, name='recipScanQR'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('download_qr/', views.create_relief_good, name='download_qr'),
    
    path('moralis_auth', views.moralis_auth, name='moralis_auth'),
    path('request_message', views.request_message, name='request_message'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('verify_message', views.verify_message, name='verify_message'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
