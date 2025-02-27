from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        print('register', token, created)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    print('TOKEN', token)
    if not token:
        return Response({'error':'Un Authenticate'}, status= status.HTTP_401_UNAUTHORIZED)
    try:
        account = Account.objects.get(app_secret_token=token)
    except:
        return Response({'error':'Invalid token'}, status=status.HTTP_403_FORBIDDEN)
    print('ACCOUNT', account)
    data = request.data
    print('DATA', data)
    for destination in account.destination_set.all():
        headers = {
            "APP_ID" : str(account.account_id),
            "APP_SECRET" : str(account.app_secret_token)
        }
        if destination.http_method == "GET":
            response = requests.get(destination.url, params=data, headers=headers)
        else:
            response = requests.request(destination.http_method, destination.url, json=data, headers=headers)
    return Response({'status':'Data sent'}, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        print('Seralizre', serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print('USER', user.email)

        token, created = Token.objects.get_or_create(user=user)
        response_data = {
            "token": token.key,
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": 'admin' if user.is_superuser else 'user'
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        print('response_data',response_data)
        return response
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchDestinationOfAccount(request, account_id):
    try:
        print(account_id)
        destinations_obj = Destination.objects.filter(account=account_id)
        serializer = DestinationSerializer(destinations_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)