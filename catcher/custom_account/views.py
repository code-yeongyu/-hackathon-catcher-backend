from django.core import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

import drf_yasg.openapi as openapi
from drf_yasg.utils import swagger_auto_schema

from custom_account.forms import SignUpForm
from custom_account.models import Account
from custom_account.serializers import AccountSerializer

SIGNUP_PARAMS = [
    openapi.Parameter('email',
                      openapi.IN_QUERY,
                      description="User's email",
                      type=openapi.TYPE_STRING),
    openapi.Parameter('username',
                      openapi.IN_QUERY,
                      description="User's username, used to login",
                      type=openapi.TYPE_STRING),
    openapi.Parameter(
        'password1',
        openapi.IN_QUERY,
        description=
        "A password that is used to login, should be the same as the field password2",
        type=openapi.TYPE_STRING),
    openapi.Parameter(
        'password2',
        openapi.IN_QUERY,
        description=
        "A password that is used to login, should be the same as the field password1",
        type=openapi.TYPE_STRING),
]


class AccountAPIView(APIView):
    PARAMS = [
        openapi.Parameter('id',
                          openapi.IN_QUERY,
                          description="primary key of user",
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter('role',
                          openapi.IN_QUERY,
                          description="Role in family",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('name',
                          openapi.IN_QUERY,
                          description="User's name, less then 10 characters",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('family_id',
                          openapi.IN_QUERY,
                          description="Family id",
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter('phone_number',
                          openapi.IN_QUERY,
                          description="11 characters of phone number",
                          type=openapi.TYPE_STRING),
        openapi.Parameter(
            'notifications',
            openapi.IN_QUERY,
            description="json typed array of invited family lists",
            type="JSON-typed array"),
        openapi.Parameter('image',
                          openapi.IN_QUERY,
                          description="Profile image",
                          type="image"),
    ]
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(operation_description="Get account info",
                         responses={
                             200: 'Successfully did requested work',
                         },
                         manual_parameters=PARAMS)
    def get(self, request):  # 프로필 조회
        profile = Account.objects.get(user=request.user)

        return Response(AccountSerializer(profile).data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Get account info",
                         responses={
                             200: 'Successfully did requested work',
                             406: 'Form not acceptable'
                         },
                         manual_parameters=PARAMS)
    def patch(self, request):
        profile = Account.objects.get(user=request.user)
        serializer = AccountSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@swagger_auto_schema(method='post',
                     operation_description="Signup",
                     responses={
                         200: 'Successfully did requested work',
                         406: 'Errors occured in form'
                     },
                     manual_parameters=SIGNUP_PARAMS)
@api_view(['POST'])
def signup(request):  # 회원가입
    form = SignUpForm(request.POST)
    if not request.POST.get('email', None) == None:
        try:
            User.objects.get(email=request.POST['email'])
            return Response({"email": "Email Already Exists."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist:  # 이메일이 중복이 아닐경우에
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                Account.objects.create(
                    user=user, family_id=Account.objects.latest("id").id + 1)
                return Response(status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def search(request, query):  # 회원가입
    accounts = Account.objects.filter(phone_number=query)
    results = serializers.serialize('json', accounts)
    return Response(results, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description=
    "Get the profile image of an user whose username is <string>",
    responses={
        200: 'Successfully did requested work',
        404: 'No image exists for the requested user'
    },)
@api_view(['GET'])
def image(request, string):  # 프로필 사진 반환
    try:
        user = User.objects.get(username=string)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if str(get_object_or_404(Account, user=user).image) is "":  # 이미지가 없을때
        return Response(status=status.HTTP_404_NOT_FOUND)

    test_file = open(
        settings.BASE_DIR + "/" +
        str(get_object_or_404(Account, user=user).image), 'rb')
    return HttpResponse(content=test_file,
                        content_type="image/jpeg",
                        status=status.HTTP_200_OK)