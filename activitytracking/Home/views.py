from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import person_collection
from .hashing import hash_password, check_password
from .creatingToken import create_tokens  # Ensure this function is correctly implemented
import threading
import time
import win32gui
import win32process
import psutil

# Shared state for tracking applications
tracking = False
tracked_applications = []

# HTML views
def Home(request):
    return render(request, "Home/index.html")

def Dashboard(request):
    return render(request, "Dashboard/index.html")

def Auth(request):
    return render(request, "Auth/signin.html")

def Signup(request):
    return render(request, "Auth/signup.html")

def Front(request):
    return render(request, "Front/index.html")

def Activity(request):
    return render(request, "Activity/index.html")

# DRF views for authentication
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

    if person_collection.find_one({'username': username}):
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = hash_password(password)

    # Store user in MongoDB
    person_collection.insert_one({
        'username': username,
        'email': email,
        'password': hashed_password,
    })

    # Generate JWT tokens
    user = {
        'username': username,
        'email': email,
    }
    access_token, refresh_token = create_tokens(user)

    return Response({
        'username': username,
        'access_token': access_token,
        'refresh_token': refresh_token
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = person_collection.find_one({'username': username})
    if user and check_password(user['password'], password):
        access_token, refresh_token = create_tokens(user)
        request.session['access_token'] = access_token
        return Response({
            'username': username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def protected_route(request):
    access_token = request.session.get('access_token')

    if not access_token:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = AccessToken(access_token)
        return Response({"message": "You have access to this protected route."}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    request.session.pop('access_token', None)
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

# Activity Tracking
def get_active_window_name():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def get_active_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def track_active_applications():
    global tracking, tracked_applications
    tracked_applications = []
    while tracking:
        active_window_name = get_active_window_name()
        if active_window_name and (not tracked_applications or active_window_name != tracked_applications[-1]):
            tracked_applications.append(active_window_name)
        time.sleep(3)

@api_view(['POST'])
def start_tracking(request):
    global tracking
    if not tracking:
        tracking = True
        thread = threading.Thread(target=track_active_applications)
        thread.start()
    return Response({'status': 'started'})

@api_view(['POST'])
def stop_tracking(request):
    global tracking
    tracking = False
    #add data to the database
    return Response({'status': 'stopped'})

@api_view(['GET'])
def get_applications(request):
    return Response({'applications': tracked_applications})
