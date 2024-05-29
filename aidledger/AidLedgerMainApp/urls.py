from django.urls import path
from . import views  
    
urlpatterns = [
    path('', views.UserLogin, name='UserLogin'),
    path('govgenqr/', views.govGenerateQR, name='govGenerateQR'),
    path('handlerscanqr/', views.handlerScanQR, name='handlerScanQR'),
    path('recipscanqr/', views.recipScanQR, name='recipScanQR'),
    
    #TEST AUTH MORALIS
    path('moralis_auth', views.moralis_auth, name='moralis_auth'),
    path('request_message', views.request_message, name='request_message'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('verify_message', views.verify_message, name='verify_message'),
    
]
