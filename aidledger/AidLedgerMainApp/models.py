from django.db import models

# Create your models here.

class AccountInfo(models.Model):
    USER_TYPE_CHOICE= {
        "NGO/GOVT": "NGO/GOVT",
        "HANDLER": "HANDLER",
        "RECIPIENT": "RECIPIENT",
    }
    ethAddress = models.CharField(max_length=42, unique=True)
    acctName = models.CharField(max_length=60)
    userType = models.CharField(max_length=10, choices=USER_TYPE_CHOICE)