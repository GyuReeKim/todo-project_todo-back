from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .serializers import TodoSerializer, UserSerializer
# api_view는 api view 페이지를 만들어준다.
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Todo, User


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

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def todo_detail(request, id):
    todo = get_object_or_404(Todo, id=id)

    # read
    if request.method == "GET":
        # 직렬화 시킨다.
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)

    # update
    elif request.method == "PUT":
        # rest framework에서 데이터를 가져오기 위해 request.data를 사용해 가져온다.
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # 사용자가 실패했을 경우 어떤 페이지를 혹은 어떤 메세지를 보여주는 것이 좋을지 생각해야한다.
        return HttpResponse(status=400)
        
    # delete
    elif request.method == "DELETE":
        todo.delete()
        # return JsonResponse({"msg": "삭제되었습니다."})
        return HttpResponse(status=204)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def user_detail(request, id):
    user = get_object_or_404(User, id=id)

    # 내가 작성한 todo에 대한 정보만 확인할 수 있도록 설정
    if request.user != user:
        return  HttpResponse(status=403)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)