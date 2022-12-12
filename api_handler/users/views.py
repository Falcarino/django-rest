from django.http import JsonResponse, HttpRequest
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound, ParseError

from .models import User
from .serializers import UserSerializer


class IDNotFound(NotFound):
    def __init__(self, id):
        message = f'ID {id} not found.'
        super().__init__(message)

# Perhaps make a generic view metaclass?
class UsersView(APIView):

    def __get_users_queryset(self, ids: str) -> QuerySet:
        """
        Collects all existing user ids provided in a request.
        If at least one provided id doesn't exists, returns error 404.
        Used for GET and DELETE handlers.

            Parameters:
            -----------
                ids : str
                    User ids to search for

            Returns:
            -----------
                users_qs : querySet
                    A query set, containing all found users
        """

        # Check if any users even exist
        try:
            ids = ids.strip().split(',')
        except:
            raise NotFound("No users found.")

        users_qs = User.objects.none() # Setting up an empty QuerySet()
        for id in ids:
            user = User.objects.filter(user_id=id)
            if user.exists():
                users_qs = user | users_qs # If User exists, add to the QuerySet
            else:
                raise IDNotFound(id)
        return users_qs

    def get(self, request: HttpRequest, ids=None) -> dict:
        """
        GETs several or all users, depending on whether any ids were provided or not.

            Parameters:
            -----------
                ids : str
                    User ids to search for. If none provided, GET all existing users.

            Returns:
            -----------
                A json array of found users.
        """
        if not ids:
            users = User.objects.all()
        if ids:
            users = self.__get_users_queryset(ids)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    
    def post(self, request: HttpRequest, ids=None) -> dict:
        """
        POSTs one or several users.

            Parameters:
            -----------
                request : http.HttpRequest
                    HTTP request from which the function gets json data.
                ids : None
                    There should no input for this function.

            Returns:
            -----------
                A json array of newly added users.
        """
        if not ids:
            parsed_data = JSONParser().parse(request)
            new_data = []

            for user_data in parsed_data['users']:
                serializer = UserSerializer(data=user_data)
                if serializer.is_valid():
                    serializer.save()
                    new_data.append(serializer.data)

            return JsonResponse(new_data, safe=False, status=201)
        raise ParseError('Bad request.')

    def put(self, request: HttpRequest, ids=None) -> dict:
        """
        PUTs a user.

            Parameters:
            -----------
                request : http.HttpRequest
                    HTTP request from which the function gets json data.
                ids : str
                    Id of an existing user.

            Returns:
            -----------
                Updated json data of the user.
        """
        if not ids:
            raise NotFound('Cannot update None.')
        if ids:
            # Since only one user object can be updated,
            # we just need to try to convert it to 'int'
            try:
                id = int(ids)
            except:
                raise ParseError('Bad request. Only one user can be updated.')

            try:
                user = User.objects.get(user_id=id)
                new_data = JSONParser().parse(request)

                for field, value in new_data.items():
                    setattr(user, field, value)

                serializer = UserSerializer(user, data=new_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=200)
            except:
                raise IDNotFound(id)
        raise ParseError('Bad request.')

    def delete(self, request: HttpRequest, ids=None) -> dict:
        """
        DELETEs several or all users.

            Parameters:
            -----------
                ids : str
                    User ids up for removal. If none provided, DELETE all existing users.

            Returns:
            -----------
                An empty json array.
        """
        if not ids:
            users = User.objects.all()
        if ids:
            users = self.__get_users_queryset(ids)

        serializer = UserSerializer(users, many=True)
        users.delete()
        return JsonResponse(serializer.data, safe=False, status=200)
