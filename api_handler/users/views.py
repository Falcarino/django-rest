from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound, ParseError

from .models import User
from .serializers import UserSerializer


class UsersView(APIView):
    def get(self, request, ids=None):
        if not ids:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        if ids:
            ids = ids.strip().split(',')
            if len(ids) == 1:
                try:
                    user = User.objects.get(id=ids[0])
                    serializer = UserSerializer(user)
                    return JsonResponse(serializer.data, safe=False, status=200)
                except:
                    raise NotFound('ID not found.')
        raise ParseError('Bad request. Only one ID can be processed.')
    
    def post(self, request, ids=None):
        if not ids:
            new_data = JSONParser().parse(request)
            serializer = UserSerializer(data=new_data)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        raise ParseError('Bad request.')

    def put(self, request, ids=None):
        if not ids:
            raise NotFound('Cannot update NONE.')
        if ids:
            ids = ids.strip().split(',')
            if len(ids) == 1:
                # Check if the requested id exists
                try:
                    # get requested instance
                    user = User.objects.get(id=ids[0])
                    # update data of the called instance
                    new_data = JSONParser().parse(request)
                    serializer = UserSerializer(user, data=new_data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data, status=200)
                except:
                    raise NotFound('ID not found.')
        raise ParseError('Bad request.')

    def delete(self, request, ids=None):
        if not ids:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            users.delete()
            return JsonResponse(serializer.data, safe = False, status=204)
        if ids:
            ids = ids.strip().split(',')
            if len(ids) == 1:
                try:
                    user = User.objects.get(id=ids[0])
                    user.delete()
                    serializer = UserSerializer(user)
                    return JsonResponse(serializer.data, safe=False, status=200)
                except:
                    raise NotFound('ID not found.')
        raise ParseError('Bad request.')
