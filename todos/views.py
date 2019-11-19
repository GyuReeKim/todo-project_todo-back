from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .serializers import TodoSerializer
# api_view는 view 페이지를 만들어준다.
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.
@api_view(['POST'])
# 인증이 된 사람만 허가해준다. 튜플 형태로 넣어준다.
@permission_classes((IsAuthenticated,)) # 허가 : 조건에 맞는 사람들만 허가
@authentication_classes((JSONWebTokenAuthentication,)) # 인증
def todo_create(request):
    serializer = TodoSerializer(data=request.POST) # 인스턴스화 시켜준다.
    if serializer.is_valid():
        serializer.save()
        # 사용자가 방금 입력한 결과를 보여준다.
        # json형태로 다른 곳에서도 사용할 수 있도록 해준다.
        return JsonResponse(serializer.data)
    # 오류가 있는지 확인한다.
    return HttpResponse(status=400)