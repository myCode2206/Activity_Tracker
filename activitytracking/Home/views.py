from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import person_collection
from .hashing import hash_password, check_password
from .creatingToken import *


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

    # Generate JWT tokens manually
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
    if user and check_password(user['password'],password):
        
        access_token, refresh_token = create_tokens(user)

        # Store the access token in the session
        request.session['access_token'] = access_token

        return Response({
            'username': username,
            'access_token': access_token,
            'refresh_token': refresh_token
    }, status=status.HTTP_201_CREATED)
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
    except Exception as e:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    request.session.pop('access_token', None)
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
