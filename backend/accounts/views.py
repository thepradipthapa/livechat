from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserLoginSerializer, UserVerifySerializer, UserDetailSerializer
from .utils import generate_otp, store_otp, verify_otp, clear_otp, name_from_email, get_tokens_for_user
from .tasks import send_otp_email_task
from .models import User
from .services.rate_limit_service import can_send_otp, can_verify_otp

class UserLoginView(APIView):
    """ View to handle user login via email base-OTP. """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        # Rate limit check
        if not can_send_otp(data["email"]):
            return Response(
                {"message": "Too many OTP requests, Please try again later"}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Generate + store OTP in Redis
        code = generate_otp()
        store_otp(data["email"], code)
        
        # Check if user exists
        user_exists = User.objects.filter(email=data["email"]).exists()
        
        # push email task to RebbitMQ via Celery
        send_otp_email_task.delay(data["email"], code)
        
        
        return Response(
            {"message": "OTP sent to email", "is_new_user": not user_exists}, 
            status=status.HTTP_200_OK
        )
        
class UserVerifyView(APIView):
    """ View to handle email based OTP verification. """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        if not data["email"] or not data["otp"]:
            return Response(
                {"error": "email and code are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Rate limit check
        if not can_verify_otp(data["email"], data["otp"]):
            return Response({"error": "Too many verification attempts"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # Verify OTP
        if not verify_otp(data["email"], data["otp"]):
            return Response(
                {"error": "Invalid OTP"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Clear OTP from Redis
        clear_otp(data["email"])
        
        name = name_from_email(data["email"])
        # Get or create user
        user, created = User.objects.get_or_create(email=data["email"], defaults={"name": name})
        
        user_data = UserDetailSerializer(user)
        
        # Generate JWT tokens
        tokens = get_tokens_for_user(user)
        
        return Response(
            {"message": "OTP verified successfully", "is_new_user": created, "user": user_data.data, "tokens": tokens}, 
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
        
class UserProfileView(APIView):
    """ View to retrieve user profile. """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
    
class UserListView(APIView):
    """ View to list all users. """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
        
class UserRetrieveView(APIView):
    """ View to retrieve a user by ID. """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserDetailSerializer(user)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )