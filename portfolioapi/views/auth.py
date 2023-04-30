import uuid
import base64
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.files.base import ContentFile

# @api_view decorator allows for a function-based view instead of a class-based view, since there is no reason to assign a class to the auth view. The @permission_classes decorator allows for the view to be accessed by anyone. Other policy decorators exist as well, but must be used under the @api_view decorator.

# A POST request with a username and password is sent to the login view. The authenticate function is used to check if the username and password are valid. If they are not, a 401 error is returned. If they are, the user is returned and a token is generated for the user. The token is then returned to the user.


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid Credentials'}, status=401)
    token, _ = Token.objects.get(user=user)
    return Response({'token': token.key})

# A POST request with a username, password, and email is sent to the signup view. The username and email are checked to see if they are already in use. If they are, a 400 error is returned. If they are not, a new user is created with the username, password, and email. A token is then generated for the user and returned to the user. This view only allows for a singular admin account to exist.


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_signup(request):
    """Handles creating new users."""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not username or not password or not email:
        return Response({'error': 'Please provide all required fields'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already taken'}, status=400)
    if User.objects.filter(is_superuser=True).exists():
        return Response({'error': 'An admin account already exists'}, status=400)
    user = User.objects.create_user(
        username=username, password=password, email=email)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    token = Token.objects.create(user=user)
    return Response({'token': token.key}, status=201)
