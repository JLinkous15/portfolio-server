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
