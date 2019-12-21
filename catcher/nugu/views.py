import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def location(request):
    import pdb
    pdb.set_trace()
    print(request.POST['action']['parameters'])
