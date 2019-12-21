from rest_framework.decorators import api_view
from rest_framework.response import Response
from family.models import Family
from rest_framework import status, permissions
from rest_framework import generics

from family.models import Family
from family.serializers import FamilySerializer


class FamilyCreation(generics.CreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = (permissions.IsAuthenticated, )


@api_view(['POST'])
def new_member(request):
    if request.user.is_authenticated:
        if not request.POST.get('user_name', None) == None:
            reqaccount = Account.objects.get(user=request.user)
            family = reqaccount.family
            account = Account.objects.filter(
                user=request.POST.get('user_name'))
            account.family = family
            account.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)