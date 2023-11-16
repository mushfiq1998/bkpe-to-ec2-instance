from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


class UsersSerializer(serializers.ModelSerializer):
    # gender = serializers.SerializerMethodField()

    # profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id",
                  "username",
                  # "is_superuser",
                  # "email",
                  # "is_verified",
                  # "is_active",
                  # "is_staff",
                  # "created_at",
                  # "updated_at",
                  # "auth_provider",
                  # "first_name",
                  # "last_name",
                  # "profile_picture",
                  # # "phone",
                  # "gender",
                  # "about",
                  # "birth_date"
                  ]
        extra_kwargs = {
            # 'password': {'required': False},
            # 'email': {'required': False},
            # 'profile_picture': {'required': False}
        }

    # def get_gender(self, obj):
    #     return obj.get_gender_display()

    # def get_profile_picture(self, obj):
    #     request = self.context.get('request')
    #
    #     return None


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    email_error_messages = {
        'email': 'That email is already taken.'}

    username_error_messages = {
        'username': 'That username is already taken.'}

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)

        if len(filtered_user_by_email) != 0:
            raise ValidationError(
                self.email_error_messages)

        filtered_user_by_username = User.objects.filter(username=username)
        if len(filtered_user_by_username) != 0:
            raise ValidationError(
                self.username_error_messages)

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResendEmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['email']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
