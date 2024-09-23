from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from django.contrib.auth import get_user_model, authenticate
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from .models import User
from core.models import User
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .models import Student, Teacher


User=get_user_model()
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset= User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'user_create':
            return UserSerializer
        
        elif self.action == 'login':
            return UserLoginSerializer
        
        elif self.action == 'activation':
            return ActivationSerializer
    
    @swagger_auto_schema(
        method="POST",
        operation_id= "user_create",
        request_body=UserSerializer,
        responses= {
            201: UserSerializer,
            400: "UserSerailizer"
        }
    )
    @action(detail=False,methods=['POST'])
    def user_create(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    
    @swagger_auto_schema(
        method="POST",
        operation_id= "user-email-activation",
        request_body=ActivationSerializer,
        responses= {
            200: UserSerializer,
            400: UserSerializer,
            403: UserSerializer
            
        }
    )
    
    @action(detail=False,methods=["POST"])
    def activation(self, request, *args, **kwargs):
        serializer=ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data.get('email')
        otp=serializer.validated_data.get('otp')
        token = request.data.get('token')
        user=get_object_or_404(User,activation_token=token)
        if user.otp==otp:
            user.is_active=True
            user.save()
            
            send_mail(
                "ACTIVATION EMAIL",
                'Your email has been verified',
                settings.EMAIL_FROM,
                [email]
            )
            
            return Response(
            {
            'details':"Your account has been Activated"
            },
            status=status.HTTP_200_OK
            )
            
        return Response(
            {
            'details':"Invalied OTP."
            },
            status=status.HTTP_403_FORBIDDEN
            )
        
        
    @swagger_auto_schema(
        method="POST",
        operation_id="user-login",
        request_body=UserLoginSerializer,
        responses={'200':UserLoginSerializer,'403':UserLoginSerializer}
    )
        
    @action(detail=False, methods=['POST'])
    def login(self,request,*args, **kwargs):
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email=serializer.validated_data.get('email')
        password=serializer.validated_data.get('password')
        
        user=authenticate(username=email,password=password)
        
        if user:
            token,_=Token.objects.get_or_create(user=user)
            return Response({
                "id":user.pk,
                "email": email,
                "token": token.key,
            })
        
        return Response({
            'details':"Invalid Credentials."
        }, status=status.HTTP_401_UNAUTHORIZED)
        
        
@api_view(['POST'])       
def activate_user(request):
    token = request.data.get('token')  # Extract the token from the request body
    user = get_object_or_404(User, activation_token=token)  # Correct usage
    user.is_active = True
    user.save()
    return Response({'status': 'account activated'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_student(request):
    user = User.objects.create_user(username='student1', password='password')
    student = Student.objects.create(
        user=user,
        roll_number='R001',
        class_name='10th Grade',
        date_of_birth='2005-08-01'
    )
    return render(request, 'success')

@api_view(['POST']) 
def create_teacher(request):
    user = User.objects.create_user(username='teacher1', password='password')
    teacher = Teacher.objects.create(
        user=user,
        employee_id='T001',
        subject='Mathematics',
        hire_date='2020-01-10'
    )
    return render(request, 'success')