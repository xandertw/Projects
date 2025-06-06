import logging
import os
import json
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import requests

API_KEY = "c6849ccd61b243faa34130810252903"

FAILED_LOGINS_FILE = "failed_logins.json"

def initialize_failed_logins_file(file_path=FAILED_LOGINS_FILE):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:  
        with open(file_path, "w") as file:
            json.dump([], file)  

initialize_failed_logins_file()

def log_failed_attempt(username, ip_address, reason):
    failed_attempt = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "ip": ip_address,
        "reason": reason
    }
    
    with open(FAILED_LOGINS_FILE, "r") as file:
        failed_logins = json.load(file)
    
    failed_logins.append(failed_attempt)

    with open(FAILED_LOGINS_FILE, "w") as file:
        json.dump(failed_logins, file, indent=4)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather_view(request):
    city = request.GET.get('city', 'Kosice') 
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse({
            "city": city,
            "temperature": data['current']['temp_c'],
            "humidity": data['current']['humidity'],
            "wind_speed": data['current']['wind_kph']
        })
    else:
        return JsonResponse({"error": "Unable to fetch weather data"}, status=response.status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown IP') 

    if not username or not password:
        log_failed_attempt(username, ip_address, "Missing credentials")
        return Response({"error": "Username and password are required"}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        log_failed_attempt(None, ip_address, "Invalid username")
        return Response({"error": "Invalid username"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        log_failed_attempt(username, ip_address, "Invalid password")
        return Response({"error": "Wrong password"}, status=400)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({"message": "Successfully logged out"}, status=200)
