from django.core import serializers
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_account.forms import SignUpForm
from custom_account.models import Account
from custom_account.serializers import AccountSerializer


class AccountAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):  # 프로필 조회
        profile = Account.objects.get(user=request.user)

        return Response(AccountSerializer(profile).data,
                        status=status.HTTP_200_OK)

    def patch(self, request):
        profile = Account.objects.get(user=request.user)
        serializer = AccountSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def signup(request):  # 회원가입
    form = SignUpForm(request.POST)
    if not request.POST.get('email', None) == None:
        try:
            User.objects.get(email=request.POST['email'])
            return Response({"email": "해당 이메일은 이미 존재합니다."},
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