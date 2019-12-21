import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

NUGU_JSON = '{"response":{"version":"2.0","resultCode":"OK","output":{},"directives":[{"type":"AudioPlayer.Play","audioItem":{"stream":{"url":"","offsetInMilliseconds":0,"progressReport":{},"token":"","expectedPreviousToken":""},"metadata":{}}}]}}'
NUGU_OBJ = json.loads(NUGU_JSON)


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
    import pdb
    pdb.set_trace()
    NUGU_OBJ['response']['output']['str'] = response_str
    NUGU_FORMAT = json.dumps(NUGU_OBJ)
    return Response(json.dumps(NUGU_OBJ), status=status.HTTP_200_OK)