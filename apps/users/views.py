from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from .models import Profile, User
from .serializers import ForgotPasswordSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer, ResetPasswordSerializer, UpdatePasswordSerializer, UpdateProfileSerializer, UserListSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token


@ensure_csrf_cookie
def csrf(request):
    token = get_token(request)

    return JsonResponse({
        "csrfToken": token
    })

# @method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            return Response({
                "message": "Login successful"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=200)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "Password reset link generated",
                "link": serializer.validated_data["reset_link"]
            })
        return Response(serializer.errors, status=400)
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset successful"})
        return Response(serializer.errors, status=400)
    
class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdatePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            return Response({"message": "Password updated successfully"})
        return Response(serializer.errors, status=400)

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    

class UserPagination(PageNumberPagination):
    page_size = 10              # default limit
    page_size_query_param = 'limit'  # allow ?limit=20
    max_page_size = 100

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    
    def get(self, request):
        query = request.GET.get('q', '')

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query)
        )

        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)