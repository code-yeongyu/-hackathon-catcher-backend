import json
from django.core import serializers
from django.contrib.auth.models import User

from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import drf_yasg.openapi as openapi
from drf_yasg.utils import swagger_auto_schema

from custom_account.models import Account

INVITE_PARAMS = [
    openapi.Parameter('username',
                      openapi.IN_QUERY,
                      description="username of the user to invite",
                      type=openapi.TYPE_STRING)
]
JOIN_PARAMS = [
    openapi.Parameter('family_id',
                      openapi.IN_QUERY,
                      description="id of the family to join",
                      type=openapi.TYPE_INTEGER)
]


@swagger_auto_schema(
    method='post',
    operation_description="Get members of requested user's current family",
    responses={
        200: 'Successfully did requested work',
        401: 'Unauthorized'
    },
    manual_parameters=INVITE_PARAMS)
@api_view(['POST'])
def invite(request):
    if request.user.is_authenticated:
        username = request.POST.get('username')
        if username == None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        requested_account = Account.objects.get(user=request.user)
        invited_user = User.objects.get(username=username)
        notifications = Account.objects.get(user=user_obj).notifications
        notifications = json.loads(notifications)
        notifications.append({
            'name': requested_account.name,
            'family_id': requested_account.family_id
        })
        invited_account = Account.objects.filter(user=user_obj)
        invited_account.notifications = json.dumps(notifications)
        invited_account.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='post',
    operation_description="Join a family with the given family id",
    responses={
        200: 'Successfully did requested work',
        400: 'Requested to join a family without permissions',
        401: 'Unauthorized',
        406: 'family_id not given to the parameters'
    },
    manual_parameters=JOIN_PARAMS)
@api_view(['POST'])
def join(request):
    if request.user.is_authenticated:
        family_id = request.POST.get('family_id')
        if family_id == None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        notifications = Account.objects.get(user=request.user).notifications
        notifications = json.loads(notifications)
        for notification in notifications:
            if notification.family_id == family_id:
                account = Account.objects.filter(user=request.user)
                account.family_id = family_id
                account.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='delete',
                     operation_description=
                     "Secede requested user from the user's current family",
                     responses={
                         200: 'Successfully did requested work',
                         401: 'Unauthorized'
                     })
@api_view(['DELETE'])
def secede(request):
    if request.user.is_authenticated:
        if family_id == None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        account = Account.objects.filter(user=request.user)
        account.family_id = Account.objects.latest("id").id + 1
        account.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='get',
    operation_description="Get members of requested user's current family",
    responses={
        200: 'Successfully did requested work',
        401: 'Unauthorized'
    })
@api_view(['get'])
def members(request):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        accounts = Accounts.objects.filter(family_id=account.family_id)
        results = serializers.serialize('json', accounts)
        return Response(results, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)