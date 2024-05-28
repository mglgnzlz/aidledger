from django.urls import path
from . import views  
    
urlpatterns = [
    path('govgenqr/', views.govGenerateQR, name='govGenerateQR'),
    path('handlerscanqr/', views.handlerScanQR, name='handlerScanQR'),
    path('recipscanqr/', views.recipScanQR, name='recipScanQR'),
    
]
