from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
                                  HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class UsersView(APIView):
    def get(self, request, ids=None):
        if not ids:
            return Response({'users': 'All Users'}, status=HTTP_200_OK)
        if ids:
            ids = ids.strip().split(',')
            if len(ids) == 1:
                return Response({'error': 'This user doesn\'t exist'}, status=HTTP_404_NOT_FOUND)
        return Response({'users': [{'id': uuid} for uuid in ids]})
    
    def post(self, request, ids=None):
        if not ids:
            return Response({'error': 'Cannot create NONE'}, status=HTTP_400_BAD_REQUEST)
        if ids:
            ids = ids.strip().split(',')
            if len(ids) > 1:
                return Response({'error': 'Can\'t create more than one user at a time'}, status=HTTP_400_BAD_REQUEST)
        return Response({'id': ids[0]}, status=HTTP_201_CREATED)

    def put(self, request, ids=None):
        if not ids:
            return Response({'error': 'Cannot update NONE'}, status=HTTP_400_BAD_REQUEST)
        if ids:
            ids = ids.strip().split(',')
            if len(ids) > 1:
                return Response({'error': 'Can\'t update more than one user at a time'}, status=HTTP_400_BAD_REQUEST)
        return Response({'id': ids[0]}, status=HTTP_200_OK)

    def delete(self, request, ids=None):
        if not ids:
            return Response({'status':'Deleted all users'}, status=HTTP_200_OK)
        else:
            ids = ids.strip().split(',')
            return Response({'users': [{'id':uuid} for uuid in ids]}, status=HTTP_200_OK)
