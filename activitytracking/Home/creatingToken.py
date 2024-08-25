import jwt
from datetime import datetime, timedelta
from django.conf import settings

def create_tokens(user):
    # Define expiration times
    access_expiration = datetime.utcnow() + timedelta(minutes=30)  # Access token valid for 30 minutes
    refresh_expiration = datetime.utcnow() + timedelta(days=7)   # Refresh token valid for 7 days

    # Payload for access token
    access_payload = {
        'user': user['username'],
        'exp': access_expiration,
        'iat': datetime.utcnow()
    }

    # Payload for refresh token (you can add more fields if needed)
    refresh_payload = {
        'user': user['username'],
        'exp': refresh_expiration,
        'iat': datetime.utcnow()
    }

    # Create tokens
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token, refresh_token
