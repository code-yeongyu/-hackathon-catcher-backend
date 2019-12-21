import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

NUGU_JSON_FIRST = '{"response":{"version":"2.0","resultCode":"OK","output":{'
NUGU_JSON_SECOND = '},"directives":[{"type":"AudioPlayer.Play","audioItem":{"stream":{"url":"","offsetInMilliseconds":0,"progressReport":{},"token":"","expectedPreviousToken":""},"metadata":{}}}]}}'
#NUGU_OBJ = json.loads(NUGU_JSON)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def location(request):
    response_str = ""
    role = request.data['action']['parameters']['name']['value']
    if role == "첫째" or role == "둘째":
        response_str = role + "는 서울시 관악구 봉천동 4-1 에 있어!"
    else:
        response_str = role + "는 아직 등록 되어있지 않아."
    a = f'"str":"{response_str}"'
    print(NUGU_JSON_FIRST + a + NUGU_JSON_SECOND)
    return Response(NUGU_JSON_FIRST + a + NUGU_JSON_SECOND,
                    status=status.HTTP_200_OK)
