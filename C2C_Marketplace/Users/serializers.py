from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Model-based Serializers

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "nationality",
            "SSN",
            "phone",
            "birth_date",
        ]
    
    def validate_email(self, value):

        current_user = self.instance

        if (
            CustomUser.objects
            .exclude(id=current_user.id)
            .filter(email=value)
            .exists()
        ):
            raise serializers.ValidationError(
                "Email is already registered."
            )

        return value
    
    def update(self, instance, validated_data):

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            return instance

        except Exception:
            raise serializers.ValidationError(
                "Failed to update user."
            )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    
    class Meta:
        model = CustomUser
        fields = [
        #'__all__' 
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'password2',
        'phone',
        'SSN',
        'nationality',
        'birth_date'
        ]

    def validate(self,attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password:passwords do not match"})
        return attr

    def create(self,validated_data):
        user = CustomUser.objects.create(
        username= validated_data['username'],
        first_name= validated_data['first_name'],
        last_name= validated_data['last_name'],
        email= validated_data['email'],
        phone= validated_data['phone'],
        SSN = validated_data['SSN'],
        nationality = validated_data['nationality'],
        birth_date = validated_data['birth_date']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    token = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")
        
        # Try authenticate with username first
        user = authenticate(username=username_or_email, password=password)
        
        # If fails, try with email
        if not user:
            try:
                user_obj = CustomUser.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        
        if not user:
            raise serializers.ValidationError({"detail": "Invalid login credentials."})
        
        attrs["user"] = user
        return attrs

    def get_token(self, obj):
        user = obj.get("user")
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return token.key
        return None
    
    def get_user(self, obj):
        user = obj.get("user")
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        return None


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model =CustomUser
        fields=[
            "password",
            "password2",
        ]

    def validate(self,attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password:passwords do not match"})
        return attr