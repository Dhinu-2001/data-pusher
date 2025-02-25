from rest_framework import serializers
from .models import Account, Destination
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'url', 'http_method']
        
class AccountSerializer(serializers.ModelSerializer):
    destinations = DestinationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'name', 'email', 'destinations']
        read_only_fields = ['app_secret_token']
        
