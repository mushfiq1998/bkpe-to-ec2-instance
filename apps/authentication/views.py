import os
from os.path import splitext
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import FileUploadParser, MultiPartParser
import excel2dict
from contextlib import suppress
import tempfile
import re
from django.utils.text import slugify
import uuid

from .models import User
from .renderers import UserRenderer
from .serializers import UsersSerializer, RegisterSerializer, SetNewPasswordSerializer, \
    ResetPasswordEmailRequestSerializer, \
    EmailVerificationSerializer, LoginSerializer, LogoutSerializer, ResendEmailVerificationSerializer
from .utils import Util


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UsersSerializer
    http_method_names = ['get', 'put', 'patch']

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "username", "is_superuser", "email", "is_verified", "is_active", "is_staff"]

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()

        request_data = request.data

        file = request_data.get('profile_picture', None)

        if file is not None:
            file_extension = splitext(file.name)[1].lower()
            if file_extension not in ['.jpg', '.jpeg', '.png']:
                return Response({"error": "Invalid file format. Only .jpg, .jpeg, or .png files are allowed."},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)


class UserProfile(views.APIView):
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            serializer = UsersSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyEmail(views.APIView):
    serializer_class = ResendEmailVerificationSerializer

    email_param_config = openapi.Parameter(
        'email', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[email_param_config])
    def get(self, request):
        email = request.GET.get('email')
        try:
            user = User.objects.filter(email=email)
            if len(user) != 0:
                user = user[0]
                token = RefreshToken.for_user(user).access_token
                current_site = get_current_site(request).domain
                relativeLink = reverse('email-verify')
                absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
                email_body = 'Hi ' + user.username + \
                             ' Use the link below to verify your email \n' + absurl
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Verify your email'}

                Util.send_email(data)
                return Response({'email': 'Sent Successfully'}, status=status.HTTP_201_CREATED)

            return Response({'email': 'Failed to sent verification link'}, status=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file = request.FILES['file']
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        ext = file.name.split('.')[-1]
        if ext not in ['xls']:
            return Response({'error': 'File not supported'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file to a temporary file path
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        for chunk in file.chunks():
            temp_file.write(chunk)

        file_path = temp_file.name

        # Convert Excel Sheets to python dict
        data_dict = excel2dict.to_dict(file_path)

        suppliers = data_dict["Suppliers"]

        i = 0
        j = 0
        k = 0
        for row in suppliers:

            email = str(row['Contact E-Mail']).strip()

            # Define a regular expression pattern for a valid email address
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            email_addresses = re.findall(pattern, email)

            if email_addresses:
                with suppress(Exception):
                    User.objects.update_or_create(manufacturer_number=str(row['Manufacturer Number']), defaults={
                        'username': str(row['Supplier Name']),
                        'email': str(email_addresses[0]).lower(),

                        'supplier_name': str(row['Supplier Name']),
                        'manufacturer_number': str(row['Manufacturer Number']),
                        'vendor_number': str(row['Vendor Number']),
                        'classic_industries': True if row['Classic Industries'] == "X" else False,
                        'npw': True if row['NPW'] == "X" else False,
                        'last_p_n': str(row['Last P/N ']),
                        'atech': True if row['Atech'] == "X" else False,
                        'jegs': True if row['Jegs'] == "X" else False,
                        'speedway': str(row['Speedway']),
                        'notes': str(row['Notes']),
                        'relationship_status': str(row['Relationship Stutus']),
                        'initial': str(row['INITIALS']),
                        'supplier': str(row['Supplier']),
                        'website': str(row['Web-Site']),
                        'account_numbers': str(row['Account Numbers']),
                        'log_on_info': str(row['Log-On Info']),
                        'phone': str(row['Phone']),
                        'user_address': str(row['Address']),
                        'city_state_zip_code': str(row['City, State and Zip Code']),
                        'contact_name': str(row['Contact Name']),
                        'contact_email': str(email_addresses[0]).lower(),
                        'contact_phone': str(row['Contact Phone']),
                    })
                    i += 1
            else:
                j += 1

            k += 1
            print(k)

        print(f"Created: {i}, Failed: {j}")

        temp_file.close()
        os.unlink(temp_file.name)

        return JsonResponse({'msg': 'File uploaded'}, safe=False)
        # return JsonResponse(json.dumps(camaro_parts), safe=False)
