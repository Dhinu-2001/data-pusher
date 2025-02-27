from django.db import models
import uuid
from django.contrib.auth.models import User
import secrets
# Create your models here.

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255, unique=True, editable=False, default=secrets.token_hex)
    website = models.URLField(blank=True, null=True)
    
class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])
    headers = models.JSONField(default=dict, blank=True, null=True) 
