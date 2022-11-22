from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound, ParseError

from .models import User
from .serializers import UserSerializer

class IDNotFound(NotFound):
    def __init__(self, id):
        message = f'ID {id} not found.'
        super().__init__(message)

class UsersView(APIView):

    def __get_users_queryset(self, ids):

        # Check if any users even exist
        try:
            ids = ids.strip().split(',')
        except:
            raise NotFound("No users found.")

        users_qs = User.objects.none() # Setting up an empty QuerySet()
        for id in ids:
            user = User.objects.filter(id=id)
            if user.exists():
                users_qs = user | users_qs # If User exists, add to the QuerySet
            else:
                raise IDNotFound(id)
        return users_qs

    def get(self, request, ids=None):
        if not ids:
            users = User.objects.all()
        if ids:
            users = self.__get_users_queryset(ids)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    
    def post(self, request, ids=None):
        if not ids:
            new_data = JSONParser().parse(request)
            
            for user in new_data['users']:
                serializer = UserSerializer(data=user)
                if serializer.is_valid():
                    serializer.save()
            return JsonResponse(new_data, status=201)
        raise ParseError('Bad request.')

    def put(self, request, ids=None):
        if not ids:
            raise NotFound('Cannot update None.')
        if ids:
            # Since only one user object can be updated,
            # we just need to try to convert it to 'int'
            try:
                id = int(ids)
            except:
                raise ParseError('Bad request. Only one user can be updated')

            try:
                user = User.objects.get(id=id)

                new_data = JSONParser().parse(request)
                serializer = UserSerializer(user, data=new_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=200)
            except:
                raise IDNotFound(id)
        raise ParseError('Bad request.')

    def delete(self, request, ids=None):
        if not ids:
            users = User.objects.all()
        if ids:
            users = self.__get_users_queryset(ids)

        serializer = UserSerializer(users, many=True)
        users.delete()
        return JsonResponse(serializer.data, safe=False, status=200)
