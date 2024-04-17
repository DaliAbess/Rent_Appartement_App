import hashlib
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status, authentication
from django.contrib import auth
from rest_framework.response import Response
from Utils.email_utils import send_activation_link
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
import jwt
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings


@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        if request.data.get('user').get('password') != request.data.get('user').get('password_confirmation'):
            return Response({"error": "Invalid password!"}, status=400)
        serializer = UserSerializer(data=request.data.get('user'))

        serializer.validate(request.data.get('user'))
        
        if serializer.is_valid():
            
                
            user = serializer.save()
                
            user.save()
            send_activation_link(user, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is not None:
            if not user.check_password(password):
                raise AuthenticationFailed('Incorrect password!')
            else:
                if user.status == "suspended":
                    return Response({'detail': 'Account is suspended'}, status=status.HTTP_401_UNAUTHORIZED)
                elif user.status == "disabled":
                    return Response({'detail': 'Account is disabled'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    Token.objects.filter(user=user).delete()
                    token = Token.objects.create(user=user)
                    auth.login(request, user)
                    return Response({
                        'token': token.key,
                        'user': UserSerializer(user).data
                    })
        else:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    def post(self, request):
        token = request.auth
        token.delete()
        auth.logout(request)
        return Response({
            "message": "You have successfully logged out.",
        }, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class EmailVerification(APIView):
    def get(self, request, token):
        user_id = signing.loads(token)
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return Response({"message": "You have successfully activate your account."})


@permission_classes([IsAuthenticated])
class ProfileView(APIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        if user.email != request.data.get('email'):
            if User.objects.filter(email=request.data.get('email')).count() > 0:
                return Response({"error": "Email Adresse already used!"}, status=400)
        if user.phone != request.data.get('phone'):
            if User.objects.filter(phone=request.data.get('phone')).count() > 0:
                return Response({"error": "Phone Number already used!"}, status=400)
        user.email = request.data.get('email')
        user.phone = request.data.get('phone')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


@permission_classes([IsAuthenticated])
class UpdatePasswordView(APIView):
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_copy = request.data.get('new_password_copy')
        if not old_password or not new_password or not new_password_copy:
            return Response({'error': 'Old password and new password are required fields'}, status=400)
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=400)
        if new_password != new_password_copy:
            return Response({'error': 'Invalid new password'}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({'success': 'Password updated successfully'}, status=200)


@permission_classes([IsAuthenticated])
class ResendVerificationLinkView(APIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user.is_active == True:
            return Response({'error': 'Account Already activated'}, status=400)
        send_activation_link(user, request)
        return Response({'success': 'Email was sent successfully'})


#  API to update profile image

@permission_classes([IsAuthenticated])
class ProfileAvatarView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    ALLOWED_IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'png']

    def put(self, request):
        user = User.objects.get(id=request.user.id)

        if 'avatar' in request.data:
            avatar_file = request.FILES.get('avatar')
            file_extension = avatar_file.name.split('.')[-1].lower()

            if file_extension not in self.ALLOWED_IMAGE_EXTENSIONS:
                return Response({'error': 'Invalid image format. Allowed formats: JPEG, JPG, PNG'},
                                status=400)

            # Generate a unique filename and crypt it
            file_hash = hashlib.sha256(avatar_file.read()).hexdigest()
            avatar_filename = f"{user.id}_{file_hash[:10]}.{file_extension}"
            avatar_path = os.path.join('images/', avatar_filename)

            # Save the avatar to the designated directory
            with open(avatar_path, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)

            # settings.BACKEND_HOST + avatar_filename gives us the URL of the image
            user.avatar = settings.BACKEND_HOST + "/" + avatar_path
            user.save()

            return Response({'message': 'Avatar uploaded successfully'}, status=200)
        else:
            return Response({'error': 'No avatar data provided'}, status=400)

