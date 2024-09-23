from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=[
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'phone_number',
        ]
        
    def validate(self, attrs):
        if attrs.get('password')!=attrs.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password':"confirm_password don't match with password"})
        return super().validate(attrs)
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user= User.objects.create_user(**validated_data)
        user.otp= randint(1111,9999)
        user.is_active=False
        user.save()
        # user = User(
        #     email=validated_data['email'],
        #     first_name=validated_data['first_name'],
        #     last_name=validated_data['last_name'],
        #     phone_number=validated_data.get('phone_number')
        # )
        # SUBJECT="Account Activation"
        # MESSAGE=f"""
        # Your Account has been Created
        # Your OTP is {user.otp}"""
        # EMAIL_FROM=settings.EMAIL_FROM
        # RECEPTION_LIST=[
        #     user.email
        # ]
        # send_mail(
        #     subject=SUBJECT,
        #     message=MESSAGE,
        #     from_email=EMAIL_FROM,
        #     recipient_list=RECEPTION_LIST,
            
        # )
        SUBJECT = "Account Activation"
        MESSAGE = f"""
        Your Account has been Created
        Your OTP is {user.otp}
        """
        EMAIL_FROM = settings.EMAIL_FROM
        RECEPTION_LIST = [user.email]
        try:
            send_mail(
                subject=SUBJECT,
                message=MESSAGE,
                from_email=EMAIL_FROM,
                recipient_list=RECEPTION_LIST,   
                )
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
        return user
    
class ActivationSerializer(serializers.Serializer):
    otp=serializers.IntegerField()
    email=serializers.EmailField()
    
    
class UserLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)